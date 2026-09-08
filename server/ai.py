import json
import os
import time

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# flash-lite carries a much larger free-tier daily quota than full flash,
# and is more than capable for a simple structured-ranking task like this.
MODEL = "gemini-flash-lite-latest"
MAX_RETRIES = 3
BACKOFF_SECONDS = 2  # multiplied by attempt number: 2s, 4s, 6s


def build_prompt(tasks):
    lines = []
    for t in tasks:
        due = t.due_date.isoformat() if t.due_date else "no due date"
        lines.append(
            f'- id={t.id}, title="{t.title}", due_date={due}, user_priority={t.user_priority}'
        )
    task_list = "\n".join(lines)

    return (
        "You are a productivity assistant. Rank the following tasks by priority, "
        "considering due dates (sooner = more urgent) and the user's own priority "
        "label (high > medium > low) as a strong signal of importance.\n\n"
        f"{task_list}\n\n"
        "Respond with a JSON array in this exact format:\n"
        '[{"task_id": <int>, "rank": <int starting at 1>, "rationale": "<one short sentence>"}]'
    )


def is_quota_error(exc):
    """Daily/rate quota errors (429 RESOURCE_EXHAUSTED) should never be
    retried — retrying only burns more of an already-exhausted quota."""
    text = str(exc)
    return "RESOURCE_EXHAUSTED" in text or "429" in text


def get_priority_ranking(tasks):
    """Calls the Gemini API to rank tasks, retrying on transient failures
    (e.g. 503 UNAVAILABLE) with a short backoff, but failing immediately on
    quota errors since those won't resolve by retrying.
    Returns (ranking_list, raw_response_text).
    Raises RuntimeError if every attempt fails (or immediately on quota)."""
    prompt = build_prompt(tasks)
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            raw_text = response.text
            ranking = json.loads(raw_text)
            return ranking, raw_text

        except json.JSONDecodeError as e:
            last_error = f"AI response was not valid JSON: {e}"

        except Exception as e:
            if is_quota_error(e):
                raise RuntimeError(
                    "Daily free-tier quota exceeded for this model. "
                    "This resets at midnight Pacific Time — try again later, "
                    "or switch to a different model/provider in the meantime."
                )
            last_error = f"AI API request failed: {e}"

        if attempt < MAX_RETRIES:
            time.sleep(BACKOFF_SECONDS * attempt)

    raise RuntimeError(f"{last_error} (after {MAX_RETRIES} attempts)")