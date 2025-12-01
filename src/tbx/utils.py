import pathlib
import tomllib

import click


def get_deps(path: pathlib.Path) -> list[str]:
    with open(path, "rb") as f:
        pyproject_data = tomllib.load(f)

    deps = pyproject_data["project"]["dependencies"]

    return deps


def check_path(path: pathlib.Path, force_write: bool) -> None:
    if force_write:
        pass
    else:
        if path.exists():
            click.confirm(
                f"{path} already exist. Do you want to overwrite it?", abort=True
            )

    return None
