"""Class to manage data input forms for fermo data analysis

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

from typing import Self

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileSize
from wtforms import (
    DecimalField,
    EmailField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import Email, NumberRange, Optional


class NotificationForm:
    """Handles the notification related fields."""

    email = EmailField(
        label="Email Notification",
        description="An optional e-mail address for job notification.",
        validators=[Optional(), Email()],
    )


class ReloadJobForm:
    """Handles the job settings reloading related fields."""

    reload_jobid = StringField(
        label="FERMO JobID",
        description=(
            "Reload parameter settings from a previous FERMO job. 'File' uploads are "
            "not retained and must be newly uploaded."
        ),
        validators=[Optional()],
    )


class PeaktableForm:
    """Handles the peaktable related fields."""

    peaktable_file = FileField(
        label="File",
        description="Upload the peaktable file.",
        validators=[Optional(), FileAllowed(["csv"]), FileSize(max_size=2000000)],
    )
    peaktable_format = SelectField(
        label="Format",
        description="Specify formatting of the peaktable file.",
        validators=[Optional()],
        choices=[("mzmine3", "mzmine3")],
    )
    peaktable_polarity = SelectField(
        label="Polarity",
        description="Specify ion mode polarity of the peaktable file.",
        validators=[Optional()],
        choices=[("positive", "positive"), ("negative", "negative")],
    )
    peaktable_ppm = DecimalField(
        label="Mass Deviation",
        description=(
            "Estimated mass accuracy of data in ppm. Used for annotation of ion "
            "adducts, MS/MS neutral losses, and MS/MS fragments."
        ),
        validators=[Optional(), NumberRange(min=0.0)],
    )
    peaktable_filter_toggle = SelectField(
        label="Module",
        description="Activate feature filtering for area and/or height.",
        validators=[Optional()],
        choices=[("False", "inactive"), ("True", "active")],
    )
    peaktable_filter_height_lower = DecimalField(
        label="Filter Height (lower)",
        description=(
            "Set the minimal relative height (=intensity) of a molecular feature. To "
            "include all, set to '0'."
        ),
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
    )
    peaktable_filter_height_upper = DecimalField(
        label="Filter Height (upper)",
        description=(
            "Set the maximum relative height (=intensity) of a molecular feature. To "
            "include all, set to '1.0'."
        ),
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
    )
    peaktable_filter_area_lower = DecimalField(
        label="Filter Area (lower)",
        description=(
            "Set the minimal relative area of a molecular feature. To include all, "
            "set to '0'."
        ),
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
    )
    peaktable_filter_area_upper = DecimalField(
        label="Filter Area (upper)",
        description=(
            "Set the maximum relative area of a molecular feature. To include "
            "all, set to '1.0'."
        ),
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
    )


class MsmsForm:
    """Handles the msms related fields."""

    msms_file = FileField(
        label="File",
        description="Upload the MS/MS file.",
        validators=[Optional(), FileAllowed(["mgf"]), FileSize(max_size=8000000)],
    )
    msms_format = SelectField(
        label="Format",
        description="Specify formatting of the MS/MS file.",
        validators=[Optional()],
        choices=[("mgf", "mgf")],
        default="mgf",
    )
    msms_rel_int_from = DecimalField(
        label="Filter",
        description=(
            "Removes MS/MS fragments with lower relative intensity than "
            "the specified value. Set to 0.0 to retain all fragments."
        ),
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
        default=0.01,
    )
    msms_fragment_toggle = SelectField(
        label="Fragment Annotation",
        description="Activate MS/MS fragment annotation.",
        validators=[Optional()],
        choices=[("True", "active"), ("False", "inactive")],
        default="True",
    )
    msms_loss_toggle = SelectField(
        label="Loss annotation",
        description="Activate MS/MS neutral loss annotation.",
        validators=[Optional()],
        choices=[("True", "active"), ("False", "inactive")],
        default="True",
    )
    msms_cosine_toggle = SelectField(
        label="Module",
        description="Activate modified cosine-based spectral (=molecular) networking.",
        validators=[Optional()],
        choices=[("True", "active"), ("False", "inactive")],
        default="True",
    )
    msms_cosine_minfrag = IntegerField(
        label="MS/MS fragments",
        description=(
            "Minimum number of fragments per spectrum to consider in " "networking"
        ),
        validators=[Optional(), NumberRange(min=1)],
        default=5,
    )
    msms_cosine_tolerance = DecimalField(
        label="Fragment tolerance",
        description="Tolerance in matching two MS/MS fragments, in m/z units.",
        validators=[Optional(), NumberRange(min=0.0)],
        default=0.1,
    )
    msms_cosine_score = DecimalField(
        label="Score",
        description="Score cutoff to match two MS/MS spectra.",
        validators=[Optional(), NumberRange(min=0.1, max=1.0)],
        default=0.7,
    )
    msms_cosine_links = IntegerField(
        label="Edges",
        description="Maximum number of edges any node is allowed to have.",
        validators=[Optional(), NumberRange(min=1)],
        default=10,
    )
    msms_deepscore_toggle = SelectField(
        label="Module",
        description="Activate MS2DeepScore-based spectral (=molecular) networking.",
        validators=[Optional()],
        choices=[("True", "active"), ("False", "inactive")],
        default="True",
    )
    msms_deepscore_minfrag = IntegerField(
        label="MS/MS fragments",
        description=(
            "Minimum number of fragments per spectrum to consider in " "networking"
        ),
        validators=[Optional(), NumberRange(min=1)],
        default=5,
    )
    msms_deepscore_score = DecimalField(
        label="Score",
        description="Score cutoff to match two MS/MS spectra.",
        validators=[Optional(), NumberRange(min=0.1, max=1.0)],
        default=0.8,
    )
    msms_deepscore_links = IntegerField(
        label="Edges",
        description="Maximum number of edges any node is allowed to have.",
        validators=[Optional(), NumberRange(min=1)],
        default=10,
    )


class PhenotypeForm:
    """Handles the phenotype related fields"""

    phenotype_file = FileField(
        label="File",
        description="Upload the phenotype file.",
        validators=[Optional(), FileAllowed(["csv"]), FileSize(max_size=2000000)],
    )
    phenotype_format = SelectField(
        label="Format",
        description="Specify formatting of the phenotype file.",
        validators=[Optional()],
        choices=[
            ("", ""),
            ("qualitative", "qualitative"),
            ("quantitative-percentage", "quantitative-percentage"),
            ("quantitative-concentration", "quantitative-concentration"),
        ],
        default="",
    )
    phenotype_qualit_factor = DecimalField(
        label="Factor",
        description="Fold difference for molecular feature differentiation.",
        validators=[Optional(), NumberRange(min=1)],
        default=10,
    )
    phenotype_qualit_algorithm = SelectField(
        label="Algorithm",
        description="Specify algorithm to calculate fold difference.",
        validators=[Optional()],
        choices=[("minmax", "minmax"), ("mean", "mean"), ("median", "median")],
        default="minmax",
    )
    phenotype_qualit_value = SelectField(
        label="Value",
        description="Specify value to use for calculation.",
        validators=[Optional()],
        choices=[
            ("area", "area"),
            ("height", "height"),
        ],
        default="area",
    )
    phenotype_quant_average = SelectField(
        label="Averaging",
        description=(
            "Specify the measure of central tendency to summarize duplicate "
            "measurements per sample."
        ),
        validators=[Optional()],
        choices=[("mean", "mean"), ("median", "median")],
        default="mean",
    )
    phenotype_quant_value = SelectField(
        label="Value",
        description="Specify value to use for calculation.",
        validators=[Optional()],
        choices=[("area", "area")],
        default="area",
    )
    phenotype_quant_algorithm = SelectField(
        label="Algorithm",
        description="Specify the statistical algorithm to determine correlation.",
        validators=[Optional()],
        choices=[("pearson", "Pearson (Bonferroni-correction)")],
        default="pearson",
    )
    phenotype_quant_p_val = DecimalField(
        label="p-Value",
        description=(
            "Maximum corrected p-value to consider (set to '0' to disable filtering)."
        ),
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
        default=0.05,
    )
    phenotype_quant_coeff = DecimalField(
        label="Coefficient",
        description=(
            "Minimum correlation coefficient to consider (set to '0' to disable "
            "filtering)."
        ),
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
        default=0.7,
    )


class GroupForm:
    """Handles the group metadata related fields"""

    group_file = FileField(
        label="File",
        description="Upload the group metadata file.",
        validators=[Optional(), FileAllowed(["csv"]), FileSize(max_size=2000000)],
    )
    group_format = SelectField(
        label="Format",
        description="Specify the format of the group metadata file.",
        validators=[Optional()],
        choices=[
            ("fermo", "fermo"),
        ],
        default="fermo",
    )
    group_blank_toggle = SelectField(
        label="Module",
        description=(
            "Activate feature blank assignment (requires samples marked as 'BLANK')."
        ),
        validators=[Optional()],
        choices=[("False", "inactive"), ("True", "active")],
        default="False",
    )
    group_blank_factor = IntegerField(
        label="Factor",
        description="Fold difference for blank assignment of molecular feature.",
        validators=[Optional(), NumberRange(min=1)],
        default=10,
    )
    group_blank_algorithm = SelectField(
        label="Algorithm",
        description="Specify the algorithm to calculate fold difference.",
        validators=[Optional()],
        choices=[("mean", "mean"), ("median", "median"), ("maximum", "maximum")],
        default="mean",
    )
    group_blank_value = SelectField(
        label="Value",
        description="Value to consider for the calculation.",
        validators=[Optional()],
        choices=[("area", "area"), ("height", "height")],
        default="area",
    )
    group_factor_toggle = SelectField(
        label="Module",
        description=(
            "Activate the calculation of fold-changes between groups of a category."
        ),
        validators=[Optional()],
        choices=[("False", "inactive"), ("True", "active")],
        default="False",
    )
    group_factor_algorithm = SelectField(
        label="Algorithm",
        description="Specify the algorithm to calculate the fold changes.",
        validators=[Optional()],
        choices=[("mean", "mean"), ("median", "median"), ("maximum", "maximum")],
        default="mean",
    )
    group_factor_value = SelectField(
        label="Value",
        description="Value to consider for the calculation.",
        validators=[Optional()],
        choices=[("area", "area"), ("height", "height")],
        default="area",
    )


class LibraryForm:
    """Handles the spectral library related fields"""

    library_file = FileField(
        label="File",
        description="Upload an MS/MS spectral library file.",
        validators=[Optional(), FileAllowed(["mgf"]), FileSize(max_size=8000000)],
    )
    library_format = SelectField(
        label="Format",
        description="Specify the format of the spectral library file.",
        validators=[Optional()],
        choices=[("mgf", "mgf")],
        default="mgf",
    )
    library_cosine_toggle = SelectField(
        label="Module",
        description="Activate modified cosine-based spectral library matching.",
        validators=[Optional()],
        choices=[("False", "inactive"), ("True", "active")],
        default="False",
    )
    library_cosine_tolerance = DecimalField(
        label="Fragment tolerance",
        description="Tolerance in matching two MS/MS fragments, in m/z units.",
        validators=[Optional(), NumberRange(min=0.0)],
        default=0.1,
    )
    library_cosine_matches = IntegerField(
        label="Matched fragments",
        description="Minimum number of fragment matches",
        validators=[Optional(), NumberRange(min=1)],
        default=5,
    )
    library_cosine_score = DecimalField(
        label="Score",
        description="Score cutoff to match two MS/MS spectra.",
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
        default=0.7,
    )
    library_cosine_mzdiff = IntegerField(
        label="Precursor Difference",
        description=(
            "Maximum tolerated difference between two precursor masses (in m/z)."
        ),
        validators=[Optional(), NumberRange(min=0)],
        default=600,
    )
    library_deepscore_toggle = SelectField(
        label="Module",
        description="Activate MS2DeepScore-based spectral library matching.",
        validators=[Optional()],
        choices=[("False", "inactive"), ("True", "active")],
        default="False",
    )
    library_deepscore_score = DecimalField(
        label="Score",
        description="Score cutoff to match two MS/MS spectra.",
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
        default=0.8,
    )
    library_deepscore_mzdiff = IntegerField(
        label="Precursor Difference",
        description=(
            "Maximum tolerated difference between two precursor masses (in m/z)."
        ),
        validators=[Optional(), NumberRange(min=0)],
        default=600,
    )


class Ms2queryForm:
    """Handles the MS2Query matching related fields"""

    ms2query_file = FileField(
        label="Existing File",
        description="Upload a pre-calulated MS2Query results file.",
        validators=[Optional(), FileAllowed(["csv"]), FileSize(max_size=2000000)],
    )
    ms2query_score = DecimalField(
        label="Score",
        description="Score cutoff for MS2Query model matches.",
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
        default=0.7,
    )
    ms2query_toggle = SelectField(
        label="New Calculation",
        description=(
            "Activate de novo MS2Query annotation (Note: computationally intense - "
            "takes about 2 seconds per spectrum. Calculation time is restricted.)"
        ),
        validators=[Optional()],
        choices=[("False", "inactive"), ("True", "active")],
        default="False",
    )


class ASKCBForm:
    """Handles the antiSMASH Knownclusterblast matching related fields"""

    askcb_jobid = StringField(
        label="antiSMASH JobID",
        description=("The antiSMASH job to use for integrated analysis with FERMO."),
        validators=[Optional()],
    )
    askcb_score = DecimalField(
        label="Similarity score",
        description=(
            "Similarity (%) cutoff for KnownClusterBlast matches against "
            "MIBiG to consider in analysis."
        ),
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
        default=0.7,
    )
    askcb_cosine_toggle = SelectField(
        label="Module",
        description="Activate modified cosine-based MIBiG spectral library matching.",
        validators=[Optional()],
        choices=[("False", "inactive"), ("True", "active")],
        default="False",
    )
    askcb_cosine_tolerance = DecimalField(
        label="Fragment tolerance",
        description="Tolerance in matching two MS/MS fragments, in m/z units.",
        validators=[Optional(), NumberRange(min=0.0)],
        default=0.1,
    )
    askcb_cosine_matches = IntegerField(
        label="Matched fragments",
        description="Minimum number of fragment matches",
        validators=[Optional(), NumberRange(min=1)],
        default=5,
    )
    askcb_cosine_score = DecimalField(
        label="Score",
        description="Score cutoff to match two MS/MS spectra.",
        validators=[Optional(), NumberRange(min=0.1, max=1.0)],
        default=0.5,
    )
    askcb_cosine_mzdiff = IntegerField(
        label="Precursor Difference",
        description=(
            "Maximum tolerated difference between two precursor masses (in m/z)."
        ),
        validators=[Optional(), NumberRange(min=0)],
        default=600,
    )
    askcb_deepscore_toggle = SelectField(
        label="Module",
        description="Activate MS2DeepScore-based MIBiG spectral library matching.",
        validators=[Optional()],
        choices=[("False", "inactive"), ("True", "active")],
        default="False",
    )
    askcb_deepscore_score = DecimalField(
        label="Score",
        description="Score cutoff to match two MS/MS spectra.",
        validators=[Optional(), NumberRange(min=0.1, max=1.0)],
        default=0.7,
    )
    askcb_deepscore_mzdiff = IntegerField(
        label="Precursor Difference",
        description=(
            "Maximum tolerated difference between two precursor masses (in m/z)."
        ),
        validators=[Optional(), NumberRange(min=0)],
        default=600,
    )


class SubmitForm:
    """Handles the submit analysis form field"""

    start_analysis = SubmitField("Start analysis")


class AnalysisForm(
    FlaskForm,
    NotificationForm,
    ReloadJobForm,
    PeaktableForm,
    MsmsForm,
    PhenotypeForm,
    GroupForm,
    LibraryForm,
    Ms2queryForm,
    ASKCBForm,
    SubmitForm,
):
    """Organizes forms for data input"""

    def apply_defaults(self: Self, p: dict):
        """Dynamically sets defaults for form fields

        Arguments:
            p: the parameters dict
        """
        dflt = {
            "peaktable_format": "mzmine3",
            "peaktable_polarity": "positive",
            "peaktable_ppm": 10,
            "peaktable_filter_toggle": False,
            "peaktable_filter_height_lower": 0.0,
            "peaktable_filter_height_upper": 1.0,
            "peaktable_filter_area_lower": 0.0,
            "peaktable_filter_area_upper": 1.0,
        }

        # TODO: Continue putting every hardcoded param in dict

        self.peaktable_format.default = (
            p.get("files", {})
            .get("peaktable", {})
            .get("format", dflt["peaktable_format"])
        )
        self.peaktable_polarity.default = (
            p.get("files", {})
            .get("peaktable", {})
            .get("polarity", dflt["peaktable_polarity"])
        )
        self.peaktable_ppm.default = (
            p.get("core_modules", {})
            .get("adduct_annotation", {})
            .get("mass_dev_ppm", dflt["peaktable_ppm"])
        )
        self.peaktable_filter_toggle.default = str(
            p.get("additional_modules", {})
            .get("feature_filtering", {})
            .get("activate_module", dflt["peaktable_filter_toggle"])
        )
        try:
            r_list = (
                p.get("additional_modules", {})
                .get("feature_filtering", {})
                .get("filter_rel_int_range")
            )
            self.peaktable_filter_height_lower.default = min(r_list)
            self.peaktable_filter_height_upper.default = max(r_list)
        except TypeError:
            self.peaktable_filter_height_lower.default = dflt[
                "peaktable_filter_height_lower"
            ]
            self.peaktable_filter_height_upper.default = dflt[
                "peaktable_filter_height_upper"
            ]
        try:
            r_list = (
                p.get("additional_modules", {})
                .get("feature_filtering", {})
                .get("filter_rel_area_range")
            )
            self.peaktable_filter_area_lower.default = min(r_list)
            self.peaktable_filter_area_upper.default = max(r_list)
        except TypeError:
            self.peaktable_filter_area_lower.default = dflt[
                "peaktable_filter_area_lower"
            ]
            self.peaktable_filter_area_upper.default = dflt[
                "peaktable_filter_area_upper"
            ]

        # TODO: continue with msms etc.

        # TODO(MMZ 31.5.):expand here for other defaults

        for field in self._fields.values():
            field.process(formdata=None)
