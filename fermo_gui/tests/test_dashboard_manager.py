import pytest

from fermo_gui.analysis.dashboard_manager import DashboardManager as Manager
from fermo_gui.analysis.general_manager import GeneralManager


@pytest.fixture
def session():
    return GeneralManager().read_data_from_json(
        "fermo_gui/upload/example/results", "out.fermo.session.json"
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
            "algorithm": "modified_cosine",
            "n_id": 1,
        },
        "groups_feature": "S",
        "groups_network": {
            "algorithm": "modified_cosine",
            "group": "S",
        },
        "nr_samples": {"minimum": 0, "maximum": 0},
        "precursor_mz": [0.0, 3000.0],
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
    assert manager.stats_analysis["Molecular Features"] == 143


def test_get_stats_analysis_invalid():
    manager = Manager()
    manager.extract_stats_analysis({})
    assert manager.stats_analysis == {"error": "error during parsing of session file"}


def test_extract_stats_samples_dyn_valid(session):
    manager = Manager()
    manager.extract_stats_samples_dyn(session)
    assert len(manager.stats_samples_dyn) == 11
    assert manager.stats_samples_dyn[0]["Phylogroup"] == "A2"
    assert manager.stats_samples_dyn[0]["Total features"] == 22
    assert manager.stats_samples_dyn[0]["Retained features"] == 22


def test_extract_stats_samples_dyn_invalid():
    manager = Manager()
    manager.extract_stats_samples_dyn({})
    assert manager.stats_samples_dyn == {
        "error": "error during parsing of session file"
    }
