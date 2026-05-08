from nyaya.schemas.pancavayava import PancavayavaShell


def build_shell_plan(plan_rows: list[dict]) -> list[PancavayavaShell]:
    shells: list[PancavayavaShell] = []
    for idx, row in enumerate(plan_rows, start=1):
        shells.append(
            PancavayavaShell(
                step_id=idx,
                pratijna=row.get("pratijna", f"Step {idx}"),
                udaharana=row.get("udaharana", "Direct method"),
            )
        )
    return shells
