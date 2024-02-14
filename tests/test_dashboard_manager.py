import pytest

from fermo_gui.analysis.dashboard_manager import DashboardManager as Manager
from fermo_gui.analysis.general_manager import GeneralManager


@pytest.fixture
def session():
    return GeneralManager().read_data_from_json(
        "fermo_gui/upload/example", "example.session.json"
    )


def test_init_dashboard_manager():
    assert isinstance(Manager(), Manager)


def test_get_stats_analysis_valid(session):
    manager = Manager()
    manager.get_stats_analysis(session)
    variable = manager.stats_analysis
    assert isinstance(variable, dict)
    assert variable["Total Samples"] == 11
    assert variable["Sample Groups"] == 5
    assert variable["Molecular Features"] == 143
