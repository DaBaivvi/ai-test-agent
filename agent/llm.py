
import os
from typing import Dict, List
from openai import OpenAI
import json

BASE_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b-instruct")

client = OpenAI(base_url=BASE_URL, api_key=os.getenv("OPENAI_API_KEY", "ollama"))


def hf_review(protocol_id: str, details: list[dict]) -> dict:
    payload = {
        "protocol_id": protocol_id,
        "scores": details,
    }

    prompt = f"""
你是一名严格的测试审核专家。

下面是一份测试评分明细(JSON):
{json.dumps(payload, ensure_ascii=False, indent=2)}

请**只按照下面的规则判断“异常”**:

1. 如果 raw_value 明显超出常规范围（例如协议或常识中的 min~max),视为异常。
2. 如果 normalized 为 0 或 1,需要判断是否因为原始值极端 / 被截断。
3. 如果 partial_score 为 0, 但该指标权重大于 0.1,优先认为是可疑，需要复核。
4. 如果某个 criterion 的数据明显不合理（比如噪音 raw_value 很大但 normalized 却为 1),视为异常。
5. 如果你无法判断，就说明“无法判断异常”。

⚠️ 很重要：
- 不要逐条原样抄写所有字段。
- 只列出你认为“真的有问题”的指标；如果没有异常，请明确写：“未发现明显异常”。
- 输出使用 Markdown,结构如下:

## 异常项目
- 指标ID: xxx
  - 问题：……
  - 依据：……

## 正常说明
- 简要说明整体情况(1-3 句话)

现在开始你的分析：
"""

    try:
        rsp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=300,
        )
        content = rsp.choices[0].message.content.strip()
        return {"ok": True, "summary": content}
    except Exception as e:
        return {"ok": False, "summary": f"Ollama调用失败: {type(e).__name__}({e})"}