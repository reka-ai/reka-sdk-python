"""Reka API."""

import importlib.metadata
import os

# Grab it from an environment variable by default, but can be overriden
API_KEY = os.getenv("REKA_API_KEY")
# Default production server
_SERVER = os.getenv("REKA_SERVER", "https://api.reka.ai")

__version__ = importlib.metadata.version("reka-api")
from reka.v2.api.chat import chat
from reka.v2.api.dataset import add_dataset, delete_dataset, list_datasets
from reka.v2.api.models import list_models
from reka.v2.api.retrieval import (
    PrepareRetrievalStatusResponse,
    prepare_retrieval,
    retrieval_job_status,
)

__all__ = [
    "chat",
    "delete_dataset",
    "add_dataset",
    "list_models",
    "list_datasets",
    "PrepareRetrievalStatusResponse",
    "prepare_retrieval",
    "retrieval_job_status",
]
