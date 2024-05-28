"""Class to process the input forms (storage, validation, processing).

Serves as interface between input forms and fermo_core processing

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

from pathlib import Path
from typing import Any, Self

from fermo_core.input_output.class_validation_manager import ValidationManager
from pydantic import BaseModel
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


class InputProcessor(BaseModel):
    """Responsible for form input processing, file storage, and specific validation.

    Interface between input forms and fermo_core processing

    Attributes:
        task_dir: the upload folder + task ID Path
        form: AnalysisForm object containing the form data
        params: a dict to assemble the parameters.json file
    """

    task_dir: Path
    form: Any
    params: dict = {}

    def return_params(self: Self):
        """Returns the params dict for writing"""
        return self.params

    def save_file(self: Self, f: FileStorage) -> str:
        """Store the input file securely in user-specific dir

        Returns:
            The secured filename used for storage
        """
        filename = secure_filename(f.filename)
        f.save(self.task_dir.joinpath(filename))
        return filename

    def check_key_params(self: Self, key: str):
        if self.params.get(key) is None:
            self.params[key] = {}

    def process_form_peaktable(self: Self):
        """Processes the peaktable input form data if any

        Raises:
            ValueError: peaktable file is empty
        """
        if self.form.peaktable_file.data is None:
            raise ValueError("No peaktable file was provided.")
        f_name = self.save_file(self.form.peaktable_file.data)
        f_path = self.task_dir.joinpath(f_name)

        if self.form.peaktable_format.data == "mzmine3":
            ValidationManager.validate_csv_file(f_path)
            ValidationManager.validate_csv_has_rows(f_path)
            ValidationManager.validate_peaktable_mzmine3(f_path)
            ValidationManager.validate_no_duplicate_entries_csv_column(f_path, "id")

        self.check_key_params("files")
        self.params["files"]["peaktable"] = {
            "filepath": str(f_path.resolve()),
            "format": self.form.peaktable_format.data,
            "polarity": self.form.peaktable_polarity.data,
        }

    def run_processor(self: Self):
        """Runs the processor steps"""
        self.process_form_peaktable()
