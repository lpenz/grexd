[![CI](https://github.com/lpenz/grexd/actions/workflows/ci.yml/badge.svg)](https://github.com/lpenz/grexd/actions/workflows/ci.yml)
[![coveralls](https://coveralls.io/repos/github/lpenz/grexd/badge.svg?branch=main)](https://coveralls.io/github/lpenz/grexd?branch=main)
[![PyPI](https://img.shields.io/pypi/v/grexd)](https://pypi.org/project/grexd/)
[![github](https://img.shields.io/github/v/release/lpenz/disk-img-tool?logo=github)](https://github.com/lpenz/disk-img-tool/releases)


# grexd

A console regular expression editor based on python's [prompt-toolkit].


## Installation


### Releases

grexd can be installed via [pypi]:

```
pip install grexd
```

For [nix] users, it is also available as a [flake].


### Repository

We can also clone the github repository and install grexd from it with:

```
pip install .
```

We can also install it for the current user only by running instead:

```
pip install --user .
```


## Development

grexd uses the standard python3 infra. To develop and test the module:
- Clone the repository and go into the directory:
  ```
  git clone git@github.com:lpenz/grexd.git
  cd grexd
  ```
- Use [`venv`] to create a local virtual environment with
  ```
  python -m venv venv
  ```
- Activate the environment by running the shell-specific `activate`
  script in `./venv/bin/`. For [fish], for instance, run:
  ```
  source ./venv/bin/activate.fish
  ```
- Install grexd in "editable mode":
  ```
  pip install -e '.[test]'
  ```
- To run the tests:
  ```
  pytest
  ```
  Or, to run the tests with coverage:
  ```
  pytest --cov
  ```
- Finally, to exit the environment and clean it up:
  ```
  deactivate
  rm -rf venv
  ```


[pypi]: https://pypi.org/project/grexd/
[nix]: https://nixos.org/
[flake]: https://nixos.wiki/wiki/Flakes
[`venv`]: https://docs.python.org/3/library/venv.html
[prompt-toolkit]: https://github.com/prompt-toolkit/python-prompt-toolkit
