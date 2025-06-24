import os
import subprocess
import sys
from time import time
from typing import Optional

from invoke import task
from rich.console import Console

console = Console()
ROOT_DIR = os.path.dirname(__file__)
SRC_DIR = "src"
BUILD_START_TIME = None

# --- Tasks ---


@task
def _build_started(c):
    global BUILD_START_TIME
    BUILD_START_TIME = time()
    console.print(
        ":factory:[bold green] initiating local build process... :factory:[/]"
    )


@task
def blackd(c):
    """
    Run black daemon.
    """
    _run_program(["blackd"])


@task
def ruff(c):
    _section_header(f"ruff")
    _log_task("ruff")
    _run_program(["ruff", "check", SRC_DIR, "--fix", "--preview"])


@task
def mypy(c):
    _section_header(f"mypy")
    _log_task("mypy")
    args = [
        "mypy",
        "--config-file",
        os.path.join(ROOT_DIR, "pyproject.toml"),
        SRC_DIR,
        "--explicit-package-bases",
        "--show-absolute-path",
        "--show-error-context",
        "--show-error-codes",
        "--pretty",
        "--color-output",
    ]
    _run_program(args)


@task
def vulture(c):
    _section_header(f"vulture")
    _log_task("vulture")
    _run_program(["vulture", SRC_DIR])


@task
def radon_analysis(c):
    _section_header(f"radon")
    _log_task("radon maintainability")
    _run_program(["radon", "mi", SRC_DIR, "--min", "C", "--show"])
    _log_task("radon complexity")
    _run_program(
        [
            "radon",
            "cc",
            SRC_DIR,
            "--average",
            "--show-complexity",
            "--min",
            "C",
            "--total-average",
        ]
    )


@task(pre=[_build_started, ruff, mypy, vulture, radon_analysis])
def build_local(c):
    duration = time() - BUILD_START_TIME
    console.print(
        f"[bold green] :raised_hands: build completed in {duration:.2f} seconds! :raised_hands: [/]"
    )


# --- Utility functions ---


def _log_task(name: str):
    console.print(f"[bold cyan]➤ Running {name}...[/]")


def _run_program(args: list[str], cwd: Optional[str] = None) -> None:
    try:
        subprocess.run(args, cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ Command failed (exit code {e.returncode})[/]")
        sys.exit(e.returncode)


def _section_header(title: str):
    console.rule(f"[bold magenta]{title}[/]", style="dim")
