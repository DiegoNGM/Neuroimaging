# Contributing

Writing conventions (LaTeX, figures, commits, naming) are in [STYLE.md](STYLE.md).

## Workflow

Manuscript sections are integrated in the `manuscript` branch, which is merged into `main` at the end of each stage.

```text
issue → branch from manuscript → commits → PR to manuscript → review and merge
                                                      manuscript → main (end of stage)
```

1. **Branch.** From the issue, use _Create a branch_ and set the base to `manuscript`. This names it `<issue>-<title>`.
2. **Commit** small changes following [STYLE.md](STYLE.md), and bring in updates with `git merge origin/manuscript`.
3. **Open a PR to `manuscript`**, in English or Spanish, with `Refs #<issue>` in the description. Check that `make pdf` works first.
4. **Review.** The maintainer reviews, merges and closes the issue. It must be closed by hand: `Closes #<issue>` only works on merges into `main`.

Changes outside the manuscript (code, scripts, CI, build setup) follow the same steps, but branch from and open their PR to `main`.

## Building the PDF

| Your setup                                   | What to do                                                             |
| -------------------------------------------- | ---------------------------------------------------------------------- |
| LaTeX installed (with `latexmk` and `biber`) | `make pdf`                                                             |
| Docker, no LaTeX                             | `make pdf` (uses the Docker image)                                     |
| Neither                                      | _Code → Codespaces → Create codespace_ on your branch, then `make pdf` |

The result is `docs/manuscript/build/main.pdf`. It is a build artifact, so never commit it. `make watch` rebuilds on every save and `make clean` removes `build/`. Don't run `make` while your editor is also compiling: both write to `build/` and corrupt it.

## Where to write

Everything is in `docs/manuscript/`. Leave `main.tex` and `preamble.tex` alone unless your change is about the document setup.

| Content                                  | File                                                        |
| ---------------------------------------- | ----------------------------------------------------------- |
| Abstract                                 | `sections/abstract.tex`                                     |
| Introduction                             | `sections/introduction.tex`                                 |
| Theoretical framework                    | `sections/theoretical_framework/` (one file per subsection) |
| Related work                             | `sections/related_work.tex`                                 |
| Methods, results, discussion, conclusion | `sections/<section>.tex`                                    |
| Figures                                  | `figures/`                                                  |

## Bibliography

All references live in the team's **Zotero group library** (ask @Lunaaaalj for access). `references.bib`, at the repository root, is generated from it and is the only bibliography file in the repo.

**To add a reference**, add it to the group library and check its item type, authors and date, since the citation key is built from them. The maintainer syncs `references.bib`.

**To cite**, use its key from `references.bib`, in `authorYEARword` format:

```latex
\textcite{prince2023understanding} or \parencite{prince2023understanding}
```

**Rules**

- **Never edit `references.bib` by hand.** Every export overwrites it, so fix the item in Zotero instead.
- Only the maintainer commits `references.bib`, and re-exports it to resolve merge conflicts.
- PRs that touch it are validated by the `Check bibliography` workflow. Run it locally with `python scripts/check_bib.py`.
