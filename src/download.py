from pathlib import Path
from urllib.request import build_opener, install_opener, urlretrieve


def main():
    repo_root = Path(__file__).resolve().parent.parent
    raw_dir = repo_root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Set a browser-like User-Agent so the server does not block the request
    opener = build_opener()
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")]
    install_opener(opener)

    for year in range(2019, 2026):
        url = f"https://opendata.rijdendetreinen.nl/public/disruptions/disruptions-{year}.csv"
        dest_file = raw_dir / f"disruptions-{year}.csv"

        if dest_file.exists():
            print(f"Skipping {dest_file.name} (already exists)")
            continue

        urlretrieve(url, dest_file)
        print(f"Downloaded {dest_file.name}")


if __name__ == "__main__":
    main()