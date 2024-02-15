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
    manager.extract_stats_analysis(session)
    assert isinstance(manager.stats_analysis, dict)
    assert manager.stats_analysis["Total Samples"] == 11
    assert manager.stats_analysis["Sample Groups"] == 5
    assert manager.stats_analysis["Molecular Features"] == 143


def test_get_stats_analysis_invalid():
    manager = Manager()
    manager.extract_stats_analysis({})
    assert manager.stats_analysis == {"error": "error during parsing of session file"}


def test_extract_stats_samples_dyn_valid(session):
    manager = Manager()
    manager.extract_stats_samples_dyn(session)
    assert len(manager.stats_samples_dyn) == 11
    assert manager.stats_samples_dyn["5440_5439_mod.mzXML"]["groups"] == "A2"
    assert manager.stats_samples_dyn["5440_5439_mod.mzXML"]["total_features"] == 23
    assert manager.stats_samples_dyn["5440_5439_mod.mzXML"]["retained_features"] == 23


def test_extract_stats_samples_dyn_invalid():
    manager = Manager()
    manager.extract_stats_samples_dyn({})
    assert manager.stats_samples_dyn == {
        "error": "error during parsing of session file"
    }


def test_prepare_ret_features(session):
    manager = Manager()
    manager.prepare_ret_features(session)
    assert len(manager.ret_features.get("total")) == 143


def test_extract_retained_features_valid(session):
    manager = Manager()
    filters = {"rel_intensity": [0.0, 1.0], "rel_area": [0.0, 1.0]}
    manager.filter_ret_features(session, filters)
    assert len(manager.ret_features["total"]) == 143


def test_filter_feature_range_valid(session):
    manager = Manager()
    manager.prepare_ret_features(session)
    manager.filter_feature_range(session, [0.06, 1.0], "rel_intensity")
    assert len(manager.ret_features["total"]) == 140
