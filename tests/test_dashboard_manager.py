import pytest

from fermo_gui.analysis.dashboard_manager import DashboardManager as Manager
from fermo_gui.analysis.general_manager import GeneralManager


@pytest.fixture
def session():
    return GeneralManager().read_data_from_json(
        "fermo_gui/upload/example", "example.session.json"
    )


@pytest.fixture
def filters():
    return {
        "rel_intensity": [0.0, 1.0],
        "abs_intensity": [0, 100000000],
        "rel_area": [0.0, 1.0],
        "abs_area": [0, 100000000],
        "peak_overlap": [0.0, 1.0],
        "novelty_score": [0.0, 1.0],
        "blank_assoc": False,
        "quant_data_assoc": {
            "algorithm": "all",
        },
        "annotation": {"field": "ms2query", "value": "siomycin", "regexp": False},
        "feature_id": 1,
        "network_id": {
            "algorithm": "mod_cosine",
            "n_id": 1,
        },
        "groups_feature": "S",
        "groups_network": "S",
        "nr_samples": [1, 3],
        "precursor_mz": [100.0, 200.0],
        "fold_include": {"groups": "S/V2", "n_fold": 3.2},
        "fold_exclude": {"groups": "V2/S", "n_fold": 2.0},
    }


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


def test_extract_retained_features_valid(session, filters):
    manager = Manager()
    manager.filter_ret_features(session, filters)
    assert len(manager.ret_features["total"]) == 143


def test_filter_rel_intensity_valid(session):
    manager = Manager()
    manager.prepare_ret_features(session)
    manager.filter_spec_feature_range(session, [0.06, 1.0], "rel_intensity")
    assert len(manager.ret_features["total"]) == 140


def test_filter_abs_intensity_valid(session):
    manager = Manager()
    manager.prepare_ret_features(session)
    manager.filter_spec_feature_range(session, [110000, 110000], "intensity")
    assert len(manager.ret_features["total"]) == 2


def test_filter_rel_area_valid(session):
    manager = Manager()
    manager.prepare_ret_features(session)
    manager.filter_spec_feature_range(session, [0.06, 1.0], "rel_area")
    assert len(manager.ret_features["total"]) == 104


def test_filter_abs_area_valid(session):
    manager = Manager()
    manager.prepare_ret_features(session)
    manager.filter_spec_feature_range(session, [44000, 44000], "area")
    assert len(manager.ret_features["total"]) == 1


def test_filter_feature_id_valid(session):
    manager = Manager()
    manager.prepare_ret_features(session)
    manager.filter_feature_id(1)
    assert len(manager.ret_features["total"]) == 1


def test_filter_feature_id_invalid(session):
    manager = Manager()
    manager.prepare_ret_features(session)
    manager.filter_feature_id(1234567)
    assert len(manager.ret_features["total"]) == 0
