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

from celery import shared_task
from flask_mail import Message

from fermo_gui.analysis.general_manager import GeneralManager
from fermo_gui.config.extensions import mail


@shared_task(ignore_result=False)
def start_fermo_core(job_id: str, upload_path: str):
    """Start fermo_core analysis via FermoAnalysisManager

    Arguments:
        job_id: links input and output of fermo_core
        upload_path: stores input and output

    Returns:
        True if job
    """
    try:
        params = GeneralManager().read_data_from_json(upload_path, f"{job_id}.json")
        manager = FermoAnalysisManager()
        manager.placeholder()
        manager.email_notification_placeholder(params["email"], job_id)
        # TODO(MMZ 12.2.24): Dump the result as job_id.session
        return True
    except Exception as e:
        print(e)
        # TODO(MMZ 12.2.24): add proper error handling; dump the log in the
        #  user-folder for display (as job_id.log)
        return False


class FermoAnalysisManager:
    """Organize logic related to fermo_core processing"""

    # Implement Pydantic-based class?

    @staticmethod
    def placeholder():
        """Placeholder method, replace once fermo_core is available."""
        sleep(10)

    @staticmethod
    def email_notification_placeholder(email: str, job_id: str):
        """Mock email placeholder"""
        msg = Message()
        msg.recipients = [email]
        msg.subject = "Fermo job notification"
        msg.body = (
            "Dear user, \n"
            "your job with the ID \n"
            f"{job_id}\n"
            "has been processed. \n"
            "Please follow this link to see the results: \n"
            f"http://127.0.0.1:5000/results/{job_id}/.\n"
        )
        mail.send(msg)

    def run_manager(self):
        """Run all fermo_core setup, analysis, and teardown steps.

        Also needs error management system.
        """
        pass

    def notify_user(self):
        """If online (email set), perform job notification"""
        pass

    def write_results(self):
        """Write results to results-json file"""
        pass
