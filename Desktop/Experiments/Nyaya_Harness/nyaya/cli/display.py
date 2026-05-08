from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from nyaya.schemas.state import SessionState


class HarnessDisplay:
    def __init__(self) -> None:
        self.console = Console()

    def show_goal(self, goal: str) -> None:
        self.console.print(Panel(goal, title="Nyaya Goal"))

    def show_plan(self, plan: list) -> None:
        table = Table(title="Plan")
        table.add_column("Step")
        table.add_column("Pratijna")
        table.add_column("Udaharana")
        for shell in plan:
            table.add_row(str(shell.step_id), shell.pratijna, shell.udaharana)
        self.console.print(table)

    def show_completion(self, state: SessionState) -> None:
        self.console.print(
            f"Completed session {state.session_id} with {len(state.trace)} steps."
        )

    def show_status(self, state: SessionState) -> None:
        self.console.print(
            f"Session={state.session_id} status={state.status} current_step={state.current_step}"
        )

    def show_trace(self, state: SessionState) -> None:
        table = Table(title=f"Trace: {state.session_id}")
        table.add_column("Step")
        table.add_column("Status")
        table.add_column("Pratijna")
        table.add_column("Nigamana")
        for step in state.trace:
            table.add_row(str(step.step_id), step.status, step.pratijna, step.nigamana or "")
        self.console.print(table)
