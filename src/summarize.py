import json
import re

import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

PROMPT = """You write a weekly business summary for a small company.
Use ONLY the figures in the data below. Do not calculate new numbers.
Write four short bullet points covering overall results, the best product,
the product with the highest return rate, and one suggested focus for next week.
Spell out small counts in words (one, two, four). Use digits only for figures from the data.

Data:
%s
"""


def summarize(data):
    message = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=500,
        messages=[{"role": "user", "content": PROMPT % json.dumps(data, indent=2)}],
    )
    return "".join(b.text for b in message.content if b.type == "text").strip()


def _flatten(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            yield from _flatten(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _flatten(v)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        yield obj


def numbers_are_grounded(summary, data):
    allowed = set()
    for value in _flatten(data):
        allowed.add(f"{value:g}".replace(",", ""))
        allowed.add(f"{value:.0f}")
        allowed.add(f"{value:.1f}")
    found = re.findall(r"\d[\d,]*(?:\.\d+)?", summary)
    return all(n.replace(",", "") in allowed for n in found)