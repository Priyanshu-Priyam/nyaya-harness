from pathlib import Path

from nyaya.core.harness import NyayaHarness


def test_harness_creates_hello_world_file(tmp_path: Path):
    harness = NyayaHarness(workspace=str(tmp_path))
    state = harness.run("create a file called hello.py with print('hello world')")
    target = tmp_path / "hello.py"
    assert target.exists()
    assert "hello world" in target.read_text(encoding="utf-8")
    assert state.status == "completed"
