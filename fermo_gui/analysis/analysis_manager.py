"""Manages fermo_core data analysis

Copyright (c) 2022-present Mitja Maximilian Zdouc, PhD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json
from pathlib import Path
from time import sleep
from typing import Self

from celery import shared_task
from pydantic import BaseModel, DirectoryPath, AnyUrl

from fermo_gui.analysis.general_manager import GeneralManager

# TODO(MMZ 14.2.24): Cover with tests


@shared_task(ignore_result=False)
def start_fermo_core(metadata: dict) -> bool:
    """Start fermo_core analysis via FermoAnalysisManager

    Arguments:
        metadata: a dict containing metadata for running of the job

    Returns:
        True if job successful, False if error was raised
    """
    try:
        params = GeneralManager().read_data_from_json(
            metadata.get("upload_path"), f"{metadata.get('job_id')}.params.json"
        )

        manager = FermoAnalysisManager(params=params, **metadata)
        manager.run_manager()

        if metadata.get("email_notify"):
            GeneralManager().email_notify_success(
                root_url=metadata.get("root_url"),
                address=metadata.get("email"),
                job_id=metadata.get("job_id"),
            )
        return True
    except Exception as e:
        # TODO(MMZ 12.2.24): dump the error in the correct location - append to log?
        log = {
            "message_log": [
                "step1",
                "step2",
            ]
        }
        log["message_log"].append(str(e))
        # TODO(MMZ 13.2.24): Error messages raised inside Celery are empty - FYI

        GeneralManager().store_data_as_json(
            metadata.get("upload_path"), f"{metadata.get('job_id')}.log.json", log
        )

        if metadata.get("email_notify"):
            GeneralManager().email_notify_fail(
                root_url=metadata.get("root_url"),
                address=metadata.get("email"),
                job_id=metadata.get("job_id"),
            )
        return False


class FermoAnalysisManager(BaseModel):
    """Pydantic-based class organizing functionality wrt fermo_core

    Attributes:
        params: user-defined parameters, matching the parameter file by fermo_core.
        upload_path: the upload-path containing user-provided files.
        job_id: The job-specific ID.
        root_url: The root URL of the running fermo_gui instance.

    Raise:
        pydantic.ValidationError: Pydantic validation failed during instantiation.
        Further Errors raised by fermo_core
    """

    params: dict
    upload_path: DirectoryPath
    job_id: str
    root_url: AnyUrl

    def run_manager(self: Self):
        """Run all fermo_core setup, analysis, and teardown steps.

        Also needs error management system.
        """

        # TODO(MMZ 13.2.24): replace placeholder functionality
        sleep(5)
        self.write_results_placeholder()
        self.write_log_placeholder()

    def write_results_placeholder(self):
        """Write results to results-json file"""
        # TODO(MMZ 13.2.24): replace placeholder session data dump
        GeneralManager().store_data_as_json(
            self.upload_path,
            f"{self.job_id}.session.json",
            {"data": "dummy data"},
        )

    def write_log_placeholder(self):
        """Write log of session"""
        # TODO(MMZ 13.2.24): replace placeholder process log dump
        GeneralManager().store_data_as_json(
            self.upload_path,
            f"{self.job_id}.log.json",
            {
                "message_log": [
                    "log step1: this happened first",
                    "log step2: this happened second",
                ]
            },
        )
