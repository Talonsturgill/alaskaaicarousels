"""Alaska scope, reusable selection, source age and bounded collection regressions."""
import copy
import datetime as dt
import email.utils
import json
from pathlib import Path
import sys
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import news_headlines as n
import news_feeds as feeds

NOW = n.instant('2026-10-10T20:00:00Z')
TITLES = [
    'AI diagnoses pancreatic cancer in screening trials', 'ChatGPT faces new school privacy rules',
    'AI improves avalanche forecasts', 'AI forecasts hurricanes from satellite imagery',
    'AI accelerators reduce electricity consumption', 'Robots use AI to sort textile waste',
    'AI video raises election security concerns', 'AI deciphers ancient manuscripts',
    'AI forecasts volcanic eruptions from seismic signals', 'AI optimizes freight delivery routes',
    'AI helps astronomers map distant galaxies', 'AI restores hearing through implants',
    'AI detects deepfake telephone scams', 'AI predicts protein structures for vaccines',
    'AI improves semiconductor lithography precision', 'AI identifies invasive forest pests',
    'AI translates endangered Indigenous languages', 'AI detects bridge corrosion using drones',
    'AI compresses satellite imagery for transmission', 'AI personalizes physical rehabilitation']


def row(title='Alaska deploys AI for storm surge forecasts', host='ktoo.org', hours=1, path='story'):
    return {'title': title, 'url': f'https://{host}/{path}',
            'first_seen_at': n.stamp(NOW - dt.timedelta(hours=hours))}


def rotating(rows, now=NOW, previous=None):
    return n.snapshot({'articles': []}, now, previous or {'articles': rows}, rotate=True)


