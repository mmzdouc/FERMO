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
from wtforms import DecimalField, EmailField, SelectField, SubmitField
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


class MsmsForm:
    """Handles the msms related fields."""

    msms_file = FileField(
        label="File",
        description="Upload the MS/MS file.",
        validators=[Optional(), FileAllowed(["mgf"]), FileSize(max_size=5000000)],
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


class AnalysisForm(FlaskForm, NotificationForm, PeaktableForm, MsmsForm):
    """Organizes forms for data input"""

    start_analysis = SubmitField("Start analysis")
