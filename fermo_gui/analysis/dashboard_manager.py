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
from typing import Self, List
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
    stats_samples_dyn: list = []
    stats_chromatogram: dict = {}
    ret_features: dict = {}

    def prepare_data_get(self: Self, f_sess: dict):
        """Run methods to prepare the data required by GET method

        Arguments:
            f_sess: fermo session file
        """
        self.extract_stats_analysis(f_sess)
        self.extract_stats_samples_dyn(f_sess)
        self.create_chromatogram(f_sess)

    def provide_data_get(self: Self) -> dict:
        """Return data required by GET method

        Returns: a json-compatible dict
        """
        return {
            "stats_analysis": self.stats_analysis,
            "stats_samples_dyn": self.stats_samples_dyn,
            "stats_chromatogram": self.stats_chromatogram,
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
            groups = f_sess.get("stats", {}).get("groups", {}).get("categories", {})

            # TODO: handle no input metadata
            if groups == "":
                groups = "N/A"

            group_list = []
            sample_to_group = {}

            for group_id, categories in groups.items():
                group_list.append(group_id.title())
                for category, details in categories.items():
                    for s_id in details["s_ids"]:
                        if s_id in sample_to_group:
                            sample_to_group[s_id].update({group_id.title(): category})
                        else:
                            sample_to_group[s_id] = {group_id.title(): category}

            for sample in f_sess.get("stats", {}).get("samples"):
                total_features = len(
                    f_sess.get("samples", {}).get(sample, {}).get("feature_ids")
                )
                if len(self.ret_features) != 0:
                    remaining_features = self.ret_features["samples"][sample]
                else:
                    remaining_features = total_features

                group_info = sample_to_group.get(sample, {})
                if len(group_info.keys()) != len(group_list):
                    for item in group_list:
                        if item not in group_info:
                            group_info[item] = "N/A"
                ordered_group_info = {
                    key: group_info.get(key, "N/A") for key in group_list
                }

                self.stats_samples_dyn.append(
                    {
                        "Sample name": sample,
                        "Total features": total_features,
                        "Retained features": remaining_features,
                        **ordered_group_info,
                    }
                )
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
                case "abs_intensity":
                    self.filter_spec_feature_range(f_sess, filters[param], "intensity")
                case "rel_area":
                    self.filter_spec_feature_range(f_sess, filters[param], "rel_area")
                case "abs_area":
                    self.filter_spec_feature_range(f_sess, filters[param], "area")
                # TODO(MM 16.2.24): implement peak_overlap range (sample_spec)
                # TODO(MM 16.2.24): implement novelty_score range (feature_spec)
                # TODO(MM 16.2.24): implement blank_assoc (feature_spec)
                # TODO(MM 16.2.24): implement quant_data_assoc (feature_spec)
                # TODO(MM 16.2.24): implement annotation (feature_spec)
                case "feature_id":
                    self.filter_feature_id(filters[param])
                case "network_id":
                    self.filter_network_id(f_sess, filters[param])
                case "groups_feature":
                    self.filter_groups_feature(f_sess, filters[param])
                case "groups_network":
                    self.filter_groups_network(f_sess, filters[param])
                case "nr_samples":
                    self.filter_nr_samples(f_sess, filters[param])
                case "precursor_mz":
                    self.filter_gen_feature_range(f_sess, filters[param], "mz")
                # TODO(MM 16.2.24): implement fold_include
                # TODO(MM 16.2.24): implement fold_exclude

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
            filt: a list of two numbers indicating a range
            param: the parameter in the session file to filter for
        """
        filt = [min(filt), max(filt)]

        if float(filt[0]) == 0.0 and float(filt[1]) == 1.0:
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

    def filter_gen_feature_range(
        self: Self, f_sess: dict, filt: List[float], param: str
    ):
        """Filters general features for a parameter with a given range

        Part of the POST functionality (user applies filter on frontend, followed by
        website update).

        Arguments:
            f_sess: fermo session file
            filt: a list of two numbers indicating a range
            param: the parameter in the session file to filter for
        """
        filt = [min(filt), max(filt)]

        if float(filt[0]) == 0.0 and float(filt[1]) == 1.0:
            return
        elif len(self.ret_features["total"]) == 0:
            return
        else:
            set_total = deepcopy(self.ret_features["total"])
            for feature in self.ret_features["total"]:
                if not (
                    filt[0]
                    <= f_sess["general_features"][str(feature)][param]
                    <= filt[1]
                ):
                    set_total.discard(feature)
            self.ret_features["total"] = set_total

            for sample in self.ret_features["samples"]:
                self.ret_features["samples"][sample].intersection_update(set_total)
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

    def filter_nr_samples(self: Self, f_sess: dict, filt: dict):
        """Filters for features observed in a specified number of samples

        Part of the POST functionality (user applies filter on frontend, followed by
        website update).

        Arguments:
            f_sess: fermo session file
            filt: a dict indicating an optional minimum and/or maximum of samples
        """
        if len(self.ret_features["total"]) == 0:
            return

        if (
            filt.get("minimum") is not None
            and filt.get("maximum") is not None
            and filt.get("minimum") > 0
            and filt.get("maximum") > 0
        ):
            mode = "range"
        elif filt.get("minimum") is not None and filt.get("minimum") > 0:
            mode = "greater_equal"
        elif filt.get("maximum") is not None and filt.get("maximum") > 0:
            mode = "less_equal"
        else:
            return

        set_total = deepcopy(self.ret_features["total"])
        for feature in self.ret_features["total"]:
            match mode:
                case "range":
                    if not (
                        filt["minimum"]
                        <= len(f_sess["general_features"][str(feature)]["samples"])
                        <= filt["maximum"]
                    ):
                        set_total.discard(feature)
                case "greater_equal":
                    if not (
                        filt["minimum"]
                        <= len(f_sess["general_features"][str(feature)]["samples"])
                    ):
                        set_total.discard(feature)
                case "less_equal":
                    if not (
                        len(f_sess["general_features"][str(feature)]["samples"])
                        <= filt["maximum"]
                    ):
                        set_total.discard(feature)

        self.ret_features["total"] = set_total
        for sample in self.ret_features["samples"]:
            self.ret_features["samples"][sample].intersection_update(set_total)
        return

    def filter_network_id(self: Self, f_sess: dict, filt: dict):
        """Filters for features observed in a specified spectrum similarity network

        Part of the POST functionality (user applies filter on frontend, followed by
        website update).

        Arguments:
            f_sess: fermo session file
            filt: a dict indicating the network algorithm and ID
        """
        if len(self.ret_features["total"]) == 0:
            return
        try:
            set_total = deepcopy(self.ret_features["total"])
            set_total.intersection_update(
                set(
                    f_sess["stats"]["networks"][filt["algorithm"]]["summary"][
                        str(filt["n_id"])
                    ]
                )
            )
            self.ret_features["total"] = set_total
            for sample in self.ret_features["samples"]:
                self.ret_features["samples"][sample].intersection_update(set_total)
            return
        except (KeyError, TypeError):
            return

    def filter_groups_feature(self: Self, f_sess: dict, filt: str):
        """Filters for features observed in a specified group if groups were specified

        Part of the POST functionality (user applies filter on frontend, followed by
        website update).

        Arguments:
            f_sess: fermo session file
            filt: a string indicating the group to filter for
        """
        if len(self.ret_features["total"]) == 0:
            return
        elif len(f_sess["stats"]["groups"]) == 1:
            return
        elif filt not in f_sess["stats"]["groups"]:
            return
        else:
            retained_set = set()
            for sample in f_sess["samples"]:
                if filt in f_sess["samples"][sample]["groups"]:
                    retained_set.update(set(f_sess["samples"][sample]["feature_ids"]))

            self.ret_features["total"].intersection_update(retained_set)
            for sample in self.ret_features["samples"]:
                self.ret_features["samples"][sample].intersection_update(retained_set)
            return

    def filter_groups_network(self: Self, f_sess: dict, filt: dict):
        """Filters for features in all networks that the groups contributed to.

        Only applicable if groups were specified.
        Part of the POST functionality (user applies filter on frontend, followed by
        website update).

        Arguments:
            f_sess: fermo session file
            filt: a dict with group and network algorithm information
        """
        if len(self.ret_features["total"]) == 0:
            return
        elif len(f_sess["stats"]["groups"]) == 1:
            return
        elif filt["group"] not in f_sess["stats"]["groups"]:
            return
        else:
            group_set = set()
            for sample in f_sess["samples"]:
                if filt["group"] in f_sess["samples"][sample]["groups"]:
                    group_set.update(set(f_sess["samples"][sample]["feature_ids"]))

            network_set = deepcopy(group_set)
            for network in f_sess["stats"]["networks"][filt["algorithm"]]["summary"]:
                if bool(
                    set(
                        f_sess["stats"]["networks"][filt["algorithm"]]["summary"][
                            network
                        ]
                    ).intersection(group_set)
                ):
                    network_set.update(
                        set(
                            f_sess["stats"]["networks"][filt["algorithm"]]["summary"][
                                network
                            ]
                        )
                    )

            self.ret_features["total"].intersection_update(network_set)
            for sample in self.ret_features["samples"]:
                self.ret_features["samples"][sample].intersection_update(network_set)
            return

    def create_chromatogram(self: Self, f_sess: dict):
        """Creates chromatogram from fermo.session file

        Arguments:
            f_sess: fermo session file
        """
        try:
            samples = f_sess.get("stats", {}).get("samples") or []
            for sample in samples:
                sample_data = f_sess.get("samples", {}).get(sample, {})
                feature_data = []
                for f_id in sample_data.get("feature_ids", []):
                    f_info = sample_data.get("sample_spec_features", {}).get(
                        str(f_id), {}
                    )
                    g_info = f_sess.get("general_features", {}).get(str(f_id), {})
                    novelty = g_info.get("scores", {}).get("novelty", {})

                    network_features = []
                    networks = f_sess.get("stats", {}).get("networks", {})
                    for network_type in networks:
                        network_data = networks.get(str(network_type), {}).get(
                            "summary", {}
                        )
                        for n_id in network_data:
                            n_features = network_data.get(str(n_id), {})
                            if f_id in n_features:
                                network_features = n_features

                    feature_data.append(
                        {
                            "f_id": f_info.get("f_id"),
                            "rt": f_info.get("rt"),
                            "trace_rt": f_info.get("trace_rt"),
                            "trace_int": f_info.get("trace_int"),
                            "abs_int": f_info.get("intensity"),
                            "rel_int": f_info.get("rel_intensity"),
                            "blank": g_info.get("blank"),
                            "novelty": 0 if not novelty else novelty,
                            "mz": g_info.get("mz"),
                            "samples": g_info.get("samples"),
                            "f_group": g_info.get("group_factors"),
                            "network_features": network_features,
                        }
                    )
                self.stats_chromatogram[sample] = feature_data

        except TypeError:
            self.stats_chromatogram = {"error": "error during parsing of session file"}
