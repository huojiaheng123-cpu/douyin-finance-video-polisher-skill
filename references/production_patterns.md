# Production Patterns

Use this reference when turning a finance script or voiceover into the actual video plan and composition.

## House-Style Target

The target is a clean finance information-animation segment, not a course PPT, subtitle video, or marketing poster. It should feel like a white/warm-white financial editorial board driven by narration.

The strongest version alternates page forms every 4-7 seconds: hook, chart/table evidence, rule explanation, comparison, backtest metrics, and book/product proof. Keep the motion purposeful: each entrance should reveal the idea currently being spoken.

Before creating a plan for the owner's style, inspect `references/house_style_memory.md`, `assets/style-references/reference-manifest.json`, and the bundled motion sheets under `assets/style-references/motion-sheets/`.

The 7 standard videos cover three families:

- VA information animation: rule explanation, indicator contrast, K-line logic, semantic page turns.
- Book endorsement/lead: curiosity hook, IP story, value mining, book cover trust, light conversion.
- Ranking blackhorse: ranking evidence, blackhorse narrative, longer pacing, product/book ranking proof.

## Scene Plan Template

Before writing HyperFrames HTML, create a compact plan:

| Scene | Time | Narration meaning | Main visual | Support beats | Motion note |
| --- | --- | --- | --- | --- | --- |
| s1 | 0.0-8.0 | Hook/contradiction | Big headline | 2-3 chips or comparison cards | Fast headline, delayed evidence |

Each scene must have:

- One main claim, not two unrelated ideas.
- One visual metaphor or evidence layer.
- At least two timed support beats unless it is a very short hook.
- A reason for the page to exist at that exact audio moment.
- Final screen text source: user script/PDF/approved draft, not raw ASR.

## Scene Recipes

Use at least three different recipes in a 45-70 second video.

### Hook Contrast

Best for the first 3-8 seconds.

- Headline: direct contradiction or painful question.
- Support: 2-3 small chips showing familiar mistakes.
- Motion: headline lands first; chips pop in on spoken examples.
- Avoid: decorative book/product placement before the user knows why it matters.

### False Opponent

Use when the script says the viewer is looking at the wrong thing.

- Layout: left card "what the viewer sees", right card "the real opponent/problem".
- Support: simple chart line, server/grid blocks, fee tag, latency tag, or data table.
- Motion: reveal the false side first, then the real side 1-3 seconds later.

### Rule System

Use when explaining a trading method, rule, or checklist.

- Layout: numbered vertical rows or flow steps.
- Support: each row gets a small status pill such as "condition", "verify", "result".
- Motion: rows enter one by one with the corresponding phrase.
- Avoid: showing all rules before the narration reaches them.

### Backtest Evidence

Use when the script mentions history, ten years, win rate, profit/loss, sample size, or probability.

- Layout options: metric cards, result table, equity curve, red/green comparison.
- Support: 2-4 metrics such as win rate, max drawdown, profit/loss ratio, sample count.
- Motion: numbers or rows reveal after the headline, not before.
- Avoid: fake precision that the script does not imply.

### Market Chart

Use for trend, signal, K-line, MACD/KDJ/RSI, buy/sell points, or "looks profitable".

- Layout: large chart panel with one primary green line and one red/noise line.
- Support: markers for signal, failure, crossover, or result.
- Motion: draw chart strokes over 1-2 seconds; markers appear on the spoken signals.
- Avoid: complex tiny chart detail that is unreadable on mobile.

### Book/Product CTA

Use only when the narration introduces the book/product.

- Layout: headline above, book card below or side-by-side inside safe area.
- Support: 2-3 tags describing lookup value, backtest tables, indicators, or probability.
- Motion: text first, book cover next, tags last.
- Avoid: book cover off-frame, book too early, or the book dominating the whole video before the CTA.

## Ending Hook And Book Cover

Use this when the ending has a book cover, traffic guidance, private-domain prompt, QR cue, search cue, or a soft sale.

The ending is a conversion beat, not a label called "book recommendation". Reserve enough time, normally 6-12 seconds, and build it in this order:

1. **Return hook:** one viewer-facing line that closes the original pain point, e.g. `别再凭感觉试指标`.
2. **Trust proof:** show the book/tool cover as a bounded card, preferably with a small shadow and 2-3 tags such as `回测表`, `指标验证`, `K线形态`.
3. **Useful reason:** one short subtitle explaining why the viewer should continue, e.g. `先查数据，再决定要不要学`.
4. **Soft action:** only if the narration contains it, use viewer-facing wording such as `可以搜来看看`, `先从验证表开始`, or `想系统看，就从这本开始`.

Rules:

- The book cover should usually be visible for at least 3 seconds in the final segment.
- Keep the cover fully inside the safe area; common width is `335-410px` on 1080x1920.
- Do not make the book appear before the narration introduces the book, source, author, method, or final resource.
- Do not write production labels on screen: avoid `书名登场`, `背书推荐`, `行动指令`, `工具书推荐`, or `CTA`.
- A soft CTA may exist, but it must be audience-facing and match the spoken narration.
- If the book cover is unavailable, create a neutral bounded placeholder only after telling the user the real cover is missing; do not pretend it is the real book.

## Finance Visual Vocabulary

Prefer finance-native elements instead of generic decoration:

- K-line / curve / crossover stroke.
- Result table with win rate and profit/loss ratio.
- Sample count badge, "10 years", "daily", "backtest".
- Rule checklist: buy, sell, stop-loss, position.
- False comparison: "feeling" vs "data", "tactic" vs "system", "indicator" vs "verification".
- Book cover card with small tags.

Avoid:

- Big empty backgrounds.
- One sentence plus one image for every page.
- Full-screen subtitles that leave no room for platform captions.
- Tiny labels pretending to be data.
- Decorative shapes that do not explain the finance idea.

## Motion Rules

- Each scene should have 2-4 timed entrances: headline, evidence, detail, result.
- Support beats should follow spoken phrases within about 0.2-0.8 seconds.
- Transition can overlap with speech only when the new headline is already readable.
- Use short light wipes or fades. Do not use a large black slab unless the style explicitly calls for it.
- For a "static-looking" scene, animate the evidence layer: chart draw, row reveal, metric count-in, card flip, highlight sweep, or marker drop.
- Dark conclusion bars should appear near the spoken conclusion, not at scene start.

## Density Targets

For 1080x1920 mobile finance videos:

- Hook scene: 1 headline + 2-3 chips/cards.
- Explanation scene: 1 headline + 3 rows or 2 comparison panels.
- Evidence scene: 1 headline + chart/table + 2-4 markers/metrics.
- CTA scene: 1 headline + book/product card + 2-3 tags.

If a scene only has a headline and one image, enrich it before rendering.

## Quality Rubric

Score each category from 0-2. Target at least 10/12 before delivery.

| Category | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Semantic sync | Page changes ignore narration | Mostly aligned with some early/late visuals | Each visual appears when its idea is spoken |
| Visual density | One sentence plus one image | Some supporting elements | Rich but readable evidence layers |
| Mobile readability | Small or crowded text | Mostly readable | Clear at phone size with safe spacing |
| Motion review | Static screenshots only | Motion strips for some spans | Direct playback or full motion-strip review |
| Finance specificity | Generic cards/shapes | Some finance labels | Charts/tables/rules/metrics match the script |
| CTA timing | Product appears too early/late | Acceptable timing | CTA appears exactly when introduced |

If any category is 0, revise before delivering.
