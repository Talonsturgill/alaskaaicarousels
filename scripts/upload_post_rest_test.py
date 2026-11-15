#!/usr/bin/env python3
"""Offline regression tests. No live provider calls or publishing."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import upload_post_rest as rest

FIXTURES = tempfile.TemporaryDirectory()
MEDIA = Path(FIXTURES.name) / 'released.mp4'
MEDIA.write_bytes(b'released')
SECOND = Path(FIXTURES.name) / 'second.jpg'
SECOND.write_bytes(b'second')
SHA = rest.file_hash(MEDIA)
SECOND_SHA = rest.file_hash(SECOND)


def manifest(platform='facebook', kind='video', placement='feed', repo='TexasAIDispatch'):
    alaska = repo.startswith('alaska')
    result = {'repository': 'Talonsturgill/' + repo, 'edition_id': '2026-11-10',
            'user': 'alaska_ai' if alaska else 'default', 'platform': platform,
            'placement': placement, 'segment_index': 0, 'media_type': kind,
            'media': [{'path': str(MEDIA), 'sha256': SHA}],
            'title': 'Released daily edition',
            'options': {'facebook_page_id': '2003130316607965' if alaska else '113073681274871'} if platform == 'facebook' else {}}
    if repo == 'alaskaaicarousels' and platform == 'linkedin' and kind == 'document':
        result['options'] = {'description': 'The released caption.\n\n#AlaskaAI #AlaskaEnergy #AlaskaPolicy',
                             'linkedin_first_comment': 'Track the decisions at https://alaskaaihq.com/'}
    return result


class MemoryState:
    def __init__(self):
        self.entries = {}
        self.results = {}

    def claim(self, identity, fingerprint):
        key = rest.digest(identity)
        if key in self.entries:
            raise ValueError('existing durable intent')
        claim = {'key': key, 'owner': 'unique-owner', 'fingerprint': fingerprint}
        self.entries[key] = claim
        return claim

    def save_result(self, claim, receipt):
        self.results[claim['key']] = receipt


class RestTests(unittest.TestCase):
    def setUp(self):
        self.remote = MemoryState()
        mock = patch.object(rest, 'GitState', return_value=self.remote)
        mock.start()
        self.addCleanup(mock.stop)

    def test_facebook_full_video_is_explicit(self):
        path, fields, _, _ = rest.build(manifest())
        self.assertEqual(path, '/upload')
        self.assertEqual(fields['facebook_media_type'], 'VIDEO')
        self.assertEqual(fields['video_state'], 'PUBLISHED')
        self.assertEqual(fields['platform[]'], 'facebook')

    def test_reels_cannot_override_facebook_feed(self):
        m = manifest(); m['options']['facebook_media_type'] = 'REELS'
        with self.assertRaises(ValueError): rest.build(m)

    def test_facebook_needs_verified_page(self):
        m = manifest(); m['options'] = {}
        with self.assertRaises(ValueError): rest.build(m)

    def test_all_brand_bindings(self):
        for repo, (user, org, kind) in rest.BRANDS.items():
            m = manifest('linkedin', 'video' if kind == 'video' else 'document', repo=repo.split('/')[1])
            _, fields, _, _ = rest.build(m)
            self.assertEqual(fields['user'], user)
            self.assertEqual(fields['target_linkedin_page_id'], 'urn:li:organization:' + org)
            self.assertEqual(fields['visibility'], 'PUBLIC')
            m['user'] = 'other'
            with self.assertRaises(ValueError): rest.build(m)

    def test_bound_linkedin_numeric_and_urn_normalize(self):
        for selector in ('78748279', 'urn:li:organization:78748279'):
            for repo, kind in [('TexasAIDispatch', 'video'), ('TexasAIDocket', 'document')]:
                m = manifest('linkedin', kind, repo=repo)
                m['options']['target_linkedin_page_id'] = selector
                self.assertEqual(rest.build(m)[1]['target_linkedin_page_id'], 'urn:li:organization:78748279')
        m['options']['target_linkedin_page_id'] = 'urn:li:organization:117084989'
        with self.assertRaises(ValueError): rest.build(m)

    def test_read_only_pins_and_email_redaction(self):
        for route in ('linkedin-pin', 'facebook-pin'):
            code, response = rest.read(route, {'profile_username': 'default'},
                                      send=lambda path: (200, {'user_email': 'private', 'selected_page_id': 'bound'}))
            self.assertEqual(response, {'selected_page_id': 'bound'})
            with self.assertRaises(ValueError): rest.read(route, {'profile_username': 'other'})
        response = {'history': [{'user_email': 'private', 'post_caption': 'copy', 'request_id': 'r1'}]}
        self.assertEqual(rest.redact(response)['history'][0], {'post_caption': 'copy', 'request_id': 'r1'})
        self.assertIn('user_email', response['history'][0])

    def test_unexpected_credentials_and_signed_urls_redacted(self):
        data = {'request_id': 'r1', 'job_id': 'j1', 'privacy_level': 'PUBLIC_TO_EVERYONE',
                'result': {'access_token': 'secret', 'Authorization': 'secret',
                           'refresh_token': 'secret', 'api_key': 'secret',
                           'url': 'https://storage.example/file?X-Amz-Signature=secret'},
                'post_url': 'https://facebook.com/story.php?story_fbid=123&id=456'}
        clean = rest.redact(data)
        self.assertNotIn('secret', json.dumps(clean))
        self.assertEqual(clean['post_url'], data['post_url'])
        self.assertEqual(clean['request_id'], 'r1')
        self.assertEqual(clean['privacy_level'], 'PUBLIC_TO_EVERYONE')

    def test_wrong_organization_refused(self):
        m = manifest('linkedin'); m['options']['target_linkedin_page_id'] = '117084989'
        with self.assertRaises(ValueError): rest.build(m)

    def test_unknown_platform_and_batch_refused(self):
        for platform in ('x', ['facebook', 'linkedin']):
            m = manifest(); m['platform'] = platform
            with self.assertRaises((ValueError, TypeError)): rest.build(m)

    def test_stories_have_explicit_placement(self):
        for platform, key in [('facebook', 'facebook_media_type'), ('instagram', 'media_type')]:
            m = manifest(platform, placement='story')
            self.assertEqual(rest.build(m)[1][key], 'STORIES')
            m['media'] *= 2
            with self.assertRaises(ValueError): rest.build(m)

    def test_no_story_on_linkedin(self):
        with self.assertRaises(ValueError): rest.build(manifest('linkedin', placement='story'))

    def test_instagram_photo_carousel_enum_and_order(self):
        m = manifest('instagram', 'photos', repo='TexasAIDocket')
        m['media'].append({'path': str(SECOND), 'sha256': SECOND_SHA})
        path, fields, media, _ = rest.build(m)
        self.assertEqual(path, '/upload_photos')
        self.assertEqual(fields['media_type'], 'IMAGE')
        self.assertEqual(media[1]['sha256'], SECOND_SHA)
        m['options']['media_type'] = 'CAROUSEL'
        with self.assertRaises(ValueError): rest.build(m)

    def test_youtube_photos_refused(self):
        with self.assertRaises(ValueError): rest.build(manifest('youtube', 'photos', repo='TexasAIDocket'))

    def test_document_has_only_document_schema(self):
        m = manifest('linkedin', 'document', repo='TexasAIDocket')
        path, fields, _, _ = rest.build(m)
        self.assertEqual(path, '/upload_document')
        self.assertNotIn('async_upload', fields)
        m['options']['async_upload'] = True
        with self.assertRaises(ValueError): rest.build(m)

    def test_document_native_first_comment_and_override_are_supported(self):
        m = manifest('linkedin', 'document', repo='alaskaaicarousels')
        m['options']['first_comment'] = 'Source https://example.org/primary'
        path, fields, _, _ = rest.build(m)
        self.assertEqual(path, '/upload_document')
        self.assertEqual(fields['description'], m['options']['description'])
        self.assertEqual(fields['first_comment'], m['options']['first_comment'])
        self.assertEqual(fields['linkedin_first_comment'], m['options']['linkedin_first_comment'])
        self.assertNotIn('alaskaaihq.com', fields['description'].lower())
        self.assertNotIn('async_upload', fields)

    def test_document_fallback_comment_must_be_effective(self):
        m = manifest('linkedin', 'document', repo='alaskaaicarousels')
        m['options']['first_comment'] = m['options'].pop('linkedin_first_comment')
        self.assertIn('https://alaskaaihq.com/', rest.build(m)[1]['first_comment'])
        # A generic fallback with the link does not save an override without it.
        m['options']['linkedin_first_comment'] = 'No website here'
        with self.assertRaises(ValueError): rest.build(m)

    def test_unsafe_linkedin_copy_never_claims_or_posts(self):
        base = manifest('linkedin', 'document', repo='alaskaaicarousels')
        variants = []
        for website in ('https://alaskaaihq.com/', 'AlaskaAIHQ.com', 'www.ALASKAAIHQ.com/docket/',
                        '[website](https://alaskaaihq.com/?from=linkedin)'):
            for field in ('title', 'description'):
                m = copy.deepcopy(base)
                target = m if field == 'title' else m['options']
                target[field] += '\nRead more at ' + website
                variants.append(m)
        for comment in ('', True, 123, 'https://alaskaaihq.com.evil.test/',
                        'https://alaskaaihq.com@evil.test/', 'Sources without a website'):
            m = copy.deepcopy(base); m['options']['linkedin_first_comment'] = comment
            variants.append(m)
        m = copy.deepcopy(base); del m['options']['linkedin_first_comment']; variants.append(m)
        m = copy.deepcopy(base); del m['options']['description']; variants.append(m)
        for m in variants:
            with self.subTest(m=m), tempfile.TemporaryDirectory() as d:
                with self.assertRaises(ValueError):
                    rest.upload(m, d, send=lambda *a: self.fail('unsafe POST'))
                self.assertEqual(self.remote.entries, {})
                self.assertEqual(list(Path(d).iterdir()), [])

    def test_native_comment_is_one_literal_form_field_with_parent_upload(self):
        m = manifest('linkedin', 'document', repo='alaskaaicarousels')
        m['options']['linkedin_first_comment'] = '@literal text\nRead https://alaskaaihq.com/'
        response = {'success': True, 'request_id': 'r-document', 'results': {'linkedin': {
            'success': True, 'post_id': 'urn:li:activity:123',
            'url': 'https://www.linkedin.com/feed/update/urn:li:activity:123/'}}}
        completed = subprocess.CompletedProcess([], 0, json.dumps(response) + '\n200', '')
        with tempfile.TemporaryDirectory() as d, patch.object(rest.subprocess, 'run', return_value=completed) as run:
            result = rest.upload(m, d)
        run.assert_called_once()
        args = run.call_args.args[0]
        self.assertEqual(args[-1], rest.BASE + '/upload_document')
        self.assertEqual(args[args.index('--request') + 1], 'POST')
        self.assertIn('platform[]=linkedin', args)
        self.assertIn('target_linkedin_page_id=urn:li:organization:117084989', args)
        self.assertIn('description=' + m['options']['description'], args)
        self.assertIn('linkedin_first_comment=' + m['options']['linkedin_first_comment'], args)
        self.assertEqual(sum(a.startswith('linkedin_first_comment=') for a in args), 1)
        self.assertTrue(args[args.index('--form') + 1].startswith('document=@'))
        self.assertEqual(result['state'], 'ACCEPTED')
        self.assertEqual(result['first_comment']['state'], 'UNKNOWN')
        self.assertEqual(result['first_comment']['text_sha256'],
                         hashlib.sha256(m['options']['linkedin_first_comment'].encode()).hexdigest())
        self.assertEqual(next(iter(self.remote.results.values()))['platform_post_id'], 'urn:li:activity:123')

    def test_linkedin_comment_failure_or_unknown_never_reposts_after_restart(self):
        for response in ({'success': True, 'request_id': 'r1', 'results': {'linkedin': {'success': True}}},
                         {'success': True, 'request_id': 'r1', 'warnings': ['First comment failed']},
                         {'success': False, 'request_id': 'r1', 'error': 'Comment outcome uncertain'}):
            self.remote = MemoryState()
            with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as resumed:
                m = manifest('linkedin', 'document', repo='alaskaaicarousels')
                calls = []
                def send(*args):
                    calls.append(args)
                    return 200, response
                result = rest.upload(m, first, send=send, state_store=self.remote)
                self.assertEqual(result['first_comment']['state'], 'UNKNOWN')
                self.assertEqual(result['response'], response)
                before = Path(result['receipt']).read_bytes()
                m['options']['linkedin_first_comment'] += ' Changed copy.'
                for directory in (first, resumed):
                    with self.assertRaises(ValueError):
                        rest.upload(m, directory, send=send, state_store=self.remote)
                self.assertEqual(len(calls), 1)
                self.assertEqual(Path(result['receipt']).read_bytes(), before)

    def test_other_platforms_keep_website_caption_and_comment_behavior(self):
        for platform in ('facebook', 'instagram', 'tiktok'):
            m = manifest(platform, 'photos', repo='alaskaaicarousels')
            m['title'] += '\nhttps://alaskaaihq.com/'
            m['options']['first_comment'] = 'Original comment'
            fields = rest.build(m)[1]
            self.assertEqual(fields['title'], m['title'])
            self.assertEqual(fields['first_comment'], 'Original comment')
            self.assertNotIn('linkedin_first_comment', fields)

    def test_linkedin_comment_lookup_is_read_only_and_uses_post_urn(self):
        calls = []
        response = {'comments': [{'comment_id': '456', 'author': 'urn:li:organization:117084989',
                                  'message': {'text': 'Read https://alaskaaihq.com/'}}]}
        query = {'user': 'alaska_ai', 'post_id': 'urn:li:activity:123'}
        code, got = rest.read('linkedin-comments', query,
                              send=lambda *args: (calls.append(args) or (200, response)))
        self.assertEqual(code, 200)
        self.assertEqual(got, response)
        self.assertEqual(calls, [('/uploadposts/comments?user=alaska_ai&post_id=urn%3Ali%3Aactivity%3A123&platform=linkedin',)])
        self.assertEqual(query, {'user': 'alaska_ai', 'post_id': 'urn:li:activity:123'})
        for query in ({'user': 'default', 'post_id': 'urn:li:activity:123'},
                      {'user': 'alaska_ai', 'post_id': '123'},
                      {'user': 'alaska_ai', 'post_id': 'urn:li:comment:123'},
                      {'user': 'alaska_ai', 'post_id': 'urn:li:activity:123', 'message': 'write'}):
            with self.assertRaises(ValueError):
                rest.read('linkedin-comments', query, send=lambda *a: self.fail('unexpected read'))

    def test_document_receipt_keeps_parent_reference_not_nested_comment(self):
        parent_url = 'https://www.linkedin.com/feed/update/urn:li:activity:123/'
        result = rest.compact_receipt({'state': 'ACCEPTED', 'endpoint': '/upload_document',
            'response': {'success': True, 'results': {'linkedin': {
                'first_comment': {'platform_post_id': 'comment-456', 'post_url': parent_url + '?comment=456'},
                'post_id': 'urn:li:activity:123', 'url': parent_url}}}})
        self.assertEqual(result, {'state': 'ACCEPTED', 'platform_post_id': 'urn:li:activity:123',
                                 'post_url': parent_url})

    def test_tiktok_public_not_draft(self):
        m = manifest('tiktok')
        fields = rest.build(m)[1]
        self.assertEqual(fields['post_mode'], 'DIRECT_POST')
        self.assertEqual(fields['privacy_level'], 'PUBLIC_TO_EVERYONE')
        m['options']['post_mode'] = 'MEDIA_UPLOAD'
        with self.assertRaises(ValueError): rest.build(m)

    def test_youtube_separate_description(self):
        m = manifest('youtube')
        with self.assertRaises(ValueError): rest.build(m)
        m['options']['youtube_description'] = 'Read more at https://texasaidocket.com/'
        self.assertEqual(rest.build(m)[1]['privacyStatus'], 'public')

    def test_unknown_options_and_headers_refused(self):
        for option in ('Authorization', 'api_key', 'scheduled_date', 'add_to_queue', 'platformOptions'):
            m = manifest(); m['options'][option] = 'bad'
            with self.assertRaises(ValueError): rest.build(m)

    def test_local_hash_verified_before_send(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'a.mp4'; path.write_bytes(b'video')
            m = manifest(); m['media'] = [{'path': str(path), 'sha256': hashlib.sha256(b'video').hexdigest()}]
            rest.build(m)
            path.write_bytes(b'changed')
            with self.assertRaises(ValueError): rest.build(m)

    def test_signed_or_credential_media_url_refused(self):
        for url in ('http://example.com/a', 'https://a:b@example.com/a', 'https://example.com/a?sig=secret', 'https://api.upload-post.com/a'):
            m = manifest(); m['media'][0]['url'] = url
            with self.assertRaises(ValueError): rest.build(m)

    def test_dry_run_does_not_write_or_send(self):
        with tempfile.TemporaryDirectory() as d:
            result = rest.upload(manifest(), d, True, send=lambda *a: self.fail('network'))
            self.assertEqual(result['state'], 'DRY_RUN')
            self.assertEqual(list(Path(d).iterdir()), [])

    def test_intent_durable_before_send_and_accepted_not_published(self):
        with tempfile.TemporaryDirectory() as d:
            def send(*args):
                self.assertEqual(json.loads(next(Path(d).glob('*.json')).read_text())['state'], 'UNKNOWN')
                return 200, {'request_id': 'r1', 'success': True}
            result = rest.upload(manifest(), d, send=send)
            self.assertEqual(result['state'], 'ACCEPTED')
            self.assertEqual(result['request_id'], 'r1')
            saved = json.loads(Path(result['receipt']).read_text())
            self.assertEqual(saved, result)

    def test_changed_copy_and_media_cannot_repeat_logical_delivery(self):
        with tempfile.TemporaryDirectory() as d:
            rest.upload(manifest(), d, send=lambda *a: (200, {'request_id': 'r1'}))
            m = manifest(); m['title'] = 'Changed'; m['media'][0] = {'path': str(SECOND), 'sha256': SECOND_SHA}
            with self.assertRaises(ValueError): rest.upload(m, d, send=lambda *a: self.fail('duplicate send'))

    def test_timeout_is_unknown_and_cannot_repeat(self):
        with tempfile.TemporaryDirectory() as d:
            def send(*a): raise subprocess.TimeoutExpired('curl', 190)
            self.assertEqual(rest.upload(manifest(), d, send=send)['state'], 'UNKNOWN')
            with self.assertRaises(ValueError): rest.upload(manifest(), d, send=send)

    def test_500_is_unknown_not_failed(self):
        with tempfile.TemporaryDirectory() as d:
            result = rest.upload(manifest(), d, send=lambda *a: (500, {'error': 'server'}))
            self.assertEqual(result['state'], 'UNKNOWN')
            self.assertEqual(result['response']['error'], 'server')

    def test_empty_crash_receipt_blocks_retry(self):
        with tempfile.TemporaryDirectory() as d:
            preview = rest.upload(manifest(), d, True)
            Path(preview['receipt']).touch()
            with self.assertRaises(ValueError): rest.upload(manifest(), d, send=lambda *a: self.fail('send'))

    def test_segment_receipts_are_distinct(self):
        with tempfile.TemporaryDirectory() as d:
            m = manifest(placement='story')
            first = rest.upload(m, d, True)
            m['segment_index'] = 1
            self.assertNotEqual(first['receipt'], rest.upload(m, d, True)['receipt'])

    def test_read_routes_use_exact_query_contract(self):
        cases = [('tiktok-settings', {'profile': 'default'}),
                 ('media', {'user': 'default', 'platform': 'linkedin', 'page_urn': '78748279'}),
                 ('history', {'page': '2', 'limit': '100'}), ('status', {'request_id': 'r1'})]
        for route, query in cases:
            rest.read(route, query, send=lambda path: (200, {'path': path}))
        for route, query in [('tiktok-settings', {'user': 'default'}), ('media', {'user': 'default', 'platform': 'linkedin'}), ('status', {}), ('history', {'limit': '1'})]:
            with self.assertRaises(ValueError): rest.read(route, query, send=lambda *a: self.fail('network'))

    def test_remote_claim_exists_before_post(self):
        with tempfile.TemporaryDirectory() as d:
            def send(*args):
                self.assertEqual(len(self.remote.entries), 1)
                return 200, {'request_id': 'r1'}
            result = rest.upload(manifest(), d, send=send)
            self.assertTrue(result['remote_receipt_saved'])
            self.assertEqual(next(iter(self.remote.results.values()))['request_id'], 'r1')

    def test_remote_claim_failure_never_posts(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(self.remote, 'claim', side_effect=RuntimeError('uncertain push')):
                with self.assertRaises(RuntimeError):
                    rest.upload(manifest(), d, send=lambda *a: self.fail('POST after failed claim'))
            self.assertEqual(list(Path(d).glob('*.json')), [])

    def test_fresh_container_existing_remote_claim_blocks(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            rest.upload(manifest(), first, send=lambda *a: (200, {'request_id': 'r1'}))
            with self.assertRaises(ValueError):
                rest.upload(manifest(), second, send=lambda *a: self.fail('duplicate POST'))

    def test_remote_receipt_failure_keeps_local_id_without_post_retry(self):
        calls = []
        with tempfile.TemporaryDirectory() as d:
            def send(*args):
                calls.append(args)
                return 200, {'request_id': 'r1', 'user_email': 'private'}
            with patch.object(self.remote, 'save_result', side_effect=RuntimeError('uncertain push')):
                result = rest.upload(manifest(), d, send=send)
            self.assertEqual(len(calls), 1)
            self.assertFalse(result['remote_receipt_saved'])
            self.assertEqual(result['request_id'], 'r1')
            self.assertEqual(json.loads(Path(result['receipt']).read_text())['request_id'], 'r1')

    def test_request_id_is_local_before_remote_receipt_write(self):
        with tempfile.TemporaryDirectory() as d:
            def save(claim, compact):
                local = json.loads(next(Path(d).glob('*.json')).read_text())
                self.assertEqual(local['request_id'], 'r1')
                self.assertFalse(local['remote_receipt_saved'])
                raise RuntimeError('interrupted metadata write')
            with patch.object(self.remote, 'save_result', side_effect=save):
                result = rest.upload(manifest(), d, send=lambda *a: (200, {'request_id': 'r1'}))
            self.assertEqual(result['request_id'], 'r1')

    def test_remote_receipt_contains_no_caption_paths_or_raw_errors(self):
        info = {'state': 'ACCEPTED', 'http_status': 200, 'request_id': 'r1',
                'receipt': '/private/local.json', 'response': {'caption': 'PRIVATE COPY',
                'error': 'PRIVATE ERROR', 'user_email': 'PRIVATE EMAIL', 'results': {
                'facebook': {'platform_post_id': '123_456', 'post_url': 'https://facebook.com/123_456'}}}}
        result = rest.compact_receipt(info)
        self.assertEqual(result, {'state': 'ACCEPTED', 'http_status': 200, 'request_id': 'r1',
                                 'platform_post_id': '123_456', 'post_url': 'https://facebook.com/123_456'})
        self.assertNotIn('PRIVATE', json.dumps(result))

    def test_transport_no_auth_no_redirect_no_retry_and_literal_caption(self):
        completed = subprocess.CompletedProcess([], 0, '{"request_id":"r1"}\n200', '')
        with patch.object(rest.subprocess, 'run', return_value=completed) as run:
            rest.transport('/upload', {'title': '@not-a-file', 'platform[]': 'facebook'},
                           [{'path': str(MEDIA), 'sha256': SHA}], 'video')
        args = run.call_args.args[0]
        self.assertEqual(args[:2], ['curl', '--disable'])
        self.assertNotIn('--location', args)
        self.assertEqual(args[args.index('--retry') + 1], '0')
        self.assertEqual([args[i + 1] for i, v in enumerate(args) if v == '--header'], ['Accept: application/json'])
        self.assertIn('title=@not-a-file', args)
        self.assertEqual(args[-1], rest.BASE + '/upload')

    def test_transport_nonjson_is_uncertain(self):
        completed = subprocess.CompletedProcess([], 0, '<html>error</html>\n502', '')
        with patch.object(rest.subprocess, 'run', return_value=completed):
            with self.assertRaises(RuntimeError): rest.transport('/uploadposts/users')


if __name__ == '__main__':
    unittest.main()
