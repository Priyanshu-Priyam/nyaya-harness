from pathlib import Path

from nyaya.core.harness import NyayaHarness


def build_harness(workspace: str = ".") -> NyayaHarness:
    return NyayaHarness(workspace=str(Path(workspace).resolve()))
