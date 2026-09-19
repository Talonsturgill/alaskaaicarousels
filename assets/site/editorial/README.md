# Editorial image accents

Two decorative spot illustrations generated with the built-in image_gen tool on September 19th, 2026. These are illustrative scenery and objects, not source photographs, maps, or evidence of a reported project. Original PNGs are retained in the task's out/image-accents-2026-09-19/ directory; WebP assets here are the production sources copied by site_build.py to docs/editorial/.

- northern-ridgeline-v1.webp: 960 x 480, shared by the homepage publication introduction and About introduction.
- field-notebook-v1.webp: 720 x 480, used in the Services Field Study card.

Resize and encode only: Sharp WebP quality 78, alpha quality 85, effort 6. Retain alpha. Decorative markup uses empty alt text and aria-hidden. Fixed intrinsic dimensions reserve space. The art is static and never sits behind copy. Small screens receive smaller compositions in normal flow.

Decorative-image guidance: https://www.w3.org/WAI/tutorials/images/decorative/
Image performance guidance: https://web.dev/learn/performance/image-performance

## Final prompts

### Northern ridgeline

Use case: stylized-concept
Asset type: small decorative editorial spot illustration for the Alaska AI website, intended to display at about 320 CSS pixels wide beside prose on a nearly black navy background.
Primary request: an exquisite hand-engraved northern mountain ridgeline, a quiet finishing touch for an established serious Alaska publication.
Subject: a compact group of angular snow-cut Alaskan alpine ridges, no identifiable named mountain, viewed from low distance, overlapping natural rock planes. Only the mountain illustration, with generous transparent margin.
Style/medium: fine intaglio engraving and scratchboard, delicate irregular ice-blue and slate-silver strokes, tiny restrained muted antique-gold touches only along two short ridges. Beautiful handmade linework and sparse stippling. Refined editorial natural-history plate, with dimensional texture; not a flat vector icon and not a photograph.
Composition: wide low silhouette, roughly 2:1 illustration; highest peak slightly right of center; lower rock hatching gently dissolves into nothing. Transparent background with real alpha. Every edge feathers into transparency, no bounding rectangle or paper sheet. No ground plane, no sky.
Color palette: luminous but restrained blue-gray #8FAEC1 linework, darker navy rock interiors, very sparse antique gold #B39858. It must remain visible on #030710 and never be bright white.
Constraints: no words, letters, labels, numbers, map markings, star, moon, sun, aurora, border, logo, badge, frame or watermark. No synthetic neon glow. This is atmosphere, not a map or depiction of a reported site. Render at high quality, landscape.

### Field notebook

Use case: stylized-concept
Asset type: small decorative editorial spot illustration for the Alaska AI website Field Study service, displayed about 250 CSS pixels wide in the vacant right-hand space of a dark navy service panel.
Primary request: a beautifully observed field notebook and simple graphite pencil, rendered as an understated handmade engraving, a visual cue for careful research.
Subject: one slim open field notebook with slightly curved cream-gray paper, three-quarter view from above, one plain slender pencil laid diagonally alongside it. On the open pages only a few very faint loose unlabelled terrain contour curves; the pages are otherwise quiet. No writing or text. No technology devices.
Style/medium: fine intaglio engraving and scratchboard with delicate irregular ice-blue and slate-silver hatch marks, sparse stipple and dimensional paper texture, tiny muted antique-gold detail on the notebook binding and pencil. Sophisticated editorial spot art, not an icon, not a 3D app emoji and not a photograph.
Composition: compact, balanced arrangement; the open book and pencil fully visible; transparent background with real alpha and generous negative space around the objects; soft hatching at their bases fading to transparency; no enclosing rectangle or scene.
Color palette: blue-gray #8FAEC1 linework, charcoal navy interiors, restrained antique gold #B39858. Paper should be dark slate silver, not a large bright white area. Legible on nearly black #030710.
Constraints: no words, letters, numbers, labels, logos, watermark, badges, stars, glows, mountains outside the page, mugs, plants or extra objects. It is decorative artwork and never a mock record. Render at high quality.

