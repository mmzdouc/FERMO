"""Class to validate the loaded session file

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
from typing import Any, Self

import jsonschema
from pydantic import BaseModel
from werkzeug.datastructures import FileStorage


class SessionProcessor(BaseModel):
    """Responsible for session file input, storage, validation.

    Attributes:
        task_dir: the upload folder + task ID Path + results
        form: SessionLoadForm object containing the form data
        online: bool to indicate if application is running online (not local)
        maxsize_file: maximum size of file, in bytes in web-version
    """

    task_dir: Path
    form: Any
    online: bool
    maxsize_file: int = 8000000

    def save_file(self: Self, f: FileStorage) -> str:
        """Store the input file securely in user-specific dir

        Arguments:
            f: A Filestorage instance from input form

        Returns:
            The secured filename used for storage
        """
        filename = "out.fermo.session.json"
        f.save(self.task_dir.joinpath(filename))
        return filename

    @staticmethod
    def check_file_size(f: FileStorage, maxsize: int):
        """Check the specified file size

        Arguments:
            f: A Filestorage instance from input form
            maxsize: the maximum allowed file size

        Raises:
            ValueError: file size surpasses maxsize value
        """
        file_size = len(f.read())
        f.seek(0)
        if file_size > maxsize:
            raise ValueError(
                f"File '{f.filename}' is too large (maximum size: '{maxsize}' bytes."
            )

    @staticmethod
    def verify_session_format(filepath: Path):
        """Validate uploaded session file against json schema

        Raises:
            ValueError: invalid session file format
        """
        with open(filepath) as userfile:
            user_input = json.load(userfile)

        with open(Path(__file__).parent.parent.joinpath("schema.json")) as infile:
            schema = json.load(infile)

        try:
            jsonschema.validate(instance=user_input, schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            lines = str(e).splitlines()
            msg = f"{filepath.name}: {lines[0]}"
            raise ValueError(f"Session file has invalid format: '{msg}'") from e

    def process_forms_session(self: Self):
        """Processes the session input form data

        Raises:
            ValueError: session file is empty
        """
        if self.form.session_file.data is None:
            raise ValueError("No FERMO session file was provided.")

        if self.online:
            self.check_file_size(
                f=self.form.session_file.data, maxsize=self.maxsize_file
            )

        f_name = self.save_file(self.form.session_file.data)
        f_path = self.task_dir.joinpath(f_name)

        self.verify_session_format(f_path)

    def run_processor(self: Self):
        """Runs the processor steps"""
        self.process_forms_session()
