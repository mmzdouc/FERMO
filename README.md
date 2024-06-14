fermo_gui
=========

`fermo_gui` is the graphical user interface for the metabolomics data analysis pipeline [`fermo_core`](https://github.com/mmzdouc/fermo_core). It allows to start new analysis jobs, load existing session files, and visualize results.

For more information about *FERMO*, `fermo_gui`, or `fermo_core`, see the [Documentation](https://mmzdouc.github.io/fermo_docs/).

*Nota bene*: `fermo_gui` has only been tested on Linux systems. While the Docker-installation is likely to work on other systems as well, they are not officially supported. Also see [*Fermo Online*](https://fermo.bioinformatics.nl/) for a user-friendly installation-free version.

Table of Contents
-----------------
- [Installation and Quickstart](#installation-and-quickstart)
- [Usage](#usage)
- [Attribution](#attribution)
- [For Developers](#for-developers)
- [Contributing](#contributing)

## Installation and Quickstart

### With docker from GitHub
- Install `docker` and `docker-compose`
- Download or clone the [repository](https://github.com/fermo-met/fermo_gui)
- (Change into the fermo_gui base directory if not already present)
- Run `docker-compose up --build`. This will install all dependencies and start the application.
- Open the application in any browser with the URL `http://0.0.0.0:8001/`

## Usage

For more information about *FERMO*, `fermo_gui`, or `fermo_core`, see the [Documentation](https://mmzdouc.github.io/fermo_docs/).

## Attribution

### License

FERMO is licensed under the [MIT License](LICENSE.md).

### Authors
- Mitja M. Zdouc <zdoucmm@gmail.com>
- Hannah E. Augustijn <hannah.augustijn@gmail.com>

### Publications

See [FERMO online](https://fermo.bioinformatics.nl/) for information on citing `fermo_gui`.

### Versions

All previous version of FERMO can be accessed via its [Zenodo repository](https://zenodo.org/doi/10.5281/zenodo.7565700).


## For Developers

### Dependencies

A list of dependencies can be found in the file [pyproject.toml](fermo_gui/pyproject.toml).

### Installation and Setup

- Clone the repository to your local machine and enter the `fermo_gui` [source directory](fermo_gui/)
- Install `python 3.11`
- Install `pip install pipx`
- Install `pipx install hatch`
- Run `hatch -v env create dev`
- Run `hatch run dev:pre-commit install`
- Install redis-server with `sudo apt-get install redis-server`
- Run the application with `hatch run dev:flask --app fermo_gui run --debug`
- In a separate command line window, run `hatch run dev:celery -A make_celery worker --loglevel ERROR`

### Contributing

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. Please see [Contributing](CONTRIBUTING.md) for more information on getting involved.
Contributors agree to adhere to the specified [Code of Conduct](CODE_OF_CONDUCT.md).
For technical details, see the For Developers pages in the [Documentation](https://mmzdouc.github.io/fermo_docs/for_devs/overview/).