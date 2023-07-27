"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve() / "src"
BLD = SRC.joinpath("..", "..", "bld").resolve()

DATA = SRC / "conjoint" / "data"
MOCK_DATA = SRC / "conjoint" / "data" / "mock_data"

__all__ = ["BLD", "SRC", "DATA", "MOCK_DATA"]
