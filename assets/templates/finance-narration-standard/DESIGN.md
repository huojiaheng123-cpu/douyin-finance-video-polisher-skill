# Finance Narration Standard

Use this visual identity for Chinese finance narration videos that should match the owner's current production style.

## Canvas

- Size: 1080x1920.
- Safe content area: left/right 72-92px, top 70-130px, bottom important content above y=1540.
- Background: warm editorial white with a very light green tint, no dark full-screen hero, no decorative orbs.

## Colors

- Ink: `#141414` for main text.
- Muted text: `#6b6256`.
- Signal green: `#00785d` for key words, numbers, and positive/verification marks.
- Warm gold: `#b38b42` for labels, dividers, and trust cues.
- Warning red: `#df605d` for false signal or risk.
- Card white: `#fffdf7`.
- Deep card: `#101820`.

## Typography

- Preferred Windows stack: `Microsoft YaHei UI`, `Microsoft YaHei`, `SimHei`, `Arial`, sans-serif.
- Cover headline: 86-96px bold, 2-3 lines.
- Scene headline: 74-88px bold.
- Supporting text: 30-42px.
- Tiny labels: minimum 22px.
- Letter spacing: 0.

## Layout Recipes

- Hook contrast: large headline plus 2-3 chips or error cards.
- False opponent: "viewer sees" vs "real problem" comparison.
- Rule system: three numbered rows for condition, verification, execution.
- Backtest evidence: table or curve plus 2-4 metrics.
- Book/product CTA: book card only when narration introduces it.

## Motion

- Build final layout in CSS first, then use `gsap.from()` for entrances.
- Headline lands first, evidence follows 0.2-0.8s after matching narration phrase.
- Use light fade/wipe transitions. Avoid large black slabs.
- Do not show all support elements at once.

## Do Not

- Do not create a landing page.
- Do not add full subtitles unless explicitly requested.
- Do not place important text in the bottom platform-caption zone.
- Do not use one headline plus one image as every scene.
- Do not let a book/product card appear before the narration introduces it.
