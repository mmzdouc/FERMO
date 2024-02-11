import pytest

from fermo_gui.analysis.general_manager import GeneralManager


def test_check_unique_task_id_valid():
    assert isinstance(GeneralManager().create_uuid("fermo_gui/upload"), str)


def test_create_upload_dir_valid(tmp_path):
    GeneralManager().create_upload_dir(str(tmp_path), "123")
    assert len(list(tmp_path.iterdir())) == 1


def test_create_upload_dir_invalid(tmp_path):
    GeneralManager().create_upload_dir(str(tmp_path), "123")
    with pytest.raises(OSError):
        GeneralManager().create_upload_dir(str(tmp_path), "123")
