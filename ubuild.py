import os
import subprocess
from uranium import task_requires


def main(build):
    build.packages.install(".", develop=True)


@task_requires("main")
def test(build):
    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    build.packages.install("pytest-asyncio")
    build.packages.install("radon")
    build.packages.install("flake8")
    build.executables.run([
        "pytest", "./tests",
        "--cov", "flakeLinter",
        "--cov-report", "term-missing",
    ] + build.options.args)
    build.executables.run([
        "flake8", "flakeLinter", "tests"
    ])


def distribute(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.executables.run([
        "python", "setup.py",
        "sdist", "bdist_wheel", "--universal", "upload"
    ])


def build_docs(build):
    build.packages.install("sphinx")
    return subprocess.call(
        ["make", "html"], cwd=os.path.join(build.root, "docs")
    )
