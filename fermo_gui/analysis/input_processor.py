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
from typing import Any, Optional, Self

import pandas as pd
from fermo_core.input_output.class_validation_manager import ValidationManager
from pydantic import BaseModel, model_validator
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


class InputProcessor(BaseModel):
    """Responsible for form input processing, file storage, and specific validation.

    Interface between input forms and fermo_core processing

    Attributes:
        task_dir: the upload folder + task ID Path
        form: AnalysisForm object containing the form data
        params: a dict to assemble the parameters.json file
        online: bool to indicate if application is running online (not local)
        n_features: the number of features in the dataframe
        max_features: the maximum allowed number of features in web-version
    """

    task_dir: Path
    form: Any
    online: bool
    params: dict = {}
    n_features: Optional[int] = None
    max_features: int = 1000

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

    def process_form_feature_filtering(self: Self):
        """Processes the feature filtering form (part of peaktable forms)"""
        if self.form.peaktable_filter_toggle.data == "False":
            return

        heights = [
            float(self.form.peaktable_filter_height_lower.data),
            float(self.form.peaktable_filter_height_upper.data),
        ]
        ordered_heights = [min(heights), max(heights)]
        ValidationManager.validate_range_zero_one(ordered_heights)

        areas = [
            float(self.form.peaktable_filter_area_lower.data),
            float(self.form.peaktable_filter_area_upper.data),
        ]
        ordered_areas = [min(areas), max(areas)]
        ValidationManager.validate_range_zero_one(ordered_areas)

        self.check_key_params("additional_modules")
        self.params["additional_modules"]["feature_filtering"] = {
            "activate_module": True,
            "filter_rel_int_range": ordered_heights,
            "filter_rel_area_range": ordered_areas,
        }

    def process_form_peaktable(self: Self):
        """Processes the peaktable input form data if any

        Raises:
            ValueError: peaktable file is empty
            ValueError: too many features in peaktable
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

        df = pd.read_csv(f_path, sep=",")
        if self.online and len(df) > self.max_features:
            raise ValueError(
                f"Peaktable contains too many features (maximum allowed number: "
                f"'{self.max_features}'. Please reduce the number of features or run "
                f"FERMO offline."
            )
        else:
            self.n_features = len(df)

        self.check_key_params("files")
        self.params["files"]["peaktable"] = {
            "filepath": str(f_path.resolve()),
            "format": self.form.peaktable_format.data,
            "polarity": self.form.peaktable_polarity.data,
        }

        self.process_form_feature_filtering()

    def process_form_msms(self: Self):
        """Processes the msms input form data if any"""
        if self.form.msms_file.data is None:
            return

        f_name = self.save_file(self.form.msms_file.data)
        f_path = self.task_dir.joinpath(f_name)

        if self.form.msms_format.data == "mgf":
            ValidationManager.validate_mgf_file(f_path)

        self.params["files"]["msms"] = {
            "filepath": str(f_path.resolve()),
            "format": self.form.msms_format.data,
            "rel_int_from": float(self.form.msms_rel_int_from.data),
        }

    def process_form_phenotype(self: Self):
        """Processes the phenotype input form data if any

        Raises:
            ValueError: format not specified
        """
        if self.form.phenotype_file.data is None:
            return

        f_name = self.save_file(self.form.phenotype_file.data)
        f_path = self.task_dir.joinpath(f_name)

        ValidationManager.validate_csv_file(f_path)
        ValidationManager.validate_csv_has_rows(f_path)
        self.params["files"]["phenotype"] = {
            "filepath": str(f_path.resolve()),
            "format": self.form.phenotype_format.data,
        }

        self.check_key_params("additional_modules")
        self.params["additional_modules"]["phenotype_assignment"] = {}
        if self.form.phenotype_format.data == "":
            raise ValueError("Phenotype 'Format' parameter was not specified.")
        elif self.form.phenotype_format.data == "qualitative":
            ValidationManager.validate_pheno_qualitative(f_path)
            ValidationManager.validate_no_duplicate_entries_csv_column(
                f_path, "sample_name"
            )
            self.params["additional_modules"]["phenotype_assignment"]["qualitative"] = {
                "activate_module": True,
                "factor": int(self.form.phenotype_qualit_factor.data),
                "algorithm": self.form.phenotype_qualit_algorithm.data,
                "value": self.form.phenotype_qualit_value.data,
            }
        elif self.form.phenotype_format.data == "quantitative-percentage":
            ValidationManager.validate_pheno_quant_percentage(f_path)
            ValidationManager.validate_no_duplicate_entries_csv_column(f_path, "well")
            self.params["additional_modules"]["phenotype_assignment"][
                "quantitative-percentage"
            ] = {
                "activate_module": True,
                "sample_avg": self.form.phenotype_quant_average.data,
                "value": self.form.phenotype_quant_value.data,
                "algorithm": self.form.phenotype_quant_algorithm.data,
                "p_val_cutoff": float(self.form.phenotype_quant_p_val.data),
                "coeff_cutoff": float(self.form.phenotype_quant_coeff.data),
            }
        elif self.form.phenotype_format.data == "quantitative-concentration":
            ValidationManager.validate_pheno_quant_concentration(f_path)
            ValidationManager.validate_no_duplicate_entries_csv_column(f_path, "well")
            self.params["additional_modules"]["phenotype_assignment"][
                "quantitative-concentration"
            ] = {
                "activate_module": True,
                "sample_avg": self.form.phenotype_quant_average.data,
                "value": self.form.phenotype_quant_value.data,
                "algorithm": self.form.phenotype_quant_algorithm.data,
                "p_val_cutoff": float(self.form.phenotype_quant_p_val.data),
                "coeff_cutoff": float(self.form.phenotype_quant_coeff.data),
            }

    def run_processor(self: Self):
        """Runs the processor steps"""
        self.process_form_peaktable()
        self.process_form_msms()
        self.process_form_phenotype()
