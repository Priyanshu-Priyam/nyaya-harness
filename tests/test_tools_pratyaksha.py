from pathlib import Path

from nyaya.tools.registry import ToolRegistry


def test_read_write_and_command_tools(tmp_path: Path):
    registry = ToolRegistry(str(tmp_path))
    writer = registry.get("pratyaksha.write_file")
    reader = registry.get("pratyaksha.read_file")
    runner = registry.get("pratyaksha.run_command")
    search = registry.get("pratyaksha.search_files")

    write_call = writer.call(used_for="upanaya", path="hello.txt", content="hello")
    assert "WROTE:" in write_call.output

    read_call = reader.call(used_for="hetu_validation", path="hello.txt")
    assert read_call.output == "hello"

    cmd_call = runner.call(used_for="upanaya", command="echo hello")
    assert "stdout=hello" in cmd_call.output

    search_call = search.call(used_for="upanaya", pattern="hello", path=".")
    assert "hello.txt" in search_call.output
