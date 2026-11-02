
import shutil
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://download.nrg.wustl.edu/data"
ARCHIVE_TEMPLATE = "oasis_cross-sectional_disc{disc}.tar.gz"
CHUNK_SIZE = 1024 * 1024


def download(url: str, destination: Path) -> None:
    """Download to a temporary file, then atomically publish the archive."""
    if destination.is_file():
        print(f"Archive already present: {destination}")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_name(destination.name + ".part")
    # Restart an incomplete download rather than treating a partial file as valid.
    if partial.exists():
        partial.unlink()
    print(f"Downloading {url}", flush=True)
    request = urllib.request.Request(url, headers={"User-Agent": "Neuroimaging-OASIS1/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=90) as response, partial.open("wb") as out:
            expected = response.headers.get("Content-Length")
            expected_size = int(expected) if expected and expected.isdigit() else None
            total = 0
            while chunk := response.read(CHUNK_SIZE):
                out.write(chunk)
                total += len(chunk)
                if total // (100 * CHUNK_SIZE) != (total - len(chunk)) // (100 * CHUNK_SIZE):
                    print(f"  {total / (1024 ** 3):.2f} GiB downloaded", flush=True)
            if expected_size is not None and total != expected_size:
                raise IOError(f"Incomplete download: {total} of {expected_size} bytes")
        partial.replace(destination)
    except Exception:
        partial.unlink(missing_ok=True)
        raise


def extract(archive: Path, destination: Path, marker: Path) -> None:
    """Extract safely to a staging directory and move subjects into destination."""
    if marker.exists():
        print(f"Already extracted: {archive.name}")
        return
    with tempfile.TemporaryDirectory(prefix="oasis1_", dir=destination) as tmp:
        staging = Path(tmp)
        with tarfile.open(archive, "r:gz") as tar:
            members = tar.getmembers()
            # Reject links, special files, absolute paths and traversal paths.
            for member in members:
                parts = Path(member.name).parts
                if (member.name.startswith("/") or ".." in parts
                        or not (member.isfile() or member.isdir())):
                    raise ValueError(f"Unsafe archive member: {member.name}")
            # Extract file contents manually, avoiding archive metadata and links.
            for member in members:
                target = staging.joinpath(*Path(member.name).parts)
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    source = tar.extractfile(member)
                    if source is None:
                        raise IOError(f"Could not read {member.name}")
                    with source, target.open("wb") as output:
                        shutil.copyfileobj(source, output, CHUNK_SIZE)
        # The official archives may contain a common top-level folder; merge
        # directories without replacing existing files from another disc.
        for source in sorted(staging.rglob("*")):
            relative = source.relative_to(staging)
            target = destination / relative
            if source.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            elif target.exists():
                if target.stat().st_size != source.stat().st_size:
                    raise FileExistsError(f"Conflicting file: {target}")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(target))
    marker.touch()
    print(f"Extracted: {archive.name}")
