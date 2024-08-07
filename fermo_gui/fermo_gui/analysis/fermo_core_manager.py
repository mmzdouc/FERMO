"""Manages functionality to run fermo_core data analysis

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

import logging
from datetime import datetime
from pathlib import Path
from typing import Self

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from fermo_core.input_output.class_file_manager import FileManager
from fermo_core.input_output.class_parameter_manager import ParameterManager
from fermo_core.input_output.class_validation_manager import ValidationManager
from fermo_core.main import main
from pydantic import BaseModel, DirectoryPath

from fermo_gui.analysis.general_manager import GeneralManager


@shared_task(ignore_result=False)
def start_fermo_core_manager(metadata: dict) -> bool:
    """Start fermo_core analysis via FermoAnalysisManager, sends email notification

    Arguments:
        metadata: a dict containing metadata for running of the job

    Returns:
        True if job successful, False if error was raised
    """

    def _write_to_log(msg: str):
        try:
            with open(
                Path(metadata.get("task_path")).joinpath("results/out.fermo.log"), "a"
            ) as file:
                file.write(msg)
        except OSError:
            with open(
                Path(metadata.get("task_path")).joinpath("results/out.fermo.log"), "w"
            ) as file:
                file.write(msg)

    def _send_mail_fail():
        if metadata.get("email_notify"):
            GeneralManager().email_notify_fail(
                root_url=metadata.get("root_url"),
                address=metadata.get("email"),
                job_id=metadata.get("job_id"),
            )

    try:
        manager = FermoCoreManager(
            job_id=metadata.get("job_id"), uploads_dir=metadata.get("task_path")
        )
        manager.run_fermo_core()

        if metadata.get("email_notify"):
            GeneralManager().email_notify_success(
                root_url=metadata.get("root_url"),
                address=metadata.get("email"),
                job_id=metadata.get("job_id"),
            )
        return True
    except SoftTimeLimitExceeded as e:
        _write_to_log(
            f"Job surpassed maximum time limit of '{metadata.get('max_runtime')}' "
            f"seconds: {e}"
        )
        _send_mail_fail()
        return False
    except Exception as e:
        _write_to_log(f"An error occurred: {e}")
        _send_mail_fail()
        return False


class FermoCoreManager(BaseModel):
    """Pydantic-based class to organize methods to call fermo_core analysis methods

    Assumes that the necessary files are in `uploads_dir/job_id/`

    Attributes:
        job_id: The job-specific ID.
        uploads_dir: the path to the respective uploads dir
    """

    job_id: str
    uploads_dir: DirectoryPath

    def create_results_folder(self: Self):
        """Create results folder for the respective run"""
        Path(f"{self.uploads_dir}/results/").mkdir(exist_ok=True)

    def configure_logger(self: Self) -> logging.Logger:
        """Set up logging parameters"""
        logger = logging.getLogger("fermo_core")
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(
            Path(f"{self.uploads_dir}/results/out.fermo.log"),
            mode="w",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

        logger.addHandler(file_handler)

        return logger

    def run_fermo_core(self: Self):
        """Run fermo_core on the respective job id"""
        start_time = datetime.now()
        self.create_results_folder()
        logger = self.configure_logger()
        logger.debug(f"Started 'fermo_core' on job_id '{self.job_id}'.")

        params_input = FileManager.load_json_file(
            f"{self.uploads_dir}/{self.job_id}.parameters.json"
        )
        ValidationManager().validate_file_vs_jsonschema(
            params_input, f"{self.uploads_dir}/{self.job_id}.parameters.json"
        )

        param_manager = ParameterManager()
        param_manager.assign_parameters_cli(params_input)

        main(param_manager, start_time, logger)
