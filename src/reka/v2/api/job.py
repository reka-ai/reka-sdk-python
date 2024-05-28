"""Job-related server interactions, i.e. retrieval, finetuning."""

from enum import Enum
from typing import Any, Dict

import reka.v2.api.driver as driver


class JobStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    ERROR = "ERROR"
    COMPLETE = "COMPLETE"


def job_status(job_id: str, job_type: str) -> Dict[str, Any]:
    """Get info about a previously submitted job.

    Args:
        job_id: name/id of the job to check.
        job_type: what kind of job is this, e.g. 'prepare-retrieval'.

    Returns:
        Object representing info about the job.
    """
    return driver.make_request(
        method="get",
        endpoint=f"jobs/{job_type}/{job_id}/status",
    )
