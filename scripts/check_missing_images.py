from pathlib import Path
import re


def main() -> None:
    root = Path("content")
    static_dir = Path("static")
    md_pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    img_pattern = re.compile(r"<img[^>]+src=\"([^\"]+)\"", re.I)

    missing: list[str] = []
    for md_file in root.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        for pattern in (md_pattern, img_pattern):
            for match in pattern.finditer(text):
                url = match.group(1).strip()
                if url.startswith(("http://", "https://", "//")):
                    continue
                if url.startswith("/"):
                    fs = static_dir / url.lstrip("/")
                else:
                    fs = (md_file.parent / url).resolve()
                if not fs.exists():
                    missing.append(f"{md_file}: {url}")

    if missing:
        print("\n".join(missing))
    else:
        print("NO_MISSING")


if __name__ == "__main__":
    main()