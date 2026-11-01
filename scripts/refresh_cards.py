"""Refresh cached profile cards, keeping the previous copy on failure."""
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree

output_dir = Path("cards")
output_dir.mkdir(exist_ok=True)
base = "https://github-profile-summary-cards.vercel.app/api/cards"
for theme, provider_theme in (("dark", "github_dark"), ("light", "github")):
    for card, endpoint in (("stats", "stats"), ("languages", "repos-per-language")):
        path = output_dir / f"{card}-{theme}.svg"
        url = f"{base}/{endpoint}?username=etonealbert&theme={provider_theme}"
        try:
            request = Request(url, headers={"User-Agent": "etonealbert-profile-refresh"})
            with urlopen(request, timeout=30) as response:
                data = response.read(1_000_000)
            root = ElementTree.fromstring(data)
            if root.tag != "{http://www.w3.org/2000/svg}svg" or len(data) < 500:
                raise ValueError("Response is not a complete SVG card")
            path.write_bytes(data)
            print(f"Updated {path}")
        except Exception as error:
            if not path.exists():
                raise RuntimeError(f"No cached copy of {path}") from error
            print(f"Keeping {path}: {error}")
