"""All the general configuration of the project."""
from pathlib import Path

IN = Path(__file__).parent.resolve() / "data"
CODE = Path(__file__).parent.resolve() / "developer"
OUT = Path(__file__).parent.resolve() / "out"

MOCK_DATA = IN / "mock_data"
