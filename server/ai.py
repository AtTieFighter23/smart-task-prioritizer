import json
import os
import time

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

MODEL = "gemini-flash-latest"
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


def get_priority_ranking(tasks):
    """Calls the Gemini API to rank tasks, retrying on transient failures
    (e.g. 503 UNAVAILABLE under high demand) with a short backoff.
    Returns (ranking_list, raw_response_text).
    Raises RuntimeError if every attempt fails."""
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
            last_error = f"AI API request failed: {e}"

        if attempt < MAX_RETRIES:
            time.sleep(BACKOFF_SECONDS * attempt)

    raise RuntimeError(f"{last_error} (after {MAX_RETRIES} attempts)")