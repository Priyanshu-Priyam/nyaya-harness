from pathlib import Path

import click

from nyaya.cli.display import HarnessDisplay
from nyaya.main import build_harness
from nyaya.state.manager import StateManager


@click.group()
def main():
    """Nyaya Agent Harness"""


@main.command()
@click.argument("task", nargs=-1, required=True)
@click.option("--workspace", "-w", default=".", help="Working directory")
@click.option("--verbose", "-v", is_flag=True, help="Show full trace")
def run(task, workspace, verbose):
    goal = " ".join(task).strip()
    display = HarnessDisplay()
    harness = build_harness(workspace=workspace)
    state = harness.run(goal)
    display.show_goal(goal)
    display.show_plan(state.plan)
    if verbose:
        display.show_trace(state)
    display.show_completion(state)


@main.command()
@click.option("--workspace", "-w", default=".", help="Working directory")
def status(workspace):
    display = HarnessDisplay()
    manager = StateManager(Path(workspace))
    state = manager.load_session()
    display.show_status(state)


@main.command(name="trace")
@click.option("--workspace", "-w", default=".", help="Working directory")
def trace_cmd(workspace):
    display = HarnessDisplay()
    manager = StateManager(Path(workspace))
    state = manager.load_session()
    display.show_trace(state)


@main.command()
@click.option("--workspace", "-w", default=".", help="Working directory")
def resume(workspace):
    display = HarnessDisplay()
    manager = StateManager(Path(workspace))
    state = manager.load_session()
    if state.status == "completed":
        click.echo("Latest session already completed.")
        return
    harness = build_harness(workspace=workspace)
    resumed = harness.run(state.goal)
    display.show_completion(resumed)
