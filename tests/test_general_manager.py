import pytest

from fermo_gui.analysis.general_manager import GeneralManager


def test_check_unique_task_id_valid():
    assert isinstance(GeneralManager().create_uuid("fermo_gui/upload"), str)
