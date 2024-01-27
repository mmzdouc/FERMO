Announcement - Please Read
============
### FERMO is currently being refactored. The code in this fork is experimental and may change quickly and without announcements. For a more stable version, please look at [FERMO's main page](https://github.com/mmzdouc/fermo).

---

## Dependencies

A list of dependencies can be found in the file [pyproject.toml](pyproject.toml).

## License

FERMO is licensed under the [MIT License](LICENSE.md).

## For Developers

### Installation and Setup

- Clone the repository to your local machine and enter it: this is the main directory
- Create a new virtual environment (e.g. with `conda`)
- Install `python 3.11`
- Install `fermo_gui` with `pip install -e '.[dev]'` (while in the main directory)
- Initialize `pre-commit` with `pre-commit install`.
- Run the app with `flask --app fermo_gui run --debug` (while in the main directory)

### Contributing and Coding Style

For general guidelines regarding contributing to this project, see [CONTRIBUTING](CONTRIBUTING.md).
Furthermore, we have a [CODE OF CONDUCT](CODE_OF_CONDUCT.md).

#### Practices:

This project follows certain practices to ensure coding standards:
- For code development, use of a branching model - one branch per feature, pull
  requests to merge into `main`. The `main` branch is protected.
- For consistent code style, tools including `black`, `flake8`.
- Application of said tools before committing via `pre-commit`.
- Unit testing using `pytest` and test-driven development in general.
- Use of type hinting and docstrings (the use of `pycodestyle` is recommended).
- Following the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- Versioning using [Semantic Versioning](http://semver.org/).

#### Code contribution:

To contribute code:
- Communicate with the lead developers and discuss the intended change/feature.
- For each feature/change, create a new branch.
- Add and test it thoroughly (with unit tests).

To merge into the `main` branch:
- Add changes to the [CHANGELOG](CHANGELOG.md) using plain and concise language.
- Update the version by increasing the counter in [pyproject.toml](pyproject.toml)
  as instructed by the lead developers.
- Issue a pull request to the `main` branch.
- After code review, the pull request may or may not be accepted.
