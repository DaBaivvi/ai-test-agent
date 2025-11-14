# Testbericht – Waschmaschinen / XZ-500
Protocol: wm.v1
Gesamtscore: **0.532**

## Details
- energy: raw=0.6 norm=0.400 weight=0.35 partial=0.140
  citations: cite:211b4de8, cite:ba839987 | conf=0.9
- clean: raw=0.82 norm=0.820 weight=0.35 partial=0.287
  citations: cite:211b4de8, cite:ba839987 | conf=0.9
- noise: raw=52.0 norm=0.000 weight=0.15 partial=0.000
  citations: cite:211b4de8, cite:ba839987 | conf=0.9
- service: raw=0.7 norm=0.700 weight=0.15 partial=0.105
  citations: cite:211b4de8, cite:ba839987 | conf=0.9

## Reviewer Notes
- LLM summary: ## 异常项目
- 指标ID: service
  - 问题：服务指标的原始值为0.7，但其权重仅为0.15，这表明该指标的重要性较低。然而，其对应的normalized值为0.7，且权重与原始值不匹配，可能需要进一步检查。
  - 依据：权重和原始值之间的不一致性。

- 指标ID: noise
  - 问题：噪声指标的raw_value为52.0，而normalized值为0.0。这表明该指标的数据被截断或异常处理了，因为正常情况下，噪声指标的raw_value应远小于1。
  - 依据：原始值与权重之间的不匹配。

## 正常说明
- 简要说明整体情况：
  - 在这份测试评分明细中，所有指标的权重和原始值之间存在一定的不一致性。这可能需要进一步检查以确保数据的一致性和准确性。