# Contributing

## Bibliography

All references live in the team's **Zotero group library**. `references.bib` at the repository root is generated from it automatically and is the only bibliography file in the repo.

**To add a reference**

1. Add it to the Zotero group library (ask @Lunaaaalj for access).
2. Check that its **item type** (article, book, …), **authors** and **date** are correct: the citation key is built from them.
3. That's it. The maintainer syncs `references.bib` and commits it (`chore(bib): sync zotero library`).

**To cite**, use the key from `references.bib`. Keys follow `authorYEARword` (e.g. `prince2023understanding`):

```latex
\usepackage[backend=biber, style=apa]{biblatex}
\addbibresource{../../references.bib}  % path relative to the .tex file
...
\textcite{prince2023understanding} or \parencite{prince2023understanding}
```

**Rules**

- **Never edit `references.bib` by hand.** It is overwritten on every export, so manual changes are lost. Fix the item in Zotero instead.
- Only the maintainer (@Lunaaaalj) commits changes to `references.bib`.
- PRs that touch it are validated by the `Check bibliography` workflow ([`scripts/check_bib.py`](scripts/check_bib.py)): no `file`/`note` fields, keys in `authorYEARword` format, no duplicate keys. Run it locally with `python scripts/check_bib.py`.
- On a merge conflict in `references.bib`, don't resolve it by hand: the maintainer re-exports from Zotero.
