# ghi

A wrapper for github cli.

<https://cli.github.com/>

## Install

```bash
pip install git+https://github.com/qsoyq/ghi.git

pip install git+https://github.com/qsoyq/ghi.git@main

pip install git+https://github.com/qsoyq/ghi.git@0.1.0
```

## Usage

```bash
python -m ghi --help
```

### Release

Use the version from pyproject.toml as the default release tag

```bash
python -m ghi release --help

python -m ghi release create

python -m ghi release delete
```
