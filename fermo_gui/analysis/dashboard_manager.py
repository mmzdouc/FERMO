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
from typing import Self, Optional, List
from copy import deepcopy

from pydantic import BaseModel


class DashboardManager(BaseModel):
    """Organizes data extraction and filtering for dashboard

    Attributes:
        stats_analysis: static stats data from general analysis run
        stats_samples_dyn: mixed static and dynamic data on samples (overview)
        ret_features: features remaining after any filter settings were applied
    """

    stats_analysis: dict = {}
    stats_samples_dyn: dict = {}
    ret_features: dict = {}

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

                if len(self.ret_features) != 0:
                    remaining_features = self.ret_features["samples"][sample]
                else:
                    remaining_features = total_features

                groups = ", ".join(
                    map(str, f_sess.get("samples", {}).get(sample, {}).get("groups"))
                )
                if groups == "":
                    groups = "N/A"

                self.stats_samples_dyn[sample] = {
                    "sample_name": sample,
                    "groups": groups,
                    "total_features": total_features,
                    "retained_features": remaining_features,
                }
        except (TypeError, ValueError):
            self.stats_samples_dyn = {"error": "error during parsing of session file"}

    def filter_ret_features(self: Self, f_sess: dict, filters: dict):
        """Extracts features and filters them based on filter settings

        Part of the POST functionality (user applies filter on frontend, followed by
        website update).

        Arguments:
            f_sess: fermo session file
            filters: filters set by user on frontend
        """
        self.prepare_ret_features(f_sess)

        for param in filters:
            match param:
                case "rel_intensity":
                    self.filter_spec_feature_range(
                        f_sess, filters[param], "rel_intensity"
                    )
                case "rel_area":
                    self.filter_spec_feature_range(f_sess, filters[param], "rel_area")
                case "filter_feature_id":
                    self.filter_feature_id(filters[param])

        return {
            "samples": {
                sample: list(self.ret_features["samples"][sample])
                for sample in self.ret_features["samples"]
            },
            "total": list(self.ret_features["total"]),
        }

    def prepare_ret_features(self: Self, f_sess: dict):
        """Prepares the ret_features attribute for further filtering

        Arguments:
            f_sess: fermo session file
        """
        self.ret_features = {
            "samples": {
                sample_name: set(f_sess["samples"][sample_name]["feature_ids"])
                for sample_name in f_sess.get("stats", {}).get("samples")
            },
            "total": set(f_sess.get("stats", {}).get("active_features")),
        }

    def filter_spec_feature_range(
        self: Self, f_sess: dict, filt: List[float], param: str
    ):
        """Filters sample-specific features for a parameter with a given range

        Part of the POST functionality (user applies filter on frontend, followed by
        website update).

        Arguments:
            f_sess: fermo session file
            filt: a list with two floats indicating a range
            param: the parameter in the session file to filter for
        """
        if filt[0] == 0.0 and filt[1] == 1.0:
            return
        elif len(self.ret_features["total"]) == 0:
            return
        else:
            for sample in f_sess["samples"]:
                set_sample = deepcopy(self.ret_features["samples"][sample])
                for feature in self.ret_features["samples"][sample]:
                    if not (
                        filt[0]
                        <= f_sess["samples"][sample]["sample_spec_features"][
                            str(feature)
                        ][param]
                        <= filt[1]
                    ):
                        set_sample.discard(feature)
                self.ret_features["samples"][sample] = set_sample

            remainder_in_samples = set().union(
                *[
                    self.ret_features["samples"][sample]
                    for sample in self.ret_features["samples"]
                ]
            )
            self.ret_features["total"].intersection_update(remainder_in_samples)
            return

    def filter_feature_id(self: Self, feature_id: int):
        """Filters for a single feature ID

        Part of the POST functionality (user applies filter on frontend, followed by
        website update).

        Arguments:
            feature_id: a feature identifier integer to filter for
        """
        if len(self.ret_features["total"]) == 0:
            return
        else:
            self.ret_features["total"].intersection_update(
                {
                    feature_id,
                }
            )
            for sample in self.ret_features["samples"]:
                self.ret_features["samples"][sample].intersection_update(
                    {
                        feature_id,
                    }
                )
            return
