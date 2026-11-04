# Reproducible LaTeX environment for the manuscript.
# TeX Live 2025 (frozen "historic" release, full scheme), pinned by digest
# so everyone builds with exactly the same TeX distribution. It matches the
# TeX Live version recommended for local installs.
# The image is amd64-only; on Apple Silicon Docker runs it under emulation.
FROM texlive/texlive:TL2025-historic@sha256:dbd65d778eb83de9b45fb0a8deb3afe44cbbaba2272e4e1e644e94dda52c7109

# make: `make pdf` inside the devcontainer; git: source control in Codespaces.
RUN apt-get update \
    && apt-get install -y --no-install-recommends make git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/docs/manuscript
