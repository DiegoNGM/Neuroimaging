# This file is required to make the Neuroimaging directory a package. It can be left empty.


# src/Neuroimaging/__init__.py

# Define the package version
from importlib.metadata import version as _version
__version__ = _version("Neuroimaging")

# Importing constants and functions for public use
from Neuroimaging.saving-images-function import (
    find_mri_files,
    extract_subject_id,
    process_mri,
    save_metrics_csv,
)

# Define publid API
__all__ = [
    "find_mri_files",
    "extract_subject_id",
    "process_mri",
    "save_metrics_csv",
]
