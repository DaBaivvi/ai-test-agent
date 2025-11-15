
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
You are a strict product test review expert.

Below is a test scoring report (JSON):
{json.dumps(payload, ensure_ascii=False, indent=2)}

Please evaluate ONLY according to the following rules to identify *abnormalities*:

1. If the raw_value clearly exceeds the normal or protocol-defined min~max range, mark it as abnormal.
2. If normalized is 0 or 1, evaluate whether this is due to extreme raw values or potential truncation.
3. If partial_score is 0 while the weight is greater than 0.1, consider it suspicious and requiring further review.
4. If any criterion shows logically inconsistent data (e.g., very large raw noise value but normalized=1), mark it as abnormal.
5. If you cannot reliably determine whether something is abnormal, explicitly state: "Unable to determine abnormality."

⚠️ IMPORTANT:
- Do NOT simply rewrite or repeat all fields.
- ONLY list the criteria that you believe have *actual problems*.
- If everything looks normal, clearly state: “No significant abnormalities found.”
- Output MUST be in Markdown format using the structure below:

## Abnormal Items
- Criterion ID: xxx
  - Issue: …
  - Basis: …

## Normal Summary
- Provide a short overall assessment (1–3 sentences)

Begin your analysis now:
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
