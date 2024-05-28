"""Retrieval-related server interactions, i.e. retrieval, finetuning."""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, List, cast

from requests.exceptions import HTTPError

import reka.v2.api.driver as driver
import reka.v2.api.job as job
from reka.v2.errors import RetrievalError


@dataclasses.dataclass
class PrepareRetrievalStatusResponse:
    """Status of a `prepare-retrieval` job.

    Args:
        job_status: The current status.
        detail: Further details, if any.
    """

    job_status: job.JobStatus
    detail: str
    history: List[Dict[str, Any]]

    def is_error(self) -> bool:
        """Whether the job has ended with an error."""
        return self.job_status == job.JobStatus.ERROR

    def is_complete(self) -> bool:
        """Whether the job has completed successfully."""
        return self.job_status == job.JobStatus.COMPLETE

    def is_running(self) -> bool:
        """Whether the job is still running."""
        return self.job_status == job.JobStatus.RUNNING

    def is_done(self) -> bool:
        """Whether the job has completed, either succesfully or with an error."""
        return self.job_status in [job.JobStatus.COMPLETE, job.JobStatus.ERROR]

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> PrepareRetrievalStatusResponse:
        try:
            status_str = dict.pop("job_status")
            job_status = job.JobStatus[status_str]
            dict["job_status"] = job_status
            return cls(**dict)

        except KeyError as e:
            raise TypeError(f"Invalid parameterisation for {cls.__name__}") from e


def prepare_retrieval(dataset_name: str) -> str:
    """Prepare dataset_name for retrieval later, creating a `prepare-retrieval` job.

    Args:
        dataset_name: name of previously uploaded dataset to prepare for retrieval

    Raises:
        RetrievalError if there is something wrong with retrieval preparation, e.g.
        no such dataset uploaded, or retrieval already prepared

    Returns:
        ID of the `prepare-retrieval` job, to be used for tracking.
    """
    try:
        resp = cast(
            str,
            driver.make_request(
                method="post", endpoint=f"datasets/{dataset_name}/prepare-retrieval"
            ),
        )
        return resp

    except HTTPError as e:
        if (
            e.response.status_code == 400
            and "Retrieval has already been prepared for dataset" in e.response.text
        ):
            raise RetrievalError(
                underlying=e,
                reason="Retrieval has already been prepared for this dataset.",
            )
        elif e.response.status_code == 404:
            raise RetrievalError(
                underlying=e,
                reason="Tried to prepare retrieval for non-existent dataset.",
            )
        else:
            raise RetrievalError(
                underlying=e,
            )


def retrieval_job_status(job_id: str) -> PrepareRetrievalStatusResponse:
    """Given a prepare retrieval job id, check the status.

    Args:
        job_id: id of the `prepare-retrieval` job.

    Returns:
        The current state of the job.
    """
    try:
        resp = job.job_status(job_id=job_id, job_type="prepare-retrieval")

        return PrepareRetrievalStatusResponse.from_dict(resp)

    except HTTPError as e:
        if e.response.status_code == 404:
            raise RetrievalError(underlying=e, reason="Retrieval job not found.")

        else:
            raise RetrievalError(underlying=e)
