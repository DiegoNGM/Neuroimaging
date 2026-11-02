# This file is required to make the Neuroimaging directory a package. It can be left empty.


# src/Neuroimaging/__init__.py

# Define the package version
from importlib.metadata import version as _version
__version__ = _version("Neuroimaging")

# Importing constants and functions for public use
from Neuroimaging.saving_images_function import (
    find_mri_files,
    extract_subject_id,
    process_mri,
    save_metrics_csv,
)

from Neuroimaging.download import (
    BASE_URL,
    ARCHIVE_TEMPLATE,
    CHUNK_SIZE,
    download,
    extract,
)

# Define publid API
__all__ = [
    "find_mri_files",
    "extract_subject_id",
    "process_mri",
    "save_metrics_csv",
]
