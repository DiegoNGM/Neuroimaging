# Manuscript build. Run from the repository root:
#   make pdf     build docs/manuscript/build/main.pdf
#   make watch   rebuild on every save
#   make clean   remove docs/manuscript/build/
#
# Uses a local latexmk if available (also the case inside the devcontainer);
# otherwise builds inside the Docker image. Force Docker with `make pdf DOCKER=1`.

MANUSCRIPT := docs/manuscript
IMAGE      := neuroimaging-latex:tl2025
PLATFORM   := linux/amd64

HAS_LATEXMK := $(shell command -v latexmk 2>/dev/null)

ifeq ($(if $(DOCKER),,$(HAS_LATEXMK)),)
  # Repo root is mounted so ../../references.bib resolves inside the container.
  RUN := docker run --rm -it --platform $(PLATFORM) \
           --user $(shell id -u):$(shell id -g) -e HOME=/tmp \
           -v "$(CURDIR)":/workspace -w /workspace/$(MANUSCRIPT) \
           $(IMAGE)
  DEPS := image
  VIEW := -view=none
else
  RUN := cd $(MANUSCRIPT) &&
  DEPS :=
  VIEW :=
endif

.PHONY: pdf watch clean image

pdf: $(DEPS)
	$(RUN) latexmk

watch: $(DEPS)
	$(RUN) latexmk -pvc $(VIEW)

clean:
	rm -rf $(MANUSCRIPT)/build

image:
	@command -v docker >/dev/null 2>&1 || { \
	  echo "Neither latexmk nor docker found. Install one (see CONTRIBUTING.md) or use Codespaces."; exit 1; }
	docker build --platform $(PLATFORM) -t $(IMAGE) $(MANUSCRIPT)
