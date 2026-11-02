"""
Download and safely extract OASIS-1 raw MRI archives.

To download the entire dataset: uv run python scripts/download_oasis1.py
To download selected discs: uv run python scripts/download_oasis1.py --discs 1 2 3

By default the destination is data/raw
location in <project root>/scripts. See --help for options.

Review the OASIS data-use terms before downloading:
https://sites.wustl.edu/oasisbrains/request-access/
"""

import argparse
from pathlib import Path
from Neuroimaging import(
    BASE_URL,
    ARCHIVE_TEMPLATE,
    CHUNK_SIZE,
    download,
    extract,
)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--discs", nargs="+", type=int, default=list(range(1, 13)),
                        help="Disc numbers 1–12 (default: all)")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent.parent / "data" / "raw",
                        help="Extraction destination (default: project/data/raw)")
    parser.add_argument("--keep-archives", action="store_true",
                        help="Keep downloaded .tar.gz archives after extraction")
    args = parser.parse_args()
    if any(disc not in range(1, 13) for disc in args.discs):
        parser.error("Disc numbers must be between 1 and 12")
    destination = args.output.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    archives = destination / ".archives"
    markers = destination / ".extracted"
    markers.mkdir(exist_ok=True)
    for disc in dict.fromkeys(args.discs):
        filename = ARCHIVE_TEMPLATE.format(disc=disc)
        archive = archives / filename
        marker = markers / f"disc{disc}.done"
        if marker.exists():
            print(f"Skipping disc {disc}: already extracted")
            continue
        print(f"\nDisc {disc} of 12", flush=True)
        download(f"{BASE_URL}/{filename}", archive)
        extract(archive, destination, marker)
        if not args.keep_archives:
            archive.unlink()
    print("\nFinished.")


if __name__ == "__main__":
    main()