class NewsSelection(unittest.TestCase):
    def test_alaska_ai_energy_and_technology_are_eligible(self):
        for title in ['Alaska researchers use AI to forecast floods',
                      'Railbelt utilities plan a new natural gas supply',
                      '$150M in Federal Funds for Beluga-Healy Electrical Intertie',
                      'UAF opens a laboratory for autonomous drones',
                      'New interactive tsunami map helps Alaska communities prepare',
                      'Cameras in downtown Juneau parking garages are not Flock-branded']:
            self.assertTrue(n.eligible(row(title), NOW), title)

    def test_global_and_brand_only_coverage_is_rejected(self):
        for title in ['AI data center opens in Malaysia', 'Arctic energy project opens in Norway',
                      'Alaska Airlines launches AI pricing for Seattle flights',
                      'Kodiak Robotics expands AI autonomous truck operations in Texas',
                      'Bethel University opens a new AI computing lab in Minnesota',
                      'Palmer develops a new AI computing chip in England',
                      'Alaska hosts a community reading program', 'Alaska football team wins with AI forecasts',
                      'Alaska sponsored webinar introduces AI tools', 'This Day in Alaska History on oil exploration']:
            article = row(title)
            if 'Alaska Airlines' in title:
                article['summary'] = 'Alaska Airlines is expanding its Seattle-based operation.'
            self.assertFalse(n.eligible(article, NOW), title)
        self.assertTrue(n.eligible(row('Alaska Airlines opens an AI operations hub in Anchorage'), NOW))
        local = row('Kodiak plans a new electrical power link')
        local['summary'] = 'The project would serve the island community in Alaska.'
        self.assertTrue(n.eligible(local, NOW))

    def test_feed_summary_can_establish_real_alaska_context(self):
        article = row('Utilities receive funds for a new electrical intertie')
        self.assertFalse(n.eligible(article, NOW))
        article['summary'] = 'The new line links Beluga and Healy in Alaska.'
        self.assertTrue(n.eligible(article, NOW))
        for value in [None, ['Alaska'], '<b>Alaska</b>', 'Alaska ' * 200]:
            self.assertFalse(n.eligible({**article, 'summary': value}, NOW))
        text = feeds.summary_text('<p>A global AI firm expands in Singapore.</p>'
             '<p>The post A global story appeared first on Alaska Native News.</p>')
        self.assertEqual(text, 'A global AI firm expands in Singapore.')
        self.assertFalse(n.eligible({**article, 'title': 'An AI firm expands its services', 'summary': text}, NOW))

    def test_known_sources_and_safe_links(self):
        for url in ['https://ktoo.org.evil.example/story', 'http://ktoo.org/story',
                    'https://user:secret@ktoo.org/story', 'https://ktoo.org:444/story',
                    'javascript:alert(1)', 'https://unknown.example/story']:
            self.assertFalse(n.eligible({**row(), 'url': url}, NOW), url)
        self.assertIsNone(n.source('https://ktoo.org\\.evil.example/story'))

    def test_fourteen_day_window_and_old_archive_dates(self):
        self.assertTrue(n.eligible(row(hours=335), NOW))
        self.assertFalse(n.eligible(row(hours=336), NOW))
        self.assertFalse(n.eligible(row(hours=-1), NOW))
        self.assertFalse(n.eligible(row(path='2020/10/10/archive'), NOW))
        self.assertEqual(n.rank([], NOW), [])

    def test_ranking_prefers_freshness_ai_energy_then_technology(self):
        ai = row('Alaska researchers test AI avalanche forecasts', path='ai')
        energy = row('Alaska utilities invest in natural gas storage', path='energy')
        tech = row('Alaska researchers open a new drone laboratory', path='tech')
        old_ai = row('Alaska uses AI for earthquake detection', hours=90, path='old-ai')
        self.assertEqual([r['url'] for r in n.rank([old_ai, tech, energy, ai], NOW)],
                         [ai['url'], energy['url'], tech['url'], old_ai['url']])
        company = {**ai, 'url': 'https://uaf.edu/ai'}
        independent = row('Alaska AI improves energy supply forecasting', hours=20, path='independent')
        self.assertEqual(n.rank([company, independent], NOW)[0]['url'], independent['url'])

    def test_coverage_deduplicates_identical_and_sister_reporting(self):
        a = row('Alaska uses AI to forecast dangerous avalanches')
        b = row('Alaska AI forecasts dangerous avalanches in new trials', 'akbizmag.com')
        self.assertEqual(n.rank([a, b], NOW)[0]['coverage'], 2)
        identical = {**a, 'url': 'https://akbizmag.com/other'}
        self.assertEqual(n.rank([a, identical], NOW)[0]['coverage'], 1)
        result = rotating([a, b, identical])
        self.assertEqual(len(result['editions'][0]['stories']), 1)

    def test_best_ten_can_remain_across_every_edition(self):
        rows = [row('Alaska ' + t, hours=i / 2, path=str(i)) for i, t in enumerate(TITLES)]
        result = rotating(rows)
        n.validate(result)
        best = {r['url'] for r in rows[:10]}
        for edition in result['editions']:
            self.assertEqual(len(edition['stories']), 10)
            self.assertEqual({s['url'] for s in edition['stories']}, best)
        later = rotating([], NOW + n.EDITION_LENGTH, result)
        n.validate(later)
        self.assertEqual({s['url'] for s in later['editions'][0]['stories']}, best)
        retry = rotating([], NOW + dt.timedelta(minutes=5), result)
        self.assertEqual(result['editions'][0]['stories'][0]['url'], retry['selected']['url'])
        self.assertEqual([s['url'] for s in result['editions'][0]['stories']],
                         [s['url'] for s in retry['editions'][0]['stories']])

    def test_new_reporting_can_displace_weaker_reporting_on_any_collection(self):
        rows = [row('Alaska ' + t, hours=i / 2 + 1, path=str(i)) for i, t in enumerate(TITLES)]
        first = rotating(rows)
        fresh = row('Alaska AI satellite network monitors coastal erosion', hours=0, path='fresh')
        result = rotating([], NOW + dt.timedelta(minutes=10), {**first, 'articles': first['articles'] + [fresh]})
        n.validate(result)
        urls = {s['url'] for s in result['editions'][0]['stories']}
        self.assertIn(fresh['url'], urls)
        self.assertNotIn(rows[9]['url'], urls)

    def test_two_and_single_story_pools_are_sustainable(self):
        rows = [row(path='storm'), row('Alaska AI improves breast cancer screening accuracy', path='health')]
        result = rotating(rows)
        n.validate(result)
        self.assertEqual([e['selected']['url'] for e in result['editions']],
                         [rows[1]['url'], rows[0]['url'], rows[1]['url'], rows[0]['url']])
        for count in [1, 2]:
            first = rotating(rows[:count])
            for _ in range(8):
                later = n.instant(first['checked_at']) + n.EDITION_LENGTH
                first = rotating([], later, n.observation_history(json.loads(json.dumps(first))))
                n.validate(first)
                self.assertEqual(len(first['editions'][0]['stories']), count)
                self.assertTrue(all(s['first_seen_at'] == rows[0]['first_seen_at']
                                    for s in first['editions'][0]['stories']))

    def test_original_dates_survive_reindexing_and_then_expire(self):
        source = row(hours=24)
        payload = {'articles': [{**source, 'language': 'English', 'seendate': '20261009T200000Z'}]}
        first = n.snapshot(payload, NOW, rotate=True)
        payload['articles'][0]['seendate'] = '20261010T200000Z'
        second = n.snapshot(payload, NOW + dt.timedelta(hours=6), first, rotate=True)
        self.assertEqual(second['selected']['first_seen_at'], first['selected']['first_seen_at'])
        expired = rotating([], NOW + dt.timedelta(days=15), second)
        n.validate(expired)
        self.assertEqual(expired['editions'], [])
        self.assertIsNone(expired['selected'])
        last_hour = rotating([row(hours=335)])
        n.validate(last_hour)
        self.assertEqual(len(last_hour['editions']), 1)

    def test_every_supporting_story_is_validated(self):
        result = rotating([row('Alaska ' + t, hours=i, path=str(i)) for i, t in enumerate(TITLES)])
        for mutation in ['global', 'unsafe', 'duplicate', 'stale', 'oversized', 'empty']:
            bad = copy.deepcopy(result)
            pool = bad['editions'][0]['stories']
            if mutation == 'global': pool[2]['title'] = 'New AI infrastructure expands in Malaysia'
            if mutation == 'unsafe': pool[2]['url'] = 'javascript:alert(1)'
            if mutation == 'duplicate': pool[2] = copy.deepcopy(pool[1])
            if mutation == 'stale': pool[2]['first_seen_at'] = n.stamp(NOW - dt.timedelta(days=15))
            if mutation == 'oversized': pool.append(n.rank(bad['articles'], NOW)[10])
            if mutation == 'empty': pool.clear()
            with self.assertRaises(ValueError, msg=mutation): n.validate(bad)
        bad = copy.deepcopy(result)
        bad['editions'][1]['starts_at'] = bad['editions'][0]['starts_at']
        with self.assertRaises(ValueError): n.validate(bad)

    def test_rss_and_atom_dates_and_bounded_excerpts(self):
        body = b'<rss><channel><item><title>Alaska AI laboratory opens</title><link>https://www.ktoo.org/lab/</link><pubDate>Fri, 09 Oct 2026 18:00:00 +0000</pubDate><description>&lt;b&gt;Fairbanks researchers test AI.&lt;/b&gt;</description></item><item><title>Undated</title></item></channel></rss>'
        rows = feeds.articles(body)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['summary'], 'Fairbanks researchers test AI.')
        self.assertEqual(feeds.articles(body.replace(b' +0000', b'')), [])
        atom = b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Alaska AI laboratory opens</title><link href="https://www.ktoo.org/lab"/><published>2026-10-09T18:00:00Z</published><updated>2026-10-10T18:00:00Z</updated></entry></feed>'
        self.assertEqual(feeds.articles(atom)[0]['seendate'], '20261009T180000Z')
        with self.assertRaises(ValueError): feeds.articles(b'<html>unavailable</html>')
        self.assertLessEqual(len(feeds.summary_text('Alaska ' * 1000)), 1000)

    def test_university_index_keeps_only_dated_card_metadata(self):
        body = b'<ul><li><p class="title h5 internal-feed"><a href="/news/uaf-ai.php">UAF joins an AI minerals research project</a></p><p class="date m-0">October 05, 2026<br><p class="excerpt short-desc">Alaska researchers test artificial intelligence.</li></ul><footer>Alaska AI news from a publisher footer</footer>'
        rows = feeds.university_index(body)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['seendate'], '20261005T080000Z')
        self.assertEqual(rows[0]['summary'], 'Alaska researchers test artificial intelligence.')
        self.assertEqual(rows[0]['url'], 'https://www.uaf.edu/news/uaf-ai.php')
        with self.assertRaises(ValueError): feeds.university_index(b'<p>Alaska AI research in an undated page</p>')
        result = n.snapshot({'articles': rows}, NOW)
        self.assertIsNotNone(result['selected'])
        self.assertFalse(n.eligible(row('UAF time capsule revisits an AI story from nineteen ninety'), NOW))

    def test_304_and_429_state_survive_restarts(self):
        url = n.RSS_FEEDS[0]
        state = {'parser_version': 2, 'etag': '"v1"', 'ok_at': n.stamp(NOW - n.EDITION_LENGTH)}
        error = urllib.error.HTTPError(url, 304, 'Not Modified', {}, None)
        with patch.object(feeds, 'allowed'), patch.object(feeds, 'request', side_effect=error) as request:
            _, report, saved = feeds.read(url, state, NOW)
            self.assertEqual(report['status'], 'not_modified')
            self.assertEqual(request.call_args.args[1]['If-None-Match'], '"v1"')
            self.assertEqual(saved['ok_at'], n.stamp(NOW))
        error = urllib.error.HTTPError(url, 429, 'Too Many Requests', {'Retry-After': '43200'}, None)
        with patch.object(feeds, 'allowed'), patch.object(feeds, 'request', side_effect=error) as request:
            _, report, saved = feeds.read(url, {}, NOW)
            self.assertEqual(request.call_count, 1)
            self.assertEqual(saved['retry_at'], n.stamp(NOW + dt.timedelta(hours=12)))
        with patch.object(feeds, 'request') as request:
            _, report, _ = feeds.read(url, json.loads(json.dumps(saved)), NOW + n.EDITION_LENGTH)
            self.assertEqual(report['status'], 'backoff')
            request.assert_not_called()

    def test_one_robots_read_per_host_and_source_restrictions(self):
        with patch.dict(feeds._POLICIES, {}, clear=True), patch.object(feeds, 'request', return_value=(b'User-agent: *\nAllow: /\n', {})) as request:
            feeds.allowed('https://www.ktoo.org/feed/')
            feeds.allowed('https://www.ktoo.org/feed/?paged=2')
            self.assertEqual(request.call_count, 1)
        with patch.dict(feeds._POLICIES, {}, clear=True), patch.object(feeds, 'request', return_value=(b'User-agent: GPTBot\nDisallow: /\n', {})):
            with self.assertRaises(ValueError): feeds.allowed('https://www.ktoo.org/feed/')

    def test_complete_feed_failure_preserves_the_published_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / 'latest.json'
            state.write_text('last good snapshot')
            unavailable = ([], {'status': 'unavailable'}, {})
            with patch.object(n, 'STATE', state), patch.object(feeds, 'read', return_value=unavailable):
                with self.assertRaises(OSError): n.collect()
            self.assertEqual(state.read_text(), 'last good snapshot')

    def test_partial_feed_failure_and_operational_health(self):
        result = rotating([row()])
        result['feeds'] = [{'url': n.RSS_FEEDS[0], 'status': 'ok'},
                           {'url': 'https://www.akbizmag.com/feed/', 'status': 'not_modified'}]
        self.assertEqual(n.health_problems(result, NOW), [])
        self.assertTrue(n.health_problems(result, NOW + dt.timedelta(hours=19)))
        result['feeds'][1]['url'] = n.RSS_FEEDS[1]
        self.assertIn('fewer than two independent publisher feeds are available', n.health_problems(result, NOW))

    def test_visible_dates_use_the_alaska_publication_day(self):
        for seen, checked, expected in [
            ('2026-10-10T03:30:00Z', '2026-10-10T20:00:00Z', 'October 9th'),
            ('2026-11-04T08:30:00Z', '2026-11-04T20:00:00Z', 'November 3rd'),
        ]:
            article = row()
            article['first_seen_at'] = seen
            state = n.snapshot({'articles': []}, n.instant(checked), {'articles': [article]}, rotate=True)
            markup = n.markup(checked[:10], state)
            self.assertIn('datetime="' + seen + '">' + expected + '</time>', markup)

    def test_source_headlines_remain_verbatim_and_house_copy_still_has_gates(self):
        import site_build as build
        import site_signoff as signoff
        article = row('Alaska AI cannot replace engineers: a new study — published today')
        state = rotating([article])
        markup = n.markup('2026-10-10', state)
        self.assertIn(article['title'], markup)
        self.assertIn('October 10th</time>', markup)
        self.assertIn('data-news-max-age-hours="336"', markup)
        self.assertNotIn('news-toggle', markup)
        build.prose_colon_gate('index.html', markup)
        build.contraction_gate('index.html', markup)
        self.assertNotIn('cannot', signoff.visible(markup))
        self.assertEqual(build.db.BANNED.findall(n.authored_html(markup)), [])
        for gate, text in [(build.prose_colon_gate, '<p>New copy: read here</p>'),
                           (build.contraction_gate, '<p>New copy cannot pass</p>')]:
            with self.assertRaises(SystemExit): gate('index.html', markup + text)
        self.assertIn('bad: wording', n.authored_html('<cite class="other">bad: wording</cite>'))


if __name__ == '__main__':
    unittest.main()
