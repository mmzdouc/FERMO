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

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired, FileSize
from wtforms import DecimalField, EmailField, IntegerField, SelectField, SubmitField
from wtforms.validators import Email, NumberRange, Optional


class NotificationForm:
    """Handles the notification related fields."""

    email = EmailField(
        label="Email Address",
        description="An optional e-mail address for job notification.",
        validators=[Optional(), Email()],
    )


class PeaktableForm:
    """Handles the peaktable related fields."""

    peaktable_file = FileField(
        label="File",
        description="Upload the peaktable file.",
        validators=[FileRequired(), FileAllowed(["csv"]), FileSize(max_size=5000000)],
    )
    peaktable_format = SelectField(
        label="Format",
        description="Specify formatting of the peaktable file.",
        validators=[Optional()],
        choices=[("mzmine3", "mzmine3")],
        default="mzmine3",
    )
    peaktable_polarity = SelectField(
        label="Polarity",
        description="Specify ion mode polarity of the peaktable file.",
        validators=[Optional()],
        choices=[("positive", "positive"), ("negative", "negative")],
        default="positive",
    )
    peaktable_filter_toggle = SelectField(
        label="Module",
        description="Activate feature filtering for area and/or height.",
        validators=[Optional()],
        choices=[("False", "deactivate"), ("True", "activate")],
        default="False",
    )
    peaktable_filter_height_lower = DecimalField(
        label="Filter Height (lower)",
        description=(
            "Set the minimal relative height (=intensity) of a feature. To include "
            "all, set to '0'."
        ),
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
        default=0.00,
    )
    peaktable_filter_height_upper = DecimalField(
        label="Filter Height (upper)",
        description=(
            "Set the maximum relative height (=intensity) of a feature. To include "
            "all, set to '1.0'."
        ),
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
        default=1.00,
    )
    peaktable_filter_area_lower = DecimalField(
        label="Filter Area (lower)",
        description=(
            "Set the minimal relative area of a feature. To include " "all, set to '0'."
        ),
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
        default=0.00,
    )
    peaktable_filter_area_upper = DecimalField(
        label="Filter Area (upper)",
        description=(
            "Set the maximum relative area of a feature. To include "
            "all, set to '1.0'."
        ),
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
        default=1.00,
    )


class MsmsForm:
    """Handles the msms related fields."""

    msms_file = FileField(
        label="File",
        description="Upload the MS/MS file.",
        validators=[Optional(), FileAllowed(["mgf"]), FileSize(max_size=10000000)],
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
            "the specified value"
        ),
        validators=[Optional(), NumberRange(min=0.0, max=1.0)],
        default=0.01,
    )


class PhenotypeForm:
    """Handles the phenotype related fields"""

    phenotype_file = FileField(
        label="File",
        description="Upload the phenotype file.",
        validators=[Optional(), FileAllowed(["csv"]), FileSize(max_size=1000000)],
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
    phenotype_qualit_factor = IntegerField(
        label="Factor",
        description="Fold difference for molecular feature differentiation.",
        validators=[Optional(), NumberRange(min=1)],
        default=10.0,
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


class AnalysisForm(
    FlaskForm,
    NotificationForm,
    PeaktableForm,
    MsmsForm,
    PhenotypeForm,
):
    """Organizes forms for data input"""

    start_analysis = SubmitField("Start analysis")
