import nox
from nox_uv import session

# Use uv as the virtualenv backend via the nox-uv plugin
nox.options.default_venv_backend = "uv"


@session(
    python=["3.11", "3.12", "3.13", "3.14", "3.14t"],
)
def tests(session: nox.Session) -> None:
    """Run test suite with pytest."""
    session.run("uv", "run", "pytest", "-q")
