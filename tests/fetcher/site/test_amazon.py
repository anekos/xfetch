import pytest

from xfetch.fetcher.site.amazon import cleanup_url


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (
            "https://www.amazon.co.jp/Some-Title/dp/B00TEST01/ref=xyz",
            "https://www.amazon.co.jp/dp/B00TEST01",
        ),
        (
            "https://www.amazon.com/Some-Title/dp/B00TEST02",
            "https://www.amazon.com/dp/B00TEST02",
        ),
        (
            "https://www.amazon.co.uk/Some-Title/dp/B00TEST03",
            "https://www.amazon.co.uk/dp/B00TEST03",
        ),
        (
            "https://www.amazon.de/Some-Title/dp/B00TEST04",
            "https://www.amazon.de/dp/B00TEST04",
        ),
    ],
)
def test_cleanup_url_strips_title_slug_across_domains(url: str, expected: str) -> None:
    assert cleanup_url(url) == expected


def test_cleanup_url_returns_input_unchanged_when_not_matching() -> None:
    url = "https://example.com/foo"
    assert cleanup_url(url) == url
