"""Manages dashboard data loading and filtering functionality

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
from typing import Self, Optional

from pydantic import BaseModel


class DashboardManager(BaseModel):
    """Organizes data extraction and filtering for dashboard

    Attributes:
        stats_analysis: static stats data from general analysis run
        stats_samples_dyn: mixed static and dynamic data on samples (overview)
        retained_features: features remaining after any filter settings were applied
    """

    stats_analysis: dict = {}
    stats_samples_dyn: dict = {}
    retained_features: Optional[set] = None

    def prepare_data_get(self: Self, f_sess: dict):
        """Run methods to prepare the data required by GET method

        Arguments:
            f_sess: fermo session file
        """
        self.extract_stats_analysis(f_sess)
        self.extract_stats_samples_dyn(f_sess)

    def provide_data_get(self: Self) -> dict:
        """Return data required by GET method

        Returns: a json-compatible dict
        """
        return {
            "stats_analysis": self.stats_analysis,
            "stats_samples_dyn": self.stats_samples_dyn,
        }

    def extract_stats_analysis(self: Self, f_sess: dict):
        """Extracts static analysis stats from fermo.session file

        Arguments:
            f_sess: fermo session file
        """
        try:
            self.stats_analysis = {
                "Total Samples": len(f_sess.get("stats", {}).get("samples")),
                "Sample Groups": (len(f_sess.get("stats", {}).get("groups")) - 1),
                "Molecular Features": f_sess.get("stats", {}).get("features"),
                "Removed Mol. Features": len(
                    f_sess.get("stats", {}).get("inactive_features")
                ),
                "FERMO-CORE Version": f_sess.get("metadata", {}).get(
                    "fermo_core_version"
                ),
            }
        except TypeError:
            self.stats_analysis = {"error": "error during parsing of session file"}

    def extract_stats_samples_dyn(self: Self, f_sess: dict):
        """Extracts dynamic stats of samples

        Arguments:
            f_sess: fermo session file
        """
        try:
            for sample in f_sess.get("stats", {}).get("samples"):
                total_features = len(
                    f_sess.get("samples", {}).get(sample, {}).get("feature_ids")
                )

                retained_features = 0
                if self.retained_features is not None:
                    # TODO(MMZ 15.2.24): add filter logic, call method for feature filtering
                    #  use set method to get intersection of total features and features in
                    #  sample
                    pass
                else:
                    retained_features = total_features

                groups = ", ".join(
                    map(str, f_sess.get("samples", {}).get(sample, {}).get("groups"))
                )
                if groups == "":
                    groups = "N/A"

                self.stats_samples_dyn[sample] = {
                    "sample_name": sample,
                    "groups": groups,
                    "total_features": total_features,
                    "retained_features": retained_features,
                }
        except (TypeError, ValueError):
            self.stats_samples_dyn = {"error": "error during parsing of session file"}
