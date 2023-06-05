# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- MS/MS mirror plots in dashboard
- Support for MASSQL search in dashboard
- Integration with [INVENTA](https://github.com/luigiquiros/inventa)
- Compatibility with OpenMS output
- Compatibility with XCMS output
- Compatibility with SIRIUS output
- Support for negative ion mode (adduct recognition, annotation)

### Changed

- Cytoscape view: incorporate group metadata information & connect to chromatogram view to update via click on node

## [0.9.0] - 2023-??-??

### Changed

- Replacement of Dash with Flask
- Folder structure in src/fermo/ changed following Flask 2.2.0 recommendations

## [0.8.10] - 2023-02-14

### Fixed

- Bugfix of `modify_feature_info_df()` in  `dashboard_functions.py`

## [0.8.9] - 2023-02-10

### Added

- Tracking of changes with CHANGELOG.md

### Changed

- Changed relative module import paths to absolute ones, making installation of tool via `pip install -e .` mandatory

### Fixed

- Bugfix by modifying `requirements.txt`: specifying package `matchmsextras==0.3.0`

## [0.8.8] - 2023-01-24

### Added

- Expanded adduct detection functionality - FERMO now also recognizes `[M+NH4]+`, `[M+K]+`, `[M+H2O+H]+`, `[M-H2O+H]+` (0.8.8.3)

### Changed

- Rework of fold-change filter on dashboard page: a range, and groups to be excluded or included can be specified (0.8.8.1)
- Changed handling of webbrowser opening (0.8.8.2)

## [0.8.7] - 2023-01-15

### Added:

- Installation via `pip install .` using `pyproject.toml`
- Centralization of dependency metadata in `requirements.txt`
- Bibliographic information using `CITATION.cff`
- Initialization of testing via `pytest` package
- Coverage of `calculate_feature_overlap.py` with unit tests
- Build testing with GitHub actions workflow `.github/workflows/CI_build.yml`

### Changed:

- Changed directory structure: moved source code to `src/fermo/...`
- Rewrite of `calculate_feature_overlap.py` to allow for testing and increase maintainability

## [0.8.6] - 2022-12-25

### Fixed:

- Bugfix in quantitative biological data parsing related to issue [Cannot upload quantitative biological data (*.csv) file](https://github.com/mmzdouc/FERMO/issues/1)

## [0.8.5] - 2022-12-23

### Added:

- Initial public version of FERMO
