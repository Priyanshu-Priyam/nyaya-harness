import shlex
import subprocess
from pathlib import Path
from typing import Optional

from nyaya.tools.base import Tool


class PratyakshaTool(Tool):
    category = "pratyaksha"
    confidence_level = "direct"

    def __init__(self, workspace: str):
        self.workspace = Path(workspace).resolve()

    def _resolve(self, path: str) -> Path:
        candidate = (self.workspace / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
        if not str(candidate).startswith(str(self.workspace)):
            raise ValueError("Path is outside workspace boundary")
        return candidate


class ReadFile(PratyakshaTool):
    name = "read_file"
    description = "Read file contents, optionally with line range."
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "start_line": {"type": "integer"},
            "end_line": {"type": "integer"},
        },
        "required": ["path"],
    }

    def execute(self, path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
        target = self._resolve(path)
        if not target.exists():
            return f"ERROR: file not found: {target}"
        content = target.read_text(encoding="utf-8")
        if start_line is None and end_line is None:
            return content
        lines = content.splitlines()
        start = 1 if start_line is None else max(1, start_line)
        end = len(lines) if end_line is None else min(len(lines), end_line)
        return "\n".join(lines[start - 1 : end])


class WriteFile(PratyakshaTool):
    name = "write_file"
    description = "Write or overwrite a file."
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "content": {"type": "string"},
        },
        "required": ["path", "content"],
    }

    def execute(self, path: str, content: str) -> str:
        target = self._resolve(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"WROTE: {target}"


class RunCommand(PratyakshaTool):
    name = "run_command"
    description = "Execute a shell command in workspace with timeout."
    input_schema = {
        "type": "object",
        "properties": {
            "command": {"type": "string"},
            "timeout": {"type": "integer"},
        },
        "required": ["command"],
    }

    def execute(self, command: str, timeout: int = 30) -> str:
        try:
            result = subprocess.run(
                command,
                cwd=self.workspace,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            return f"exit_code={result.returncode}\nstdout={stdout}\nstderr={stderr}"
        except subprocess.TimeoutExpired:
            return f"ERROR: command timed out after {timeout}s"


class ListDirectory(PratyakshaTool):
    name = "list_directory"
    description = "List files under a directory."
    input_schema = {
        "type": "object",
        "properties": {"path": {"type": "string"}},
        "required": [],
    }

    def execute(self, path: str = ".") -> str:
        target = self._resolve(path)
        if not target.exists():
            return f"ERROR: path not found: {target}"
        items = sorted(str(p.relative_to(self.workspace)) for p in target.rglob("*"))
        return "\n".join(items)


class SearchFiles(PratyakshaTool):
    name = "search_files"
    description = "Search files in workspace using ripgrep."
    input_schema = {
        "type": "object",
        "properties": {"pattern": {"type": "string"}, "path": {"type": "string"}},
        "required": ["pattern"],
    }

    def execute(self, pattern: str, path: str = ".") -> str:
        target = self._resolve(path)
        cmd = f"rg -n {shlex.quote(pattern)} {shlex.quote(str(target))}"
        return RunCommand(str(self.workspace)).execute(command=cmd, timeout=30)


class RunTest(PratyakshaTool):
    name = "run_test"
    description = "Run a test command and capture output."
    input_schema = {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"],
    }

    def execute(self, command: str) -> str:
        return RunCommand(str(self.workspace)).execute(command=command, timeout=60)


class InspectState(PratyakshaTool):
    name = "inspect_state"
    description = "Inspect whether a path exists in workspace."
    input_schema = {
        "type": "object",
        "properties": {"path": {"type": "string"}},
        "required": ["path"],
    }

    def execute(self, path: str) -> str:
        target = self._resolve(path)
        return f"exists={target.exists()} path={target}"
