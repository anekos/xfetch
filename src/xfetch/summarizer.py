import anthropic

from xfetch.models import Article, Fetched
from xfetch.secrets import ANTHROPIC_API_KEY

MODEL = "claude-opus-4-8"

PROMPT = (
    "Summarize the following description concisely, in its original language."
    " Output only the summary itself, with no preamble or closing remarks.\n\n"
    "{text}"
)


def summarize(text: str) -> str:
    if ANTHROPIC_API_KEY is None:
        raise RuntimeError("XFETCH_ANTHROPIC_API_KEY is not set")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": PROMPT.format(text=text)}],
    )
    if response.stop_reason == "max_tokens":
        raise RuntimeError("要約が max_tokens で切れました")

    return "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()


def summarize_description(fetched: Fetched) -> None:
    if isinstance(fetched, Article) and fetched.description:
        fetched.description = summarize(fetched.description)
