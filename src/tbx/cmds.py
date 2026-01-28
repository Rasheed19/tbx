import pathlib

import click

from tbx import utils


@click.command(
    help="Write the entries of pyproject.toml's dependencies table to a requirements.txt file (or a given path)"
)
@click.option(
    "--in-path",
    "-i",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, writable=False, readable=True
    ),
    default=pathlib.Path("pyproject.toml"),
    help="A complete path to the pyproject.toml file.",
    show_default=True,
)
@click.option(
    "--out-path",
    "-o",
    type=click.Path(
        exists=False, file_okay=True, dir_okay=False, writable=True, readable=True
    ),
    default=pathlib.Path("requirements.txt"),
    show_default=True,
    help="A complete path to write output to.",
)
@click.option(
    "--pkg-dir",
    "-p",
    type=click.STRING,
    default=None,
    help="If given, will add the path as where to find packages to install locally.",
    show_default=True,
)
@click.option(
    "--force-write",
    is_flag=True,
    help="Give this flag if you want to overwrite the existing file in the given path.",
)
def write_req(
    in_path: str | click.Path,
    out_path: str | click.Path,
    pkg_dir: str | None,
    force_write: bool,
) -> None:
    dependencies = []

    if pkg_dir is not None:
        check = pathlib.Path(pkg_dir)

        if not check.is_dir():
            raise click.BadOptionUsage("--pkg-path/-p", "dir is not a valid dir")

        if not check.exists():
            raise click.BadOptionUsage("--pkg-path/-p", "dir does not exist")

        dependencies.append(f"--find-links {pkg_dir}")

    in_path = pathlib.Path(in_path)
    out_path = pathlib.Path(out_path)

    utils.check_path(path=out_path, force_write=force_write)

    click.echo(f"Writing dependencies to path: {out_path}")

    dependencies.extend(utils.get_deps(in_path))

    with open(out_path, "w") as f:
        f.write("\n".join(dependencies))

    click.echo(f"Dependencies written to {out_path}.")

    return None


@click.command(help="Write given environment variables to .env file.")
@click.option(
    "--contents",
    "-c",
    type=click.Tuple([str, str]),
    nargs=2,
    required=True,
    multiple=True,
    help="The name-value pair of env variable. E.g., GU_ID abc123. Can be given multiple times.",
)
@click.option(
    "--out-path",
    "-o",
    type=click.Path(
        exists=False, file_okay=True, dir_okay=False, writable=True, readable=True
    ),
    default=pathlib.Path(".env"),
    show_default=True,
    help="A complete path to write the variables to.",
)
@click.option(
    "--force-write",
    is_flag=True,
    help="Give this flag if you want to overwrite the existing file in the given path.",
)
def write_env(
    contents: tuple[str, str], out_path: str | click.Path, force_write: bool
) -> None:
    out_path = pathlib.Path(out_path)

    utils.check_path(path=out_path, force_write=force_write)

    click.echo(f"Writing variables to path: {out_path}")

    lines = []
    for key, value in contents:
        value_fmtd = f'"{value}"'
        lines.append(f"{key}={value_fmtd}")

    with open(out_path, "w") as f:
        f.write("\n".join(lines))

    click.echo(f"Environment variables written to {out_path}.")

    return None
