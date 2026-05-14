# Text And Terms

Use this reference when screen text, VA/CDVA terminology, book/product mentions, or ASR corrections matter.

## Source Of Truth

The user draft, PDF, or approved script is the source of truth for on-screen text. ASR is only for:

- Timing boundaries.
- Semantic segmentation.
- Checking whether audio is complete.

Never directly paste ASR into the video without correction.

## Screen Text Direction

Screen text must be audience-facing, not production-facing.

Good examples:

- `指标越多越犹豫`
- `方法有没有数据`
- `两根K线判断多空`
- `规则明确，才能回测`
- `用带鱼系统验收信号真假`
- `回归价格本身`

Forbidden examples:

- `书名登场`
- `背书推荐`
- `行动指令`
- `人物登场`
- `工具书推荐`
- `CTA`
- `信息动画素材`
- `静音版`
- `同步预览`
- `成品区`
- `素材区`

Viewer-facing light CTA examples, only when the narration supports them:

- `可以搜来看看`
- `先从验证表开始`
- `想系统看，就从这本开始`
- `用数据先验一遍`

## Names And Terms

Correct:

- `乔烨`
- `桥博士`
- `VA分型`
- `V分型`
- `A分型`
- `CDVA分型体系`
- `裸K分型`
- `宽论`
- `弹论`
- `带鱼系统`
- `带鱼`
- `短鱼`

Incorrect:

- `乔业`
- `乔博士`
- `CTVA`
- `CDVA分析`
- `谈论`
- `待余系统`
- `带余系统`
- `待鱼`
- `短余`

## VA Definitions

V分型:

- 当前K线收盘价高于前一根K线实体的上沿。
- 看涨信号。

A分型:

- 当前K线收盘价低于前一根K线实体的下沿。
- 看跌信号。

K线实体:

- 阳线：实体下沿是开盘价，实体上沿是收盘价。
- 阴线：实体上沿是开盘价，实体下沿是收盘价。

CDVA四种分型:

- C: 金叉。
- D: 死叉。
- V: 站上前K实体上沿。
- A: 跌破前K实体下沿。

C/D 属于指标型分型，依赖均线交叉，重视时间维度。V/A 属于裸K型分型，不依赖任何指标，重视空间维度。

## VA Article Notes

Use these notes only as guardrails. Full copy still comes from the user's approved script or PDF.

### VA 1: Cognition

Direction: 扔掉 MACD 和 KDJ，只看两根K线判断多空方向。

Key points:

- Indicators can conflict and create decision paralysis.
- VA only needs two K-lines.
- VA does not rely on technical indicators; it returns to price itself.
- Validity comes from data verification, not feeling.
- VA is part of the CDVA system proposed by 《概率的朋友》 author 桥博士.

### VA 2: Practice

Direction: 不用任何指标，只看两根K线抓买卖点。

Key points:

- Explain K-line entities and upper/lower edges.
- Use exact V/A examples.
- Mention trend confirmation, stop-loss reference, and moving-average filtering.
- VA can be programmed and backtested.

### VA 3: Comparison

Direction: 金叉死叉慢半拍，VA 更快但也要过滤噪音。

Key points:

- Moving averages and MACD lag because they emphasize process/time.
- VA emphasizes spatial result.
- Use moving averages for direction filtering.
- Use 带鱼系统 to verify whether signals are true or false.
- V starts the signal, A ends it; if ending price is higher, it is 带鱼; if lower, it is 短鱼.
