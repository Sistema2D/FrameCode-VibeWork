"""Select complete optional chunks under an explicit, estimated JSON budget."""
from __future__ import annotations

import json


def estimated_tokens(results: list[dict]) -> int:
    return (len(json.dumps(results, ensure_ascii=False, indent=2)) + 3) // 4 if results else 0


def select_chunks(candidates: list[dict], mandatory: list[str], *, budget: int,
                  top_k: int = 8, per_file: int = 2) -> dict:
    if type(budget) is not int or budget < 0 or not 0 <= top_k <= 20 or not 1 <= per_file <= 20:
        raise ValueError("invalid optional budget or chunk limits")
    selected, decisions, texts, ids, counts = [], [], set(), set(), {}
    for candidate in candidates:
        path, chunk_id = candidate["path"], candidate["chunk_id"]
        content = candidate["excerpt"].strip()
        reason = ("mandatory_path" if path in mandatory else "duplicate_id" if chunk_id in ids
                  else "duplicate_content" if content in texts else "empty" if not content
                  else "top_k" if len(selected) >= top_k
                  else "per_file" if counts.get(path, 0) >= per_file
                  else "budget" if estimated_tokens([*selected, candidate]) > budget else "selected")
        decisions.append({"chunk_id": chunk_id, "path": path, "decision": reason})
        if reason == "selected":
            selected.append(candidate)
            texts.add(content)
            ids.add(chunk_id)
            counts[path] = counts.get(path, 0) + 1
    return {"results": selected, "decisions": decisions, "budget": budget,
            "estimated_optional_tokens": estimated_tokens(selected),
            "estimator": "ceil(Unicode characters in indent=2 JSON result array / 4); not model tokens",
            "complete_chunks": True}
