fermo_gui
=========

`fermo_gui` is the graphical user interface for the metabolomics data analysis pipeline [`fermo_core`](https://github.com/mmzdouc/fermo_core). It allows to start new analysis jobs, load existing session files, and visualize results.

For more information about *FERMO*, `fermo_gui`, or `fermo_core`, see the [Documentation](https://mmzdouc.github.io/fermo_docs/).

*Nota bene*: `fermo_gui` has only been tested on Linux systems. While the Docker-installation is likely to work on other systems as well, they are not officially supported. See [*Fermo Online*](https://fermo.bioinformatics.nl/) for a user-friendly installation-free version.

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
- Download or clone the [repository](https://github.com/mmzdouc/fermo)
- (Change into the fermo_gui base directory if not already present)
- Run `docker-compose up --build`. This will compose the docker container, install all dependencies and start the application.
- Open the application in any browser with the URL `http://0.0.0.0:8001/`
- To terminate the container, simply hit `ctrl+c`

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

### Config file

The flask application automatically reads configuration settings from a `config.py` file in the `instance` directory in the `fermo_gui` [source directory](fermo_gui/) (not in version control for security reasons). 
If not available, `fermo_gui` will employ default settings, assuming that the application runs offline. 
These default settings must not be used if the application is to be deployed to production. 
The following default settings are used:

```python
SECRET_KEY: str
ONLINE: bool = True
MAX_RUN_TIME: int = 3600
CELERY: dict = {
    "broker_url": "redis://localhost",
    "result_backend": "redis://localhost",
    "task_ignore_result": True,
    "task_soft_time_limit": 3600
}
MAIL_USERNAME: str
MAIL_PASSWORD: str
MAIL_DEFAULT_SENDER: str
MAIL_SERVER: str
MAIL_PORT: int
MAIL_USE_TLS: bool
MAIL_USE_SSL: bool
```

Further, the number of workers can be adjusted in the [`entrypoint_docker.sh`](fermo_gui/entrypoint_docker.sh) script.

### Contributing

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. Please see [Contributing](CONTRIBUTING.md) for more information on getting involved.
Contributors agree to adhere to the specified [Code of Conduct](CODE_OF_CONDUCT.md).
For technical details, see the For Developers pages in the [Documentation](https://mmzdouc.github.io/fermo_docs/for_devs/overview/).