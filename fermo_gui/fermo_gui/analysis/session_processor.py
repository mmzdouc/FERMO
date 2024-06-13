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

    @staticmethod
    def create_params_json(sess_path: Path):
        """Create a parameters.json file from session.json

        Arguments:
            sess_path: a Path pointing towards the session file
        """
        with open(sess_path) as userfile:
            sess = json.load(userfile)

        params = {
            "files": {},
            "core_modules": {"spec_sim_networking": {}},
            "additional_modules": {
                "phenotype_assignment": {},
                "spectral_library_matching": {},
                "as_kcb_matching": {},
            },
        }

        if sess.get("parameters", {}).get("PeaktableParameters") is not None:
            params["files"]["peaktable"] = {
                "format": sess["parameters"]["PeaktableParameters"].get(
                    "format", "mzmine3"
                ),
                "polarity": sess["parameters"]["PeaktableParameters"].get(
                    "polarity", "positive"
                ),
            }

        if sess.get("parameters", {}).get("MsmsParameters") is not None:
            params["files"]["msms"] = {
                "format": sess["parameters"]["MsmsParameters"].get("format", "mgf"),
                "rel_int_from": sess["parameters"]["MsmsParameters"].get(
                    "polarity", 0.01
                ),
            }

        if sess.get("parameters", {}).get("MS2QueryResultsParameters") is not None:
            params["files"]["ms2query_results"] = {
                "score_cutoff": sess["parameters"]["MS2QueryResultsParameters"].get(
                    "score_cutoff", 0.7
                ),
            }

        if sess.get("parameters", {}).get("AsResultsParameters") is not None:
            params["files"]["ms2query_results"] = {
                "similarity_cutoff": sess["parameters"]["AsResultsParameters"].get(
                    "similarity_cutoff", 0.7
                ),
            }

        if (
            sess.get("parameters", {})
            .get("AdductAnnotationParameters", {})
            .get("activate_module", False)
        ):
            params["core_modules"]["adduct_annotation"] = {
                "activate_module": True,
                "mass_dev_ppm": sess.get("parameters", {})
                .get("AdductAnnotationParameters", {})
                .get("mass_dev_ppm"),
            }

        if (
            sess.get("parameters", {})
            .get("NeutralLossParameters", {})
            .get("activate_module", False)
        ):
            params["core_modules"]["neutral_loss_annotation"] = {
                "activate_module": True,
                "mass_dev_ppm": sess.get("parameters", {})
                .get("NeutralLossParameters", {})
                .get("mass_dev_ppm"),
            }

        if (
            sess.get("parameters", {})
            .get("FragmentAnnParameters", {})
            .get("activate_module", False)
        ):
            params["core_modules"]["fragment_annotation"] = {
                "activate_module": True,
                "mass_dev_ppm": sess.get("parameters", {})
                .get("FragmentAnnParameters", {})
                .get("mass_dev_ppm"),
            }

        if (
            sess.get("parameters", {})
            .get("SpecSimNetworkCosineParameters", {})
            .get("activate_module", False)
        ):
            params["core_modules"]["spec_sim_networking"]["modified_cosine"] = {
                "activate_module": True,
                "msms_min_frag_nr": sess.get("parameters", {})
                .get("SpecSimNetworkCosineParameters", {})
                .get("msms_min_frag_nr", 5),
                "fragment_tol": sess.get("parameters", {})
                .get("SpecSimNetworkCosineParameters", {})
                .get("fragment_tol", 0.1),
                "score_cutoff": sess.get("parameters", {})
                .get("SpecSimNetworkCosineParameters", {})
                .get("score_cutoff", 0.7),
                "max_nr_links": sess.get("parameters", {})
                .get("SpecSimNetworkCosineParameters", {})
                .get("max_nr_links", 10),
            }

        if (
            sess.get("parameters", {})
            .get("SpecSimNetworkDeepscoreParameters", {})
            .get("activate_module", False)
        ):
            params["core_modules"]["spec_sim_networking"]["ms2deepscore"] = {
                "activate_module": True,
                "score_cutoff": sess.get("parameters", {})
                .get("SpecSimNetworkDeepscoreParameters", {})
                .get("score_cutoff", 0.8),
                "max_nr_links": sess.get("parameters", {})
                .get("SpecSimNetworkDeepscoreParameters", {})
                .get("max_nr_links", 10),
                "msms_min_frag_nr": sess.get("parameters", {})
                .get("SpecSimNetworkDeepscoreParameters", {})
                .get("msms_min_frag_nr", 5),
            }

        if (
            sess.get("parameters", {})
            .get("FeatureFilteringParameters", {})
            .get("activate_module", False)
        ):
            params["additional_modules"]["feature_filtering"] = {
                "activate_module": True,
                "filter_rel_int_range_min": sess.get("parameters", {})
                .get("FeatureFilteringParameters", {})
                .get("filter_rel_int_range_min", 0.0),
                "filter_rel_int_range_max": sess.get("parameters", {})
                .get("FeatureFilteringParameters", {})
                .get("filter_rel_int_range_max", 1.0),
                "filter_rel_area_range_min": sess.get("parameters", {})
                .get("FeatureFilteringParameters", {})
                .get("filter_rel_area_range_min", 0.0),
                "filter_rel_area_range_max": sess.get("parameters", {})
                .get("FeatureFilteringParameters", {})
                .get("filter_rel_area_range_max", 1.0),
            }

        if (
            sess.get("parameters", {})
            .get("BlankAssignmentParameters", {})
            .get("activate_module", False)
        ):
            params["additional_modules"]["blank_assignment"] = {
                "activate_module": True,
                "factor": sess.get("parameters", {})
                .get("BlankAssignmentParameters", {})
                .get("factor", 10),
                "algorithm": sess.get("parameters", {})
                .get("BlankAssignmentParameters", {})
                .get("algorithm", "mean"),
                "value": sess.get("parameters", {})
                .get("BlankAssignmentParameters", {})
                .get("value", "area"),
            }

        if (
            sess.get("parameters", {})
            .get("GroupFactAssignmentParameters", {})
            .get("activate_module", False)
        ):
            params["additional_modules"]["group_factor_assignment"] = {
                "activate_module": True,
                "algorithm": sess.get("parameters", {})
                .get("GroupFactAssignmentParameters", {})
                .get("algorithm", "mean"),
                "value": sess.get("parameters", {})
                .get("GroupFactAssignmentParameters", {})
                .get("value", "area"),
            }

        if (
            sess.get("parameters", {})
            .get("PhenoQualAssgnParams", {})
            .get("activate_module", False)
        ):
            params["additional_modules"]["phenotype_assignment"]["qualitative"] = {
                "activate_module": True,
                "factor": sess.get("parameters", {})
                .get("PhenoQualAssgnParams", {})
                .get("factor", 10),
                "algorithm": sess.get("parameters", {})
                .get("PhenoQualAssgnParams", {})
                .get("algorithm", "minmax"),
                "value": sess.get("parameters", {})
                .get("PhenoQualAssgnParams", {})
                .get("value", "area"),
            }

        if (
            sess.get("parameters", {})
            .get("PhenoQuantPercentAssgnParams", {})
            .get("activate_module", False)
        ):
            params["additional_modules"]["phenotype_assignment"][
                "quantitative-percentage"
            ] = {
                "activate_module": True,
                "sample_avg": sess.get("parameters", {})
                .get("PhenoQuantPercentAssgnParams", {})
                .get("sample_avg", "mean"),
                "value": sess.get("parameters", {})
                .get("PhenoQuantPercentAssgnParams", {})
                .get("value", "area"),
                "algorithm": sess.get("parameters", {})
                .get("PhenoQuantPercentAssgnParams", {})
                .get("algorithm", "pearson"),
                "p_val_cutoff": sess.get("parameters", {})
                .get("PhenoQuantPercentAssgnParams", {})
                .get("p_val_cutoff", 0.05),
                "coeff_cutoff": sess.get("parameters", {})
                .get("PhenoQuantPercentAssgnParams", {})
                .get("coeff_cutoff", 0.7),
            }

        if (
            sess.get("parameters", {})
            .get("PhenoQuantConcAssgnParams", {})
            .get("activate_module", False)
        ):
            params["additional_modules"]["phenotype_assignment"][
                "quantitative-concentration"
            ] = {
                "activate_module": True,
                "sample_avg": sess.get("parameters", {})
                .get("PhenoQuantConcAssgnParams", {})
                .get("sample_avg", "mean"),
                "value": sess.get("parameters", {})
                .get("PhenoQuantConcAssgnParams", {})
                .get("value", "area"),
                "algorithm": sess.get("parameters", {})
                .get("PhenoQuantConcAssgnParams", {})
                .get("algorithm", "pearson"),
                "p_val_cutoff": sess.get("parameters", {})
                .get("PhenoQuantConcAssgnParams", {})
                .get("p_val_cutoff", 0.05),
                "coeff_cutoff": sess.get("parameters", {})
                .get("PhenoQuantConcAssgnParams", {})
                .get("coeff_cutoff", 0.7),
            }

        if (
            sess.get("parameters", {})
            .get("SpectralLibMatchingCosineParameters", {})
            .get("activate_module", False)
        ):
            params["additional_modules"]["spectral_library_matching"][
                "modified_cosine"
            ] = {
                "activate_module": True,
                "fragment_tol": sess.get("parameters", {})
                .get("SpectralLibMatchingCosineParameters", {})
                .get("fragment_tol", 0.1),
                "min_nr_matched_peaks": sess.get("parameters", {})
                .get("SpectralLibMatchingCosineParameters", {})
                .get("min_nr_matched_peaks", 5),
                "score_cutoff": sess.get("parameters", {})
                .get("SpectralLibMatchingCosineParameters", {})
                .get("score_cutoff", 0.7),
                "max_precursor_mass_diff": sess.get("parameters", {})
                .get("SpectralLibMatchingCosineParameters", {})
                .get("max_precursor_mass_diff", 600),
            }

        if (
            sess.get("parameters", {})
            .get("SpectralLibMatchingDeepscoreParameters", {})
            .get("activate_module", False)
        ):
            params["additional_modules"]["spectral_library_matching"][
                "ms2deepscore"
            ] = {
                "activate_module": True,
                "score_cutoff": sess.get("parameters", {})
                .get("SpectralLibMatchingDeepscoreParameters", {})
                .get("score_cutoff", 0.8),
                "max_precursor_mass_diff": sess.get("parameters", {})
                .get("SpectralLibMatchingDeepscoreParameters", {})
                .get("max_precursor_mass_diff", 600),
            }

        if (
            sess.get("parameters", {})
            .get("Ms2QueryAnnotationParameters", {})
            .get("activate_module", False)
        ):
            params["additional_modules"]["ms2query_annotation"] = {
                "activate_module": True,
                "score_cutoff": sess.get("parameters", {})
                .get("Ms2QueryAnnotationParameters", {})
                .get("score_cutoff", 0.7),
            }

        if (
            sess.get("parameters", {})
            .get("AsKcbCosineMatchingParams", {})
            .get("activate_module", False)
        ):
            params["additional_modules"]["as_kcb_matching"]["modified_cosine"] = {
                "activate_module": True,
                "fragment_tol": sess.get("parameters", {})
                .get("AsKcbCosineMatchingParams", {})
                .get("fragment_tol", 0.1),
                "min_nr_matched_peaks": sess.get("parameters", {})
                .get("AsKcbCosineMatchingParams", {})
                .get("min_nr_matched_peaks", 5),
                "score_cutoff": sess.get("parameters", {})
                .get("AsKcbCosineMatchingParams", {})
                .get("score_cutoff", 0.7),
                "max_precursor_mass_diff": sess.get("parameters", {})
                .get("AsKcbCosineMatchingParams", {})
                .get("max_precursor_mass_diff", 600),
            }

        if (
            sess.get("parameters", {})
            .get("AsKcbDeepscoreMatchingParams", {})
            .get("activate_module", False)
        ):
            params["additional_modules"]["as_kcb_matching"]["ms2deepscore"] = {
                "activate_module": True,
                "score_cutoff": sess.get("parameters", {})
                .get("AsKcbDeepscoreMatchingParams", {})
                .get("score_cutoff", 0.8),
                "max_precursor_mass_diff": sess.get("parameters", {})
                .get("AsKcbDeepscoreMatchingParams", {})
                .get("max_precursor_mass_diff", 600),
            }

        params = {key: value for key, value in params.items() if len(value) > 0}

        job_id = sess_path.parent.parent.name
        params_path = sess_path.parent.parent.joinpath(f"{job_id}.parameters.json")

        with open(params_path, "w") as outfile:
            json.dump(params, outfile, indent=2)

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

        self.create_params_json(f_path)

    def run_processor(self: Self):
        """Runs the processor steps"""
        self.process_forms_session()
