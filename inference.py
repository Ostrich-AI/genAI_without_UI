import json
import os
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd


def discover_input_path() -> str:
    dataset_dir = Path("dataset")
    preferred = dataset_dir / "input.csv"
    if preferred.exists():
        return str(preferred)

    matches = sorted(dataset_dir.glob("input.*"))
    if not matches:
        raise FileNotFoundError("Missing input file. Expected dataset/input.<ext> (e.g. dataset/input.csv).")

    for p in matches:
        if p.suffix.lower() == ".csv":
            return str(p)

    if len(matches) == 1:
        return str(matches[0])

    raise FileNotFoundError(f"Multiple candidate inputs found: {[str(p) for p in matches]}")


def openai_generate(prompt: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

    url = f"{base_url}/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        raise RuntimeError(f"OpenAI HTTP error: {e.code} {e.reason}: {err[:500]}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to reach OpenAI at {base_url}. Error: {e}") from e

    doc = json.loads(body)
    try:
        return str(doc["choices"][0]["message"]["content"])
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"Unexpected OpenAI response: {doc}") from e


def ollama_generate(prompt: str) -> str:
    host = os.environ.get("OLLAMA_HOST", "http://0.0.0.0:11434").rstrip("/")
    model = os.environ.get("OLLAMA_MODEL", "tinyllama")
    num_predict = int(os.environ.get("OLLAMA_NUM_PREDICT", "128"))

    url = f"{host}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": num_predict, "temperature": 0},
    }
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Failed to reach Ollama at {host}. Start Ollama and run `ollama pull {model}`. Error: {e}"
        ) from e

    doc = json.loads(body)
    if not isinstance(doc, dict) or "response" not in doc:
        raise RuntimeError(f"Unexpected Ollama response: {doc}")
    return str(doc["response"])


def build_prompt(row: dict) -> str:
    system = str(row.get("prompt", "")).strip()
    question = str(row.get("question", "")).strip()
    context = str(row.get("context", "")).strip()

    return (
        f"{system}\n\n"
        f"Question:\n{question}\n\n"
        f"Context:\n{context}\n\n"
        "Answer:"
    )


def main() -> None:
    os.makedirs("output", exist_ok=True)

    input_path = discover_input_path()
    df = pd.read_csv(input_path)
    required = {"prompt", "question", "context"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required column(s) in {input_path}: {sorted(missing)}")

    use_openai = bool(os.environ.get("OPENAI_API_KEY"))
    gen = openai_generate if use_openai else ollama_generate

    answers = [gen(build_prompt(row)) for row in df.to_dict(orient="records")]
    df_out = df.copy()
    df_out["answer"] = answers
    df_out["target"] = answers
    df_out.to_csv("output/output.csv", index=False)


if __name__ == "__main__":
    main()

