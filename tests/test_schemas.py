from nyaya.schemas.pancavayava import PancavayavaShell, PancavayavaStep
from nyaya.schemas.pramana import PramanaCall
from nyaya.schemas.state import SessionState


def test_schema_instantiation_and_json_roundtrip():
    shell = PancavayavaShell(step_id=1, pratijna="Create file", udaharana="Write file")
    step = PancavayavaStep(step_id=1, pratijna="Create file", hetu="Workspace", udaharana="Write file")
    call = PramanaCall(
        tool="pratyaksha.read_file",
        category="pratyaksha",
        input={"path": "a.txt"},
        output="ok",
        confidence="direct",
        used_for="hetu_validation",
    )
    step.pramana_calls.append(call)
    state = SessionState(session_id="abc123", goal="test", workspace=".")
    state.plan.append(shell)
    state.trace.append(step)

    serialized = state.model_dump_json()
    parsed = SessionState.model_validate_json(serialized)
    assert parsed.session_id == "abc123"
    assert parsed.trace[0].pramana_calls[0].tool == "pratyaksha.read_file"
