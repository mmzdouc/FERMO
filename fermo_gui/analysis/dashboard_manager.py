"""Manages all dashboard functionality

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
from typing import Optional, Self

from pydantic import BaseModel


class DashboardManager(BaseModel):
    """Organize general functionality such as data management"""

    stats_analysis: Optional[dict] = None

    def get_dashboard_data(self: Self, f_sess: dict, filters: Optional[dict] = None):
        """Extract and filter dashboard data

        Filter settings can be provided to filter output data (for POST methods)

        Arguments:
            f_sess: fermo session file
            filters: optional filter settings
        """
        self.get_stats_analysis(f_sess)

    def to_json_dict(self: Self) -> dict:
        """Returns dashboard data as dict

        Returns: a json-compatible dict
        """
        return {"stats_analysis": self.stats_analysis}

    def get_stats_analysis(self: Self, f_sess: dict):
        """Extracts static analysis stats from fermo.session file

        Arguments:
            f_sess: fermo session file
        """
        self.stats_analysis = {
            "Total Samples": len(f_sess.get("stats", {}).get("samples")),
            "Sample Groups": (len(f_sess.get("stats", {}).get("groups")) - 1),
            "Molecular Features": f_sess.get("stats", {}).get("features"),
            "Removed Mol. Features": len(
                f_sess.get("stats", {}).get("inactive_features")
            ),
            "FERMO-CORE Version": f_sess.get("metadata", {}).get("fermo_core_version"),
        }

    # each data package is its own attribute (a dict)

    # build up the attributes with different functions

    # for the post functionality, apply filters to the dictionaries

    # have an export function that dups it at once as a json-compatible dict

    # TODO(MMZ 14.2.24): Cover with tests
