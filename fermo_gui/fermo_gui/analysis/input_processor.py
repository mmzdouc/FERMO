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

import os
import zipfile
from pathlib import Path
from typing import Any, Optional, Self

import pandas as pd
import requests
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
        online: bool to indicate if application is running online (not local)
        n_features: the number of features in the dataframe
        max_features: the maximum allowed number of features in web-version
        maxsize_file: the maximum accepted size of files in bytes in web-version
        max_time_module: the maximum runtime per module, in seconds
    """

    task_dir: Path
    form: Any
    online: bool
    params: dict = {}
    n_features: Optional[int] = None
    max_features: int = 3000
    maxsize_file: int = 8000000
    max_time_module: int = 900

    def return_params(self: Self):
        """Returns the params dict for writing"""
        return self.params

    def check_key_in_params(self: Self, key: str):
        """Add key with empty dict if not in self.params"""
        if self.params.get(key) is None:
            self.params[key] = {}

    def save_file(self: Self, f: FileStorage) -> str:
        """Store the input file securely in user-specific dir

        Arguments:
            f: A Filestorage instance from input form

        Returns:
            The secured filename used for storage
        """
        filename = secure_filename(f.filename)
        f.save(self.task_dir.joinpath(filename))
        return filename

    def download_as_job(self: Self) -> Path:
        """Download antiSMASH job from antiSMASH website

        Returns:
            A path to the downloaded dir

        Raises:
            ValueError: could not detect antiSMASH job
        """
        url = (
            f"https://antismash.secondarymetabolites.org/upload"
            f"/{self.form.askcb_jobid.data}/"
        )
        response = requests.get(url)
        html = response.text
        zips = []
        for line in html.split("\n"):
            if ".zip" in line:
                zips.append(line.split('"')[1])

        if len(zips) == 0:
            raise ValueError("antiSMASH JobID not found.")
        else:
            for zip_file in zips:
                response = requests.get(os.path.join(url, zip_file))

                with open(self.task_dir.joinpath(zip_file), "wb") as f:
                    f.write(response.content)

                as_dir = zip_file.split(".")[0]
                with zipfile.ZipFile(self.task_dir.joinpath(zip_file), "r") as zip_ref:
                    zip_ref.extractall(self.task_dir.joinpath(as_dir))

                os.remove(self.task_dir.joinpath(zip_file))

                return self.task_dir.joinpath(as_dir)

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

    def verify_max_features(self: Self, peaktable_path: Path):
        """Verify that the number of features does not surpass a certain maximum

        Arguments:
            peaktable_path: the path to the peaktable to check

        Raises:
            ValueError: too many features in peaktable (> self.max_features)
        """
        df = pd.read_csv(peaktable_path, sep=",")
        if len(df) > self.max_features:
            raise ValueError(
                f"Peaktable contains too many features (maximum allowed number: "
                f"'{self.max_features}'. Please reduce the number of features or run "
                f"FERMO as offline version."
            )
        else:
            self.n_features = len(df)

    def verify_peaktable_format(self: Self, filepath: Path):
        """Verify that peaktable format is correct

        Raises:
            ValueError: Unsupported peaktable format
        """
        if self.form.peaktable_format.data == "mzmine3":
            ValidationManager.validate_csv_file(filepath)
            ValidationManager.validate_csv_has_rows(filepath)
            ValidationManager.validate_peaktable_mzmine3(filepath)
            ValidationManager.validate_no_duplicate_entries_csv_column(filepath, "id")
        else:
            raise ValueError(
                f"Unsupported peaktable format: '{self.form.peaktable_format.data}'"
            )

        if self.online:
            self.verify_max_features(peaktable_path=filepath)

    def verify_msms_format(self: Self, filepath: Path):
        """Verify that msms format is correct

        Raises:
            ValueError: Unsupported msms format
        """
        if self.form.msms_format.data == "mgf":
            ValidationManager.validate_mgf_file(filepath)
        else:
            raise ValueError(f"Unsupported msms format: '{self.form.msms_format.data}'")

    def verify_phenotype_format(self: Self, filepath: Path):
        """Verify that phenotype format is correct

        Raises:
            ValueError: Empty phenotype format
            ValueError: Unsupported phenotype format
        """
        if self.form.phenotype_format.data == "":
            raise ValueError(f"Phenotype format left empty: specify the format")

        ValidationManager.validate_csv_file(filepath)
        ValidationManager.validate_csv_has_rows(filepath)

        if self.form.phenotype_format.data == "qualitative":
            ValidationManager.validate_pheno_qualitative(filepath)
            ValidationManager.validate_no_duplicate_entries_csv_column(
                filepath, "sample_name"
            )
        elif self.form.phenotype_format.data == "quantitative-percentage":
            ValidationManager.validate_pheno_quant_percentage(filepath)
            ValidationManager.validate_no_duplicate_entries_csv_column(filepath, "well")
        elif self.form.phenotype_format.data == "quantitative-concentration":
            ValidationManager.validate_pheno_quant_concentration(filepath)
            ValidationManager.validate_no_duplicate_entries_csv_column(filepath, "well")
        else:
            raise ValueError(
                f"Unsupported phenotype format: '{self.form.phenotype_format.data}'"
            )

    def verify_group_format(self: Self, filepath: Path):
        """Verify that group metadata format is correct

        Raises:
            ValueError: Unsupported group metadata format
        """
        if self.form.group_format.data == "fermo":
            ValidationManager.validate_csv_file(filepath)
            ValidationManager.validate_csv_has_rows(filepath)
            ValidationManager.validate_group_metadata_fermo(filepath)
            ValidationManager.validate_no_duplicate_entries_csv_column(
                filepath, "sample_name"
            )
        else:
            raise ValueError(
                f"Unsupported group metadata format: '{self.form.group_format.data}'"
            )

    def verify_library_format(self: Self, filepath: Path):
        """Verify that library format is correct

        Raises:
            ValueError: Unsupported library format
        """
        if self.form.library_format.data == "mgf":
            ValidationManager.validate_mgf_file(filepath)
        else:
            raise ValueError(
                f"Unsupported library format: '{self.form.library_format.data}'"
            )

    def process_forms_peaktable(self: Self):
        """Processes the peaktable input form data if any

        Raises:
            ValueError: peaktable file is empty
        """
        if self.form.peaktable_file.data is None:
            raise ValueError("No peaktable file was provided.")

        if self.online:
            self.check_file_size(
                f=self.form.peaktable_file.data, maxsize=self.maxsize_file
            )

        f_name = self.save_file(self.form.peaktable_file.data)
        f_path = self.task_dir.joinpath(f_name)

        self.verify_peaktable_format(f_path)

        self.check_key_in_params("files")
        self.params["files"]["peaktable"] = {
            "filepath": str(f_path.resolve()),
            "format": str(self.form.peaktable_format.data),
            "polarity": str(self.form.peaktable_polarity.data),
        }

        self.check_key_in_params("core_modules")
        self.params["core_modules"]["adduct_annotation"] = {
            "activate_module": self.form.peaktable_adduct_toggle.data,
            "mass_dev_ppm": float(self.form.peaktable_ppm.data),
        }

        if self.form.peaktable_filter_toggle.data:
            self.check_key_in_params("additional_modules")
            self.params["additional_modules"]["feature_filtering"] = {
                "activate_module": True,
                "filter_rel_int_range_min": float(
                    self.form.peaktable_filter_height_lower.data
                ),
                "filter_rel_int_range_max": float(
                    self.form.peaktable_filter_height_upper.data
                ),
                "filter_rel_area_range_min": float(
                    self.form.peaktable_filter_area_lower.data
                ),
                "filter_rel_area_range_max": float(
                    self.form.peaktable_filter_area_upper.data
                ),
            }

    def process_forms_msms(self: Self):
        """Processes the msms input form data if any"""
        if self.form.msms_file.data is None:
            return

        if self.online:
            self.check_file_size(f=self.form.msms_file.data, maxsize=self.maxsize_file)

        f_name = self.save_file(self.form.msms_file.data)
        f_path = self.task_dir.joinpath(f_name)

        self.verify_msms_format(filepath=f_path)

        self.params["files"]["msms"] = {
            "filepath": str(f_path.resolve()),
            "format": str(self.form.msms_format.data),
        }

        if self.form.msms_filter_toggle.data:
            self.params["files"]["msms"]["rel_int_from"] = float(
                self.form.msms_rel_int_from.data
            )
        else:
            self.params["files"]["msms"]["rel_int_from"] = 0.0

        self.check_key_in_params("core_modules")
        self.params["core_modules"]["fragment_annotation"] = {
            "activate_module": self.form.msms_fragment_toggle.data,
            "mass_dev_ppm": float(self.form.peaktable_ppm.data),
        }
        self.params["core_modules"]["neutral_loss_annotation"] = {
            "activate_module": self.form.msms_loss_toggle.data,
            "mass_dev_ppm": float(self.form.peaktable_ppm.data),
        }

        self.params["core_modules"]["spec_sim_networking"] = {}
        self.params["core_modules"]["spec_sim_networking"]["modified_cosine"] = {
            "activate_module": self.form.msms_cosine_toggle.data,
            "msms_min_frag_nr": int(self.form.msms_cosine_minfrag.data),
            "fragment_tol": float(self.form.msms_cosine_tolerance.data),
            "score_cutoff": float(self.form.msms_cosine_score.data),
            "max_nr_links": int(self.form.msms_cosine_links.data),
            "maximum_runtime": (self.max_time_module if self.online else 0),
        }
        self.params["core_modules"]["spec_sim_networking"]["ms2deepscore"] = {
            "activate_module": self.form.msms_deepscore_toggle.data,
            "msms_min_frag_nr": int(self.form.msms_deepscore_minfrag.data),
            "score_cutoff": float(self.form.msms_deepscore_score.data),
            "max_nr_links": int(self.form.msms_deepscore_links.data),
            "maximum_runtime": (self.max_time_module if self.online else 0),
        }

    def process_forms_phenotype(self: Self):
        """Processes the phenotype input form data if any

        Raises:
            ValueError: format not specified
        """
        if self.form.phenotype_file.data is None:
            return

        if self.online:
            self.check_file_size(
                f=self.form.phenotype_file.data, maxsize=self.maxsize_file
            )

        f_name = self.save_file(self.form.phenotype_file.data)
        f_path = self.task_dir.joinpath(f_name)

        self.verify_phenotype_format(f_path)

        self.params["files"]["phenotype"] = {
            "filepath": str(f_path.resolve()),
            "format": str(self.form.phenotype_format.data),
        }

        self.check_key_in_params("additional_modules")
        self.params["additional_modules"]["phenotype_assignment"] = {}
        if self.form.phenotype_format.data == "qualitative":
            self.params["additional_modules"]["phenotype_assignment"]["qualitative"] = {
                "activate_module": True,
                "factor": int(self.form.phenotype_qualit_factor.data),
                "algorithm": str(self.form.phenotype_qualit_algorithm.data),
                "value": str(self.form.phenotype_qualit_value.data),
            }
        elif self.form.phenotype_format.data == "quantitative-percentage":
            self.params["additional_modules"]["phenotype_assignment"][
                "quantitative-percentage"
            ] = {
                "activate_module": True,
                "sample_avg": str(self.form.phenotype_quant_average_perc.data),
                "value": str(self.form.phenotype_quant_value_perc.data),
                "algorithm": str(self.form.phenotype_quant_algorithm_perc.data),
                "p_val_cutoff": float(self.form.phenotype_quant_p_val_perc.data),
                "coeff_cutoff": float(self.form.phenotype_quant_coeff_perc.data),
            }
        elif self.form.phenotype_format.data == "quantitative-concentration":
            self.params["additional_modules"]["phenotype_assignment"][
                "quantitative-concentration"
            ] = {
                "activate_module": True,
                "sample_avg": str(self.form.phenotype_quant_average_conc.data),
                "value": str(self.form.phenotype_quant_value_conc.data),
                "algorithm": str(self.form.phenotype_quant_algorithm_conc.data),
                "p_val_cutoff": float(self.form.phenotype_quant_p_val_conc.data),
                "coeff_cutoff": float(self.form.phenotype_quant_coeff_conc.data),
            }

    def process_forms_group(self: Self):
        """Processes the group metadata input form data if any"""
        if self.form.group_file.data is None:
            return

        if self.online:
            self.check_file_size(f=self.form.group_file.data, maxsize=self.maxsize_file)

        f_name = self.save_file(self.form.group_file.data)
        f_path = self.task_dir.joinpath(f_name)

        self.verify_group_format(f_path)

        self.params["files"]["group_metadata"] = {
            "filepath": str(f_path.resolve()),
            "format": str(self.form.group_format.data),
        }

        self.check_key_in_params("additional_modules")
        self.params["additional_modules"]["blank_assignment"] = {
            "activate_module": self.form.group_blank_toggle.data,
            "factor": int(self.form.group_blank_factor.data),
            "algorithm": str(self.form.group_blank_algorithm.data),
            "value": str(self.form.group_blank_value.data),
        }
        self.params["additional_modules"]["group_factor_assignment"] = {
            "activate_module": self.form.group_factor_toggle.data,
            "algorithm": str(self.form.group_factor_algorithm.data),
            "value": str(self.form.group_factor_value.data),
        }

    def process_forms_library(self: Self):
        """Processes the library input form data if any"""
        if self.form.library_file.data is None:
            return

        if self.online:
            self.check_file_size(
                f=self.form.library_file.data, maxsize=self.maxsize_file
            )

        f_name = self.save_file(self.form.library_file.data)
        f_path = self.task_dir.joinpath(f_name)

        self.verify_library_format(f_path)

        self.params["files"]["spectral_library"] = {
            "filepath": str(f_path.resolve()),
            "format": str(self.form.library_format.data),
        }

        self.check_key_in_params("additional_modules")
        self.params["additional_modules"]["spectral_library_matching"] = {}
        self.params["additional_modules"]["spectral_library_matching"][
            "modified_cosine"
        ] = {
            "activate_module": self.form.library_cosine_toggle.data,
            "fragment_tol": float(self.form.library_cosine_tolerance.data),
            "min_nr_matched_peaks": int(self.form.library_cosine_matches.data),
            "score_cutoff": float(self.form.library_cosine_score.data),
            "max_precursor_mass_diff": int(self.form.library_cosine_mzdiff.data),
            "maximum_runtime": (self.max_time_module if self.online else 0),
        }
        self.params["additional_modules"]["spectral_library_matching"][
            "ms2deepscore"
        ] = {
            "activate_module": self.form.library_deepscore_toggle.data,
            "score_cutoff": float(self.form.library_deepscore_score.data),
            "max_precursor_mass_diff": int(self.form.library_deepscore_mzdiff.data),
            "maximum_runtime": (self.max_time_module if self.online else 0),
        }

    def process_forms_ms2query(self: Self):
        """Processes the ms2query input form data if any"""
        if self.form.ms2query_file.data is not None:
            if self.online:
                self.check_file_size(
                    f=self.form.ms2query_file.data, maxsize=self.maxsize_file
                )
            f_name = self.save_file(self.form.ms2query_file.data)
            f_path = self.task_dir.joinpath(f_name)
            ValidationManager.validate_csv_has_rows(f_path)
            ValidationManager.validate_ms2query_results(f_path)
            self.params["files"]["ms2query_results"] = {
                "filepath": str(f_path.resolve()),
                "score_cutoff": float(self.form.ms2query_score.data),
            }

    def process_forms_askcb(self: Self):
        """Processes the antismash input form data if any

        Raises:
            ValueError: antiSMASH JobID not found
        """
        if len(self.form.askcb_jobid.data) < 1:
            return

        dir_as = self.download_as_job()

        self.params["files"]["as_results"] = {
            "directory_path": str(self.task_dir.joinpath(dir_as).resolve()),
            "similarity_cutoff": float(self.form.askcb_score.data),
        }

        self.check_key_in_params("additional_modules")
        self.params["additional_modules"]["as_kcb_matching"] = {}
        self.params["additional_modules"]["as_kcb_matching"]["modified_cosine"] = {
            "activate_module": self.form.askcb_cosine_toggle.data,
            "fragment_tol": float(self.form.askcb_cosine_tolerance.data),
            "min_nr_matched_peaks": int(self.form.askcb_cosine_matches.data),
            "score_cutoff": float(self.form.askcb_cosine_score.data),
            "max_precursor_mass_diff": int(self.form.askcb_cosine_mzdiff.data),
            "maximum_runtime": (self.max_time_module if self.online else 0),
        }
        self.params["additional_modules"]["as_kcb_matching"]["ms2deepscore"] = {
            "activate_module": self.form.askcb_deepscore_toggle.data,
            "score_cutoff": float(self.form.askcb_deepscore_score.data),
            "max_precursor_mass_diff": int(self.form.askcb_deepscore_mzdiff.data),
            "maximum_runtime": (self.max_time_module if self.online else 0),
        }

    def run_processor(self: Self):
        """Runs the processor steps"""
        self.process_forms_peaktable()
        self.process_forms_msms()
        self.process_forms_phenotype()
        self.process_forms_group()
        self.process_forms_library()
        self.process_forms_ms2query()
        self.process_forms_askcb()
