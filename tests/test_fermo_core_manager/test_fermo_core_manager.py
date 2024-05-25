from pathlib import Path

import pytest
import jsonschema

from fermo_gui.analysis.fermo_core_manager import FermoCoreManager


def test_run_fermo_core_min_jobid_invalid():
    m_fermo = FermoCoreManager(
        job_id="nonexisting_folder", uploads_dir=Path("tests/test_fermo_core_manager/")
    )
    with pytest.raises(FileNotFoundError):
        m_fermo.run_fermo_core()


def test_run_fermo_core_min_json_invalid():
    m_fermo = FermoCoreManager(
        job_id="example_invalid_input_data",
        uploads_dir=Path("tests/test_fermo_core_manager/"),
    )
    with pytest.raises(jsonschema.exceptions.ValidationError):
        m_fermo.run_fermo_core()


def test_run_fermo_core_min_valid():
    m_fermo = FermoCoreManager(
        job_id="example_data_min", uploads_dir=Path("tests/test_fermo_core_manager/")
    )
    assert m_fermo.run_fermo_core() is None
