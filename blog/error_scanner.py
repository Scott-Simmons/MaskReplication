import json

from inspect_scout import Result, Scanner, Transcript, scanner


def _get_type(part: object) -> str:
    """Get content part type from either a dict or Inspect AI object."""
    if isinstance(part, dict):
        return part.get("type", "")
    return getattr(part, "type", "")


def _get_text(part: object) -> str:
    """Get text content from either a dict or Inspect AI object."""
    if isinstance(part, dict):
        return part.get("text", "")
    return getattr(part, "text", "")


@scanner(messages=None, events=["model"])
def error_scanner() -> Scanner[Transcript]:
    async def classify(transcript: Transcript) -> Result | None:
        subject_model = transcript.model
        events = transcript.events or []

        # Find judge calls: model events from a different model than the subject
        judge_calls = [
            e for e in events
            if e.event == "model" and getattr(e, "model", "") != subject_model
        ]

        if not judge_calls:
            return Result(value="error", answer="no_judge_call")

        last_judge = judge_calls[-1]
        choices = getattr(getattr(last_judge, "output", None), "choices", None) or []
        if not choices:
            return Result(value="error", answer="no_judge_call")

        content = choices[0].message.content if choices[0].message else ""

        if isinstance(content, list):
            text_parts = [p for p in content if _get_type(p) == "text"]
            reasoning_parts = [p for p in content if _get_type(p) == "reasoning"]

            if not text_parts and reasoning_parts:
                return Result(value="error", answer="reasoning_exhaustion")

            if text_parts:
                text = _get_text(text_parts[0])
                if "attachment://" in text:
                    return Result(value="error", answer="output_truncated")
                if text.strip().startswith("{"):
                    try:
                        parsed = json.loads(text)
                        if any(v is None for v in parsed.values()):
                            return Result(value="error", answer="null_values")
                        return Result(value="error", answer="subject_unparseable")
                    except json.JSONDecodeError:
                        return Result(value="error", answer="output_truncated")
                return Result(value="error", answer="output_truncated")

            return Result(value="error", answer="reasoning_exhaustion")

        elif isinstance(content, str):
            if content.strip().startswith("{"):
                try:
                    parsed = json.loads(content)
                    if any(v is None for v in parsed.values()):
                        return Result(value="error", answer="null_values")
                    return Result(value="error", answer="subject_unparseable")
                except json.JSONDecodeError:
                    return Result(value="error", answer="output_truncated")
            elif not content.strip():
                return Result(value="error", answer="reasoning_exhaustion")
            return Result(value="error", answer="output_truncated")

        return Result(value="error", answer="other")

    return classify
