Final Build Plan: Nyaya Agent Harness
Verification Checklist (Before We Begin)
I've cross-referenced every element from the architecture. Here's what must be accounted for:

┌───────────────────────────────────────────────────────────────────┐
│ CONCEPT                    │ ACCOUNTED IN          │ STATUS       │
├───────────────────────────────────────────────────────────────────┤
│ Pañcāvayava (5 members)  │ Schemas + Step Exec   │ ✓            │
│ Pramāṇas (4 tools)       │ Tool Layer            │ ✓            │
│ Hetvābhāsa (5 failures)  │ Failure Router        │ ✓            │
│ Vyāpti chain             │ Orchestration Loop    │ ✓            │
│ Sādhya-sādhana          │ Planner (backward)    │ ✓            │
│ Karaṇatā (3 validity)   │ Validity Gate         │ NEED TO ADD  │
│ Anvaya-vyatireka         │ Verification          │ NEED TO ADD  │
│ State (3-part record)     │ State Manager         │ ✓            │
│ Recovery routing          │ Failure Router        │ ✓            │
│ Forward chain (4 phases)  │ Harness Loop          │ ✓            │
│ Nigamana → Hetu link     │ Step composition      │ ✓            │
│ Tool call recording       │ PramanaCall schema    │ ✓            │
│ Failure + recovery record │ FailureRecord schema  │ ✓            │
│ Cascade check (bādhita)  │ Recovery handler      │ NEED TO ADD  │
│ Escalation (satprati.)    │ Interactive mode      │ ✓            │
│ Upstream walk (asiddha)   │ Recovery handler      │ ✓            │
│ Step revision tracking    │ State schema          │ NEED TO ADD  │
└───────────────────────────────────────────────────────────────────┘
Missing elements added to this final plan:

Karaṇatā gate — three validity conditions checked before step commits
Anvaya-vyatireka — positive AND negative verification
Cascade check — when bādhita invalidates a rule, check if other steps share it
Step revision tracking — when upstream step is re-executed, record the revision
Final Architecture Diagram
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                         NYAYA AGENT HARNESS                              │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                          CLI LAYER                                │  │
│  │   Terminal input → Goal parsing → Display → Interactive mode      │  │
│  └────────────────────────────────┬─────────────────────────────────┘  │
│                                   │                                     │
│  ┌────────────────────────────────▼─────────────────────────────────┐  │
│  │                     ORCHESTRATION LOOP                            │  │
│  │                                                                   │  │
│  │   ┌─────────┐    ┌──────────┐    ┌─────────┐    ┌──────────┐   │  │
│  │   │  PLAN   │───►│  READ    │───►│DETERMINE│───►│ EXECUTE  │   │  │
│  │   │(Phase 0)│    │(Phase 1) │    │(Phase 2)│    │(Phase 3) │   │  │
│  │   └─────────┘    └──────────┘    └─────────┘    └────┬─────┘   │  │
│  │                                                       │          │  │
│  │        ┌──────────────────────────────────────────────┘          │  │
│  │        │                                                         │  │
│  │        ▼                                                         │  │
│  │   ┌──────────┐    ┌───────────┐    ┌──────────┐                │  │
│  │   │  VERIFY  │───►│ VALIDITY  │───►│ ADVANCE  │──► next step   │  │
│  │   │(Phase 4) │    │   GATE    │    │(Phase 5) │                │  │
│  │   └────┬─────┘    │(Karaṇatā)│    └──────────┘                │  │
│  │        │           └───────────┘                                 │  │
│  │        │ FAIL                                                    │  │
│  │        ▼                                                         │  │
│  │   ┌──────────┐    ┌──────────┐    ┌──────────┐                │  │
│  │   │ CLASSIFY │───►│  ROUTE   │───►│ RECOVER  │──► replan/abort │  │
│  │   │(Phase 6a)│    │(Phase 6b)│    │(Phase 6c)│                │  │
│  │   └──────────┘    └──────────┘    └──────────┘                │  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────────┐    │
│  │  LLM CLIENT  │  │ TOOL REGISTRY│  │     STATE MANAGER         │    │
│  │              │  │  (Pramāṇas) │  │                           │    │
│  │  • plan()    │  │              │  │  • pañcāvayava trace     │    │
│  │  • execute() │  │  • pratyakṣa│  │  • epistemology log       │    │
│  │  • verify()  │  │  • anumāna  │  │  • failure/recovery       │    │
│  │  • classify()│  │  • upamāna  │  │  • revision history       │    │
│  │  • recover() │  │  • śabda    │  │                           │    │
│  └──────────────┘  └──────────────┘  └───────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
Project Structure (Final)
nyaya-harness/
├── pyproject.toml
├── README.md
├── .env.example
├── LICENSE
│
├── nyaya/
│   ├── __init__.py
│   ├── main.py                     ← build_harness(), entry point wiring
│   │
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── app.py                  ← click/typer CLI commands
│   │   ├── display.py              ← rich terminal output formatting
│   │   └── interactive.py          ← human escalation (satpratipaksha)
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── harness.py              ← orchestration loop (the heart)
│   │   ├── planner.py              ← sādhya-sādhana (backward planning)
│   │   ├── executor.py             ← phase 3 (execute single step)
│   │   ├── verifier.py             ← phase 4 (anvaya-vyatireka)
│   │   ├── validity_gate.py        ← karaṇatā (3 conditions)
│   │   └── failure_router.py       ← phase 6 (classify + route + recover)
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── client.py               ← Anthropic API wrapper
│   │   └── prompts/
│   │       ├── __init__.py
│   │       ├── plan.py             ← planning system prompt
│   │       ├── execute.py          ← execution system prompt
│   │       ├── verify.py           ← verification system prompt
│   │       ├── classify.py         ← failure classification prompt
│   │       └── recover.py          ← recovery system prompt
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── registry.py            ← tool registry + dispatch
│   │   ├── base.py                ← tool protocol/interface
│   │   ├── pratyaksha.py          ← direct observation tools
│   │   ├── anumana.py             ← inference tools (LLM-backed)
│   │   ├── upamana.py             ← pattern matching tools
│   │   └── shabda.py              ← knowledge retrieval tools
│   │
│   ├── state/
│   │   ├── __init__.py
│   │   ├── manager.py             ← state persistence + session mgmt
│   │   ├── trace.py               ← trace read/write/query operations
│   │   └── revision.py            ← step revision tracking
│   │
│   └── schemas/
│       ├── __init__.py
│       ├── pancavayava.py         ← PancavayavaStep, PancavayavaShell
│       ├── pramana.py             ← PramanaCall, tool call records
│       ├── failure.py             ← FailureType, FailureRecord
│       ├── state.py               ← SessionState, full state schema
│       └── validity.py            ← KaranataResult, validity conditions
│
├── tests/
│   ├── __init__.py
│   ├── test_schemas.py
│   ├── test_tools_pratyaksha.py
│   ├── test_tools_anumana.py
│   ├── test_harness_happy_path.py
│   ├── test_harness_failure.py
│   ├── test_validity_gate.py
│   ├── test_failure_router.py
│   ├── test_state_persistence.py
│   └── test_cli.py
│
└── examples/
    ├── simple_file_task.md         ← walkthrough: "create a hello world"
    ├── bug_fix_task.md             ← walkthrough: fix a real bug
    └── failure_recovery.md         ← walkthrough: demonstrates all 5 types
Exhaustive Build Steps
PHASE 1: Foundation (Steps 1-7)
Step 1: Project Setup
What: Create project skeleton with all directories, pyproject.toml, dependencies.

Files to create:

pyproject.toml — package name nyaya-harness, entry point nyaya = "nyaya.cli.app:main"
.env.example — ANTHROPIC_API_KEY=your-key-here
README.md — brief description
All __init__.py files
Empty placeholder files for every module listed above
Dependencies:

[project]
name = "nyaya-harness"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "anthropic>=0.40.0",
    "click>=8.0",
    "rich>=13.0",
    "pydantic>=2.0",
    "python-dotenv>=1.0",
]

[project.scripts]
nyaya = "nyaya.cli.app:main"
Test: pip install -e . succeeds, nyaya --help shows help text (even if empty).

Step 2: Schemas (Data Models)
What: Define all Pydantic models. This is the foundation everything else builds on.

File: nyaya/schemas/pramana.py

from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class PramanaCall(BaseModel):
    """Record of a single epistemology tool call."""
    tool: str                          # "pratyaksha.read_file"
    category: Literal["pratyaksha", "anumana", "upamana", "shabda"]
    input: dict                        # parameters passed
    output: str                        # what came back
    confidence: Literal["direct", "derived", "analogical", "authoritative"]
    used_for: Literal[
        "hetu_validation",             # confirming preconditions
        "udaharana_confirmation",      # confirming method applies
        "upanaya",                     # during execution
        "nigamana",                    # producing output
        "verification",                # checking output vs contract
        "failure_classification",      # diagnosing what went wrong
        "recovery"                     # fixing the problem
    ]
    timestamp: datetime = Field(default_factory=datetime.now)
File: nyaya/schemas/failure.py

from pydantic import BaseModel
from typing import Optional, Literal
from enum import Enum

class FailureType(str, Enum):
    SAVYABHICARA = "savyabhicara"       # erratic / flaky
    VIRUDDHA = "viruddha"              # wrong approach
    SATPRATIPAKSHA = "satpratipaksha"   # conflicting evidence
    ASIDDHA = "asiddha"                 # missing dependency
    BADHITA = "badhita"                 # falsified assumption

class FailureRecord(BaseModel):
    """Complete record of what failed and how it was handled."""
    type: FailureType
    description: str                    # what went wrong
    evidence: str                       # how we know
    
    # Recovery
    recovery_applied: Literal[
        "decompose_and_strengthen",     # savyabhicara
        "abandon_and_replan",           # viruddha
        "switch_pramana_and_gather",    # satpratipaksha
        "go_upstream",                  # asiddha
        "update_rule",                  # badhita
        "escalate_to_human"             # satpratipaksha fallback
    ]
    recovery_pramana: str               # which tool was used
    recovery_outcome: str               # what happened
    
    # Type-specific fields
    root_step: Optional[int] = None                 # asiddha: which upstream step
    abandoned_udaharana: Optional[str] = None        # viruddha: old approach
    new_udaharana: Optional[str] = None              # viruddha/badhita: new approach
    falsified_rule: Optional[str] = None            # badhita: what was wrong
    observation_override: Optional[str] = None       # badhita: what was actually seen
    cascade_affected_steps: Optional[list[int]] = None  # badhita: other steps with same rule
    conflicting_evidence: Optional[dict] = None     # satpratipaksha: evidence_a vs evidence_b
    decomposed_into: Optional[list[str]] = None     # savyabhicara: new substep pratijnas
File: nyaya/schemas/validity.py

from pydantic import BaseModel

class KaranataResult(BaseModel):
    """Result of the three validity conditions check."""
    
    # Pūrvavartitva: cause precedes effect
    purvavartitva: bool                 # does input exist before execution?
    purvavartitva_evidence: str         # how we confirmed
    
    # Niyatatva: cause reliably produces effect
    niyatatva: bool                     # is output consistent with rule?
    niyatatva_evidence: str             # how we confirmed
    
    # Ananyathasiddhatva: cause is genuinely necessary
    ananyathasiddhatva: bool            # was this step actually needed?
    ananyathasiddhatva_evidence: str    # how we confirmed
    
    @property
    def is_valid(self) -> bool:
        return all([
            self.purvavartitva, 
            self.niyatatva, 
            self.ananyathasiddhatva
        ])
File: nyaya/schemas/pancavayava.py

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from .pramana import PramanaCall
from .failure import FailureRecord
from .validity import KaranataResult

class PancavayavaShell(BaseModel):
    """Plan-time step: only pratijna and udaharana filled."""
    step_id: int
    pratijna: str                       # output contract
    udaharana: str                       # planned method/rule
    
class PancavayavaStep(BaseModel):
    """Complete step record after execution."""
    step_id: int
    
    # ─── The Five Members ───
    pratijna: str                        # what I claim I'll produce (BEFORE)
    hetu: str                            # what I have + why method applies (BEFORE)
    udaharana: str                        # the rule I rely on (BEFORE)
    upanaya: Optional[str] = None        # what I actually did (DURING)
    nigamana: Optional[str] = None       # what I actually got (AFTER)
    
    # ─── Verification ───
    verification: Optional[Literal["PASS", "FAIL"]] = None
    validity: Optional[KaranataResult] = None
    
    # ─── Epistemology Log ───
    pramana_calls: list[PramanaCall] = Field(default_factory=list)
    
    # ─── Failure/Recovery ───
    failure: Optional[FailureRecord] = None
    
    # ─── Revision Tracking ───
    revised: bool = False
    revision_reason: Optional[str] = None
    revision_timestamp: Optional[datetime] = None
    previous_nigamana: Optional[str] = None  # what it said before revision
    
    # ─── Metadata ───
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: Literal["planned", "executing", "passed", "failed", "revised"] = "planned"
File: nyaya/schemas/state.py

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from .pancavayava import PancavayavaStep, PancavayavaShell

class SessionState(BaseModel):
    """Complete harness state for a single task execution."""
    session_id: str
    goal: str
    workspace: str                      # directory path
    
    # Plan
    plan: list[PancavayavaShell] = Field(default_factory=list)
    
    # Execution state
    current_step: int = 0
    status: Literal[
        "planning", "executing", "recovering", 
        "completed", "failed", "paused"
    ] = "planning"
    
    # Completed trace (the core record)
    trace: list[PancavayavaStep] = Field(default_factory=list)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    total_pramana_calls: int = 0
    total_failures: int = 0
    total_recoveries: int = 0
Test: All schemas instantiate correctly. Serialization to/from JSON works.

Step 3: Tool Base + Pratyaksha Tools
What: Build the tool interface and the direct-observation tools (most critical, used everywhere).

File: nyaya/tools/base.py

from abc import ABC, abstractmethod
from nyaya.schemas.pramana import PramanaCall
from datetime import datetime

class Tool(ABC):
    """Base interface for all pramāṇa tools."""
    
    category: str       # "pratyaksha" | "anumana" | "upamana" | "shabda"
    name: str           # "read_file" | "run_command" | etc.
    description: str    # for LLM tool-use description
    confidence_level: str  # "direct" | "derived" | "analogical" | "authoritative"
    
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Run the tool. Return string result."""
        pass
    
    def call(self, used_for: str, **kwargs) -> PramanaCall:
        """Execute the tool and return a structured record."""
        output = self.execute(**kwargs)
        return PramanaCall(
            tool=f"{self.category}.{self.name}",
            category=self.category,
            input=kwargs,
            output=output,
            confidence=self.confidence_level,
            used_for=used_for,
            timestamp=datetime.now()
        )
    
    def to_llm_tool_spec(self) -> dict:
        """Convert to Anthropic tool-use format for the LLM."""
        # Returns the tool definition that Claude can call
        pass
File: nyaya/tools/pratyaksha.py

Implements these tools:

ReadFile — read file contents (optionally line range)
WriteFile — write/overwrite file
RunCommand — execute shell command with timeout
ListDirectory — list directory tree
SearchFiles — grep/ripgrep search
RunTest — run a test command and parse result
InspectState — read from the harness state directly (for upstream verification)
Each tool:

Has proper error handling (file not found, timeout, permission denied)
Returns structured string output
Has a clear description for LLM tool-use
File: nyaya/tools/registry.py

class ToolRegistry:
    """Registry of all available tools. Dispatch by name."""
    
    def __init__(self, workspace: str):
        self.workspace = workspace
        self._tools: dict[str, Tool] = {}
        self._register_defaults()
    
    def _register_defaults(self):
        # Register all pratyaksha tools
        # (anumana, upamana, shabda added in later phases)
        pass
    
    def get(self, tool_name: str) -> Tool:
        """Get tool by full name like 'pratyaksha.read_file'"""
        pass
    
    def list_available(self) -> list[dict]:
        """Return all tools in LLM tool-use format."""
        pass
    
    def list_by_category(self, category: str) -> list[Tool]:
        pass
Test:

read_file reads a real file
write_file writes and content is verifiable
run_command executes echo hello and returns "hello"
search_files finds known patterns
All return PramanaCall records with correct structure
Step 4: LLM Client (Basic)
What: Wrapper around Anthropic API. Structured calls for each harness phase.

File: nyaya/llm/client.py

class LLMClient:
    def __init__(self, api_key: str = None, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    def plan(self, goal: str, context: str) -> list[dict]:
        """Phase 0: Decompose goal into step shells."""
        # Uses PLAN_SYSTEM prompt
        # Returns list of {pratijna, udaharana}
        pass
    
    def determine_method(self, step: dict, current_state: str) -> dict:
        """Phase 2: Confirm/update method given current state."""
        # Returns {udaharana: str, reasoning: str, proceed: bool}
        pass
    
    def execute_step(self, step: dict, tools: list[dict]) -> dict:
        """Phase 3: Decide and make tool calls."""
        # Uses Anthropic tool-use API
        # Returns {tool_calls: [...], nigamana: str}
        pass
    
    def verify(self, pratijna: str, nigamana: str, context: str) -> dict:
        """Phase 4: Check output against contract."""
        # Returns {passes: bool, reason: str}
        pass
    
    def classify_failure(self, step: dict, trace: list) -> dict:
        """Phase 6a: Classify failure type."""
        # Returns {type: str, evidence: str, suggested_recovery: str}
        pass
    
    def plan_recovery(self, failure_type: str, step: dict, trace: list) -> dict:
        """Phase 6c: Generate recovery plan."""
        # Returns {action: str, tool_calls: [...], new_plan: [...]}
        pass
Key design decision: The LLM client uses Anthropic's native tool use feature. When execute_step is called, the LLM receives the available tools as Anthropic tool definitions, and the LLM responds with tool_use blocks. The client then dispatches those to the tool registry.

Test:

plan() returns structured list given a simple goal
verify() correctly identifies pass/fail on trivial cases
Step 5: State Manager
What: Persistence layer. Reads/writes .nyaya/ directory.

File: nyaya/state/manager.py

class StateManager:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.nyaya_dir = workspace / ".nyaya"
        self.traces_dir = self.nyaya_dir / "traces"
        self._ensure_dirs()
        self.session: Optional[SessionState] = None
    
    def new_session(self, goal: str) -> SessionState:
        """Create new session, assign ID, persist."""
        pass
    
    def load_session(self, session_id: str = None) -> SessionState:
        """Load existing session (latest if no ID given)."""
        pass
    
    def save(self):
        """Persist current state to disk."""
        pass
    
    def set_plan(self, plan: list[PancavayavaShell]):
        pass
    
    def get_current_step_shell(self) -> PancavayavaShell:
        pass
    
    def commit_step(self, step: PancavayavaStep):
        """Add completed step to trace. Auto-save."""
        pass
    
    def advance(self):
        """Move to next step."""
        pass
    
    def revise_step(self, step_id: int, new_nigamana: str, reason: str):
        """Mark a previous step as revised (for asiddha recovery)."""
        pass
    
    def replace_plan_from(self, step_id: int, new_steps: list[PancavayavaShell]):
        """Replace plan from step_id onward (for viruddha/badhita recovery)."""
        pass
    
    def insert_substeps(self, after_step_id: int, substeps: list[PancavayavaShell]):
        """Insert new substeps (for savyabhicara decomposition)."""
        pass
File: nyaya/state/trace.py

class TraceQuery:
    """Query operations on the completed trace."""
    
    def get_step(self, step_id: int) -> PancavayavaStep:
        pass
    
    def get_last_nigamana(self) -> str:
        pass
    
    def find_steps_with_udaharana(self, rule: str) -> list[int]:
        """For bādhita cascade check: which steps used this rule?"""
        pass
    
    def walk_upstream(self, from_step: int) -> Iterator[PancavayavaStep]:
        """For asiddha recovery: walk backward through trace."""
        pass
    
    def get_all_pramana_calls(self) -> list[PramanaCall]:
        """All tool calls across all steps."""
        pass
Persistence format: JSON files in .nyaya/

.nyaya/
├── current_session.json          ← pointer to active session
├── config.json                   ← user preferences
└── traces/
    ├── session_abc123.json       ← complete SessionState
    └── session_def456.json
Test:

Create session, commit steps, reload from disk — state matches
revise_step correctly tracks previous value
replace_plan_from correctly truncates and replaces
Step 6: Minimal Harness Loop (No Verification Yet)
What: Wire together LLM + Tools + State in the basic forward chain. Plan → Execute → Record. No verification, no failure handling yet.

File: nyaya/core/harness.py

Implement only:

Phase 0 (Plan): call llm.plan(), store shells
Phase 1 (Read): load previous nigamana into hetu
Phase 2 (Determine): call llm.determine_method(), confirm udaharana
Phase 3 (Execute): call llm.execute_step(), dispatch tool calls, record upanaya
Phase 5 (Advance): commit step, move to next
Skip Phase 4 (Verify) and Phase 6 (Failure) — just auto-advance.

Test:

nyaya run "list all python files in this directory and count them"
Should: plan 1-2 steps, execute them, show results. No verification.

Step 7: CLI Entry Point
What: Working terminal interface. User types task, agent executes.

File: nyaya/cli/app.py

@click.group()
def main():
    """Nyaya Agent Harness"""
    pass

@main.command()
@click.argument("task", nargs=-1, required=True)
@click.option("--workspace", "-w", default=".", help="Working directory")
@click.option("--verbose", "-v", is_flag=True, help="Show full trace")
def run(task, workspace, verbose):
    """Execute a task. Example: nyaya run fix the login bug"""
    pass

@main.command()
def status():
    """Show current session status."""
    pass

@main.command()
def trace():
    """Display full trace of last session."""
    pass

@main.command() 
def resume():
    """Resume a paused session."""
    pass
File: nyaya/cli/display.py

Use rich for:
Goal panel at top
Plan display (numbered steps with pratijñā)
Step execution progress (tool calls as they happen)
Pass/fail indicators
Failure classification display
Trace table view
Test:

nyaya run "create a file called hello.py with print('hello world')"
Should: show plan, execute, display result, file exists on disk.

PHASE 2: Verification (Steps 8-12)
Step 8: Verifier (Anvaya-Vyatireka)
What: Implement Phase 4. Not just "does nigamana match pratijñā" but the full anvaya-vyatireka: positive co-presence AND negative co-absence.

File: nyaya/core/verifier.py

class Verifier:
    """Implements anvaya-vyatireka verification."""
    
    def __init__(self, llm: LLMClient, tools: ToolRegistry):
        self.llm = llm
        self.tools = tools
    
    def verify(self, step: PancavayavaStep, next_step_shell: Optional[PancavayavaShell]) -> VerificationResult:
        """
        Full anvaya-vyatireka:
        1. Anvaya (positive): nigamana satisfies pratijñā?
        2. Vyatireka (negative): if we hadn't executed, would this output exist anyway?
        3. Upādhi check: is there a confounding condition?
        """
        
        # CHECK 1: ANVAYA (positive co-presence)
        # "When the step executed with these inputs and this method,
        #  did the expected output appear?"
        anvaya_result = self._check_anvaya(step)
        
        # CHECK 2: VYATIREKA (negative co-absence)  
        # "Is the output genuinely caused by this step, or would it 
        #  exist regardless?" (e.g., file already existed before write)
        vyatireka_result = self._check_vyatireka(step)
        
        # CHECK 3: UPĀDHI (confounding condition)
        # "Could something else have produced this output?"
        # (e.g., another process wrote the file)
        upadhi_result = self._check_upadhi(step)
        
        # CHECK 4: COMPOSABILITY
        # "Does nigamana feed the next step's hetu?"
        composability_result = self._check_feeds_next(step, next_step_shell)
        
        return VerificationResult(
            anvaya=anvaya_result,
            vyatireka=vyatireka_result,
            upadhi=upadhi_result,
            composability=composability_result,
            overall_pass=all([anvaya_result.passes, composability_result.passes])
            # vyatireka and upadhi are warnings, not hard failures
        )
    
    def _check_anvaya(self, step) -> CheckResult:
        """Does nigamana match pratijñā?"""
        # Call LLM: compare nigamana text against pratijna contract
        # OR if pratijna has testable criteria, run pratyaksha.run_test
        pass
    
    def _check_vyatireka(self, step) -> CheckResult:
        """Could the output exist without this step?"""
        # For file writes: did the file exist before?
        # For commands: is the output new?
        # This is often a pratyaksha check
        pass
    
    def _check_upadhi(self, step) -> CheckResult:
        """Is there a confounding condition?"""
        # Call LLM: "Could anything else have produced this output?"
        # Usually lightweight — just flags potential confounders
        pass
    
    def _check_feeds_next(self, step, next_shell) -> CheckResult:
        """Does this nigamana provide what the next step needs?"""
        # If last step: check against goal instead
        # Call LLM: "Does this output satisfy the preconditions of next step?"
        pass
Design note: Vyatireka and upādhi checks are "soft" — they produce warnings but don't block advancement. Only anvaya (positive match) and composability (feeds next step) are hard gates.

Test:

Step that produces what it claims → PASS
Step whose nigamana contradicts pratijna → FAIL
Step that produces correct output but can't feed next step → FAIL
Step 9: Validity Gate (Karaṇatā)
What: The three validity conditions checked before a step is committed.

File: nyaya/core/validity_gate.py

class ValidityGate:
    """
    Implements karaṇatā — the three conditions for a step 
    to be a genuine causal link in the chain.
    """
    
    def check(self, step: PancavayavaStep, trace: list, plan: list) -> KaranataResult:
        """
        Check all three conditions.
        Called AFTER verification passes, BEFORE commit.
        """
        
        # 1. PŪRVAVARTITVA: Cause precedes effect
        # "Did the input exist and was it fully written before execution started?"
        purva = self._check_purvavartitva(step, trace)
        
        # 2. NIYATATVA: Cause reliably produces effect
        # "Is this step's method reliable? Would it produce the same output again?"
        niyata = self._check_niyatatva(step)
        
        # 3. ANANYATHASIDDHATVA: Cause is genuinely necessary
        # "Was this step actually needed? Did it contribute something 
        #  that wasn't already present?"
        ananya = self._check_ananyathasiddhatva(step, trace, plan)
        
        return KaranataResult(
            purvavartitva=purva.valid,
            purvavartitva_evidence=purva.evidence,
            niyatatva=niyata.valid,
            niyatatva_evidence=niyata.evidence,
            ananyathasiddhatva=ananya.valid,
            ananyathasiddhatva_evidence=ananya.evidence,
        )
    
    def _check_purvavartitva(self, step, trace):
        """
        For sequential execution: trivially satisfied 
        (we read state before executing).
        
        For future parallel execution: must verify 
        that all dependencies are committed.
        """
        # Check: does step.hetu reference a nigamana that exists in trace?
        # For step 1: hetu comes from initial state (always present)
        pass
    
    def _check_niyatatva(self, step):
        """
        Is the output consistent with what the udāharaṇa predicts?
        Would running this step again produce the same result?
        
        Note: This is not re-execution. It's a consistency check.
        "Given this input + this method, does this output make sense?"
        """
        # LLM check: "Is this nigamana a reasonable output of 
        # applying this udaharana to this hetu?"
        pass
    
    def _check_ananyathasiddhatva(self, step, trace, plan):
        """
        Was this step genuinely necessary?
        Could the next step have proceeded without this one?
        
        Note: This is checked AFTER the fact. If a step turns out 
        to be unnecessary, flag it for future plan optimization.
        Not a hard failure — just a signal.
        """
        # LLM check: "Could step i+1 have proceeded with only 
        # what was available before step i?"
        pass
Integration: In harness loop, after verification passes:

if verification.overall_pass:
    validity = self.validity_gate.check(step, trace, plan)
    if validity.is_valid:
        step.validity = validity
        self.state.commit_step(step)
        return "advance"
    else:
        # Validity failed — this is unusual
        # Most likely ananyathasiddhatva (unnecessary step)
        # Log warning, still advance, but flag for plan optimization
        ...
Test:

Step with verified upstream nigamana → pūrvavartitva passes
Step whose output contradicts its method → niyatatva fails
Step that produces nothing new → ananyathasiddhatva fails (warning)
Step 10: Wire Verification + Validity into Harness
What: Update the harness loop to include Phase 4 (Verify) and the validity gate.

Update nyaya/core/harness.py:

The _execute_cycle method now has the full flow:

READ → DETERMINE → EXECUTE → VERIFY → VALIDITY GATE → ADVANCE
                                  ↓ (fail)
                            CLASSIFY → ROUTE → RECOVER
Test:

nyaya run "create a file called test.py that prints hello"
Should show verification step in output
Should show validity check passing
Step committed with full record
# Force a failure: ask it to read a nonexistent file
nyaya run "read the contents of /nonexistent/path.txt and summarize them"
Should fail at verification
Currently just shows FAIL (no recovery yet — that's Phase 3)
Step 11: State Persistence + Resume
What: Full session save/load. Resume interrupted sessions.

Update StateManager to:

Auto-save after every step commit
Save on any status change
The resume command loads last session and continues from current_step
File: nyaya/state/revision.py

class RevisionTracker:
    """Track when steps are revised during recovery."""
    
    def record_revision(self, step_id: int, original_nigamana: str, 
                        new_nigamana: str, reason: str, triggered_by_step: int):
        """Record that a step was revised."""
        pass
    
    def get_revisions(self) -> list[dict]:
        """All revisions in this session."""
        pass
    
    def was_revised(self, step_id: int) -> bool:
        pass
Test:

Start a task, Ctrl+C mid-execution
nyaya resume picks up at the right step
State file on disk matches in-memory state
Step 12: Trace Display
What: nyaya trace command shows the full pañcāvayava trace with epistemology log and failures.

File: nyaya/cli/display.py — add trace formatting:

╭─── Session abc123 ─── Goal: Fix login bug ───────────────────╮
│ Status: COMPLETED │ Steps: 4/4 │ Failures: 1 │ Recoveries: 1 │
╰──────────────────────────────────────────────────────────────╯

┌─ Step 1 ─────────────────────────────────────── ✅ PASS ─────┐
│ Pratijñā:  Describe bug trigger → actual → expected          │
│ Hetu:      Issue text (initial state)                         │
│ Udāharaṇa: Restate issue as trigger/actual/expected          │
│ Upanaya:   pratyaksha.read_file(ISSUE.md)                    │
│ Nigamana:  + in email → 400 error → should succeed           │
│ Validity:  ✓ pūrva  ✓ niyata  ✓ ananya                     │
│ Tools:     pratyaksha.read_file [direct] → hetu_validation   │
└───────────────────────────────────────────────────────────────┘

┌─ Step 4 ─────────────────────────────────────── ❌ FAIL ─────┐
│ Pratijñā:  All tests pass                                     │
│ Nigamana:  1 test failed                                      │
│ Failure:   ASIDDHA — step 3 claimed write but file wrong      │
│ Recovery:  go_upstream → pratyaksha.read_file → re-wrote      │
│ Outcome:   Step 3 revised, re-ran step 4 → PASS              │
└───────────────────────────────────────────────────────────────┘
Test: nyaya trace renders correctly after a completed session.

PHASE 3: Failure Handling (Steps 13-18)
Step 13: Failure Classifier
What: Given a failed step + trace, classify into one of five types.

File: nyaya/core/failure_router.py (classification part)

Prompt (nyaya/llm/prompts/classify.py):

CLASSIFY_SYSTEM = """You are a failure diagnostician. A step in a causal 
chain has failed. Your job is to classify the failure into exactly ONE type.

THE FIVE TYPES:

1. SAVYABHICARA (erratic)
   - Signal: Non-deterministic output. Same inputs → different results.
   - Example: Test passes sometimes, fails sometimes. API returns 
     different data on retry.
   - Key question: "If I ran this exact step again with exact same 
     inputs, would I get the same failure?" If NO → savyabhicara.

2. VIRUDDHA (wrong approach)  
   - Signal: Step executes RELIABLY but output moves AWAY from goal.
   - Example: "I applied the fix consistently and it made things worse."
   - Key question: "Is the method itself the problem, not the execution?"
     If YES → viruddha.

3. SATPRATIPAKSHA (conflicting evidence)
   - Signal: Two legitimate sources contradict each other.
   - Example: Local test passes, CI fails. Docs say X, runtime shows Y.
   - Key question: "Do I have contradictory evidence where both sources 
     seem legitimate?" If YES → satpratipaksha.

4. ASIDDHA (ungrounded/missing dependency)
   - Signal: Step assumed something exists that doesn't.
   - Example: Step 5 uses output of step 4, but step 4's output is 
     wrong/missing/different from what step 5 assumed.
   - Key question: "Did a previous step fail to produce what this step 
     needs?" If YES → asiddha.

5. BADHITA (falsified assumption)
   - Signal: Direct observation contradicts the rule being applied.
   - Example: "I assumed the API returns JSON, but it returns XML."
     The assumption (udāharaṇa) is empirically wrong.
   - Key question: "Has direct observation falsified a rule I was 
     relying on?" If YES → badhita.

You have access to:
- The failed step's full pañcāvayava (pratijna, hetu, udaharana, upanaya, nigamana)
- The trace of all previous steps
- The verification failure reason

Output:
{
  "type": "one of: savyabhicara, viruddha, satpratipaksha, asiddha, badhita",
  "confidence": "high" | "medium" | "low",
  "evidence": "why you classified it this way",
  "details": {
    // type-specific fields
    "root_step": int,              // for asiddha
    "falsified_rule": string,      // for badhita
    "conflicting_sources": [...],  // for satpratipaksha
    "retry_prediction": string     // for savyabhicara
  }
}"""
The classifier also does a detection step for savyabhicara: Before classifying, if the failure could be erratic, actually retry the execution once:

def _detect_savyabhicara(self, step) -> bool:
    """Run the same step again. If output differs, it's erratic."""
    retry_result = self.tools.get(step.last_tool_call).call(...)
    return retry_result.output != step.nigamana
Test:

Give it a step that got different output on retry → classifies as savyabhicara
Give it a step where upstream nigamana is missing → classifies as asiddha
Give it a step where method produces opposite of goal → classifies as viruddha
Step 14: Recovery Handlers (One Per Type)
What: Each failure type has its own recovery implementation.

File: nyaya/core/failure_router.py (recovery part)

class FailureRouter:
    
    def handle(self, step: PancavayavaStep, classification: dict) -> RecoveryResult:
        """Route to correct handler based on type."""
        handlers = {
            FailureType.SAVYABHICARA: self._recover_savyabhicara,
            FailureType.VIRUDDHA: self._recover_viruddha,
            FailureType.SATPRATIPAKSHA: self._recover_satpratipaksha,
            FailureType.ASIDDHA: self._recover_asiddha,
            FailureType.BADHITA: self._recover_badhita,
        }
        return handlers[classification.type](step, classification)
Recovery: SAVYABHICĀRA (decompose + strengthen)

def _recover_savyabhicara(self, step, classification) -> RecoveryResult:
    """
    The step is flaky. Decompose it into smaller, more reliable substeps.
    
    1. Use anumāna to identify WHY it's flaky (what part varies?)
    2. Decompose into substeps where each is individually reliable
    3. Insert substeps into plan, replacing the flaky step
    """
    # Tool: anumana.trace_dependency — find variance source
    variance_analysis = self.tools.get("anumana.trace_dependency").call(
        used_for="recovery",
        symptom=f"Step {step.step_id} produces different outputs on same inputs",
        context=step.upanaya
    )
    
    # Ask LLM to decompose
    substeps = self.llm.plan_recovery(
        failure_type="savyabhicara",
        step=step,
        analysis=variance_analysis.output
    )
    
    # Insert substeps into plan
    self.state.insert_substeps(step.step_id, substeps)
    
    return RecoveryResult(
        action="decompose_and_strengthen",
        pramana_used="anumana.trace_dependency",
        outcome=f"Decomposed into {len(substeps)} substeps",
        next="replan"  # re-execute from the new first substep
    )
Recovery: VIRUDDHA (abandon + replan)

def _recover_viruddha(self, step, classification) -> RecoveryResult:
    """
    The approach is wrong. Don't retry — find a different approach.
    
    1. Use upamāna to find similar problems with different solutions
       OR use śabda to read docs for alternative approaches
    2. Generate new udāharaṇa (method)
    3. Replace plan from this step onward
    """
    # Try upamana first
    similar = self.tools.get("upamana.find_similar").call(
        used_for="recovery",
        description=f"Step failed because approach '{step.udaharana}' "
                   f"moves away from goal. Need different approach.",
        context=step.hetu
    )
    
    # If upamana doesn't help, try shabda
    if not similar.output or "no similar case found" in similar.output:
        docs = self.tools.get("shabda.read_docs").call(
            used_for="recovery",
            topic=f"alternative approaches to: {step.pratijna}"
        )
        basis = docs.output
        pramana_used = "shabda.read_docs"
    else:
        basis = similar.output
        pramana_used = "upamana.find_similar"
    
    # Ask LLM to replan with new approach
    new_plan = self.llm.plan_recovery(
        failure_type="viruddha",
        step=step,
        alternative_basis=basis
    )
    
    # Replace plan from this step onward
    self.state.replace_plan_from(step.step_id, new_plan)
    
    return RecoveryResult(
        action="abandon_and_replan",
        pramana_used=pramana_used,
        outcome=f"New approach: {new_plan[0]['udaharana']}",
        abandoned_udaharana=step.udaharana,
        next="replan"
    )
Recovery: SATPRATIPAKṢA (gather more evidence or escalate)

def _recover_satpratipaksha(self, step, classification) -> RecoveryResult:
    """
    Conflicting evidence. Don't commit to either side.
    
    1. Switch pramāṇa mode (if was using anumāna, try pratyakṣa)
    2. Gather additional evidence from a different source
    3. If still unresolvable → escalate to human
    """
    evidence_a = classification.details.get("evidence_a", "")
    evidence_b = classification.details.get("evidence_b", "")
    
    # Strategy: use a DIFFERENT tool category than what produced the conflict
    # Find which pramana categories were used in the conflicting checks
    used_categories = {call.category for call in step.pramana_calls 
                       if call.used_for == "verification"}
    
    # Switch to unused category
    if "pratyaksha" not in used_categories:
        # Try direct observation
        resolution = self.tools.get("pratyaksha.run_command").call(
            used_for="recovery",
            command=...  # LLM decides what to run
        )
    elif "shabda" not in used_categories:
        # Consult authoritative source
        resolution = self.tools.get("shabda.query_spec").call(
            used_for="recovery",
            interface=...
        )
    else:
        # All categories tried → escalate
        return self._escalate_to_human(step, evidence_a, evidence_b)
    
    # Check if resolution breaks the tie
    tie_broken = self.llm.verify(...)
    
    if tie_broken:
        return RecoveryResult(action="switch_pramana_and_gather", ...)
    else:
        return self._escalate_to_human(step, evidence_a, evidence_b)

def _escalate_to_human(self, step, evidence_a, evidence_b) -> RecoveryResult:
    """Pause execution and ask the human."""
    # Set state to "paused"
    # Display conflict to terminal
    # Wait for human input
    # Resume based on human decision
    ...
Recovery: ASIDDHA (go upstream)

def _recover_asiddha(self, step, classification) -> RecoveryResult:
    """
    Missing dependency. A previous step didn't actually produce what 
    this step needs.
    
    1. Walk backward through trace using pratyakṣa
    2. Find the step whose nigamana is wrong/missing
    3. Re-execute that step
    4. Update its trace entry (revision tracking)
    5. Re-execute current step
    """
    root_step_id = classification.details.get("root_step")
    
    if root_step_id is None:
        # LLM didn't identify it — walk backward ourselves
        for prev_step in self.state.trace.walk_upstream(step.step_id):
            # Verify each upstream nigamana with pratyaksha
            check = self.tools.get("pratyaksha.inspect_state").call(
                used_for="recovery",
                variable=prev_step.nigamana
                # e.g., if nigamana says "file written", check file exists
            )
            if "not found" in check.output or "mismatch" in check.output:
                root_step_id = prev_step.step_id
                break
    
    if root_step_id is None:
        # Can't find the gap — escalate
        return RecoveryResult(action="escalate", next="abort")
    
    # Re-execute the root step
    root_step = self.state.get_step(root_step_id)
    original_nigamana = root_step.nigamana
    
    # ... re-run execution for that step ...
    
    # Record revision
    self.state.revise_step(
        step_id=root_step_id,
        new_nigamana=new_result,
        reason=f"asiddha detected at step {step.step_id}"
    )
    
    return RecoveryResult(
        action="go_upstream",
        pramana_used="pratyaksha.inspect_state",
        outcome=f"Revised step {root_step_id}. Re-executing step {step.step_id}.",
        root_step=root_step_id,
        next="replan"  # re-execute current step with corrected upstream
    )
Recovery: BĀDHITA (update rule + cascade check)

def _recover_badhita(self, step, classification) -> RecoveryResult:
    """
    Direct observation contradicts the rule. The world doesn't work 
    the way we assumed.
    
    1. Accept observation (pratyakṣa overrides anumāna)
    2. Formulate new rule from observation
    3. CASCADE CHECK: find other steps that relied on the old rule
    4. Replan affected steps
    """
    falsified_rule = classification.details.get("falsified_rule", step.udaharana)
    observation = step.nigamana  # what was actually seen
    
    # Accept observation
    # LLM: "Given that we observed X, what is the correct rule?"
    new_rule = self.llm.plan_recovery(
        failure_type="badhita",
        step=step,
        observation=observation,
        old_rule=falsified_rule
    )
    
    # CASCADE CHECK: which other steps in the plan used the same rule?
    affected_steps = self.state.trace.find_steps_with_udaharana(falsified_rule)
    
    # Also check FUTURE planned steps
    affected_future = [s for s in self.state.plan 
                       if s.udaharana == falsified_rule 
                       and s.step_id > step.step_id]
    
    # Replan from current step with new rule
    # Also flag affected past steps (they may need re-verification)
    self.state.replace_plan_from(step.step_id, new_plan_with_updated_rule)
    
    return RecoveryResult(
        action="update_rule",
        pramana_used="pratyaksha (overriding)",
        outcome=f"Rule updated. Old: '{falsified_rule}'. New: '{new_rule}'",
        falsified_rule=falsified_rule,
        new_rule=new_rule,
        cascade_affected_steps=affected_steps + [s.step_id for s in affected_future],
        next="replan"
    )
Test:

Simulate each failure type with a crafted step + trace
Verify correct handler is invoked
Verify state is updated with full failure record
Verify recovery actions produce the expected plan modifications
Step 15: Wire Failure Router into Harness
What: Update harness loop. When verification fails → classify → route → recover.

# In harness._execute_cycle:

if not verification.overall_pass:
    step.verification = "FAIL"
    
    # Phase 6a: Classify
    classification = self.failure_router.classify(step, self.state.trace)
    
    # Phase 6b+6c: Route + Recover
    recovery = self.failure_router.handle(step, classification)
    
    # Record in state
    step.failure = FailureRecord(
        type=classification.type,
        description=classification.evidence,
        evidence=classification.details,
        recovery_applied=recovery.action,
        recovery_pramana=recovery.pramana_used,
        recovery_outcome=recovery.outcome,
        # type-specific fields
        root_step=recovery.root_step,
        abandoned_udaharana=recovery.abandoned_udaharana,
        # ... etc
    )
    
    # Commit the failed step (with failure record)
    self.state.commit_step(step)
    self.state.total_failures += 1
    self.state.total_recoveries += 1
    
    if recovery.next == "replan":
        # Plan has been modified by recovery handler
        # Reset current_step to the appropriate position
        return "replan"
    elif recovery.next == "abort":
        return "abort"
Add retry budget:

MAX_FAILURES_PER_STEP = 3
MAX_TOTAL_FAILURES = 10

# If same step fails 3 times → abort that step
# If total failures exceed 10 → abort session
Test:

# Task that will hit asiddha:
nyaya run "read config.yaml and update the database host to localhost"
# (if config.yaml doesn't exist)

# Task that will hit badhita:
nyaya run "call the /api/users endpoint and parse the JSON response"
# (if endpoint returns XML)
Step 16: Failure/Recovery State Recording
What: Ensure every failure and recovery is fully recorded in state AND visible in trace output.

This is already handled by the FailureRecord schema and the commit logic, but verify:

Failed step is committed to trace with verification: "FAIL" and full failure record
Recovery tool calls are recorded with used_for: "recovery"
If upstream step is revised, revision is tracked
If plan is modified, the old plan is preserved in state (for audit)
nyaya trace shows failures inline with their recovery
Add to state:

class SessionState(BaseModel):
    ...
    # Audit trail
    plan_revisions: list[dict] = []  # {timestamp, reason, old_plan, new_plan}
Test: After a failure+recovery session, the trace file on disk contains the complete narrative of what failed, why, what was tried, and what worked.

Step 17: Anumāna + Upamāna + Śabda Tools
What: Implement the remaining three pramāṇa categories.

File: nyaya/tools/anumana.py

These are LLM-backed tools. The tool calls the LLM with a specific inference prompt.

class InferCause(Tool):
    category = "anumana"
    name = "infer_cause"
    confidence_level = "derived"
    description = "Given an observation, infer the most likely cause."
    
    def execute(self, observation: str, context: str = "") -> str:
        response = self.llm.call(
            system="You are a causal reasoning engine. Given an observation, "
                   "infer the most likely cause. Be specific and grounded.",
            user=f"Observation: {observation}\nContext: {context}\n\nMost likely cause:"
        )
        return response

class InferEffect(Tool):
    """Predict what will happen if an action is taken."""
    ...

class TraceDependency(Tool):
    """Trace a symptom back to its root cause through dependencies."""
    ...

class AnalyzeDiff(Tool):
    """Given before/after state, identify what changed and why."""
    ...
File: nyaya/tools/upamana.py

Pattern matching against past traces and known patterns.

class FindSimilar(Tool):
    category = "upamana"
    name = "find_similar"
    confidence_level = "analogical"
    description = "Find similar past issues/solutions in trace history."
    
    def execute(self, description: str, history: str = "") -> str:
        # Search past session traces for similar failures/solutions
        # Use LLM to assess structural similarity
        past_traces = self.state_manager.load_all_traces()
        # ... match against description ...
        pass

class MatchErrorPattern(Tool):
    """Match an error against known error patterns."""
    ...

class StructuralAnalogy(Tool):
    """Find structural analogies between current situation and known cases."""
    ...
File: nyaya/tools/shabda.py

Knowledge retrieval from authoritative sources.

class ReadDocs(Tool):
    category = "shabda"
    name = "read_docs"
    confidence_level = "authoritative"
    description = "Read documentation or specification files."
    
    def execute(self, topic: str, path: str = None) -> str:
        # Search for README, docs/, .md files related to topic
        # Read and return relevant sections
        pass

class QuerySpec(Tool):
    """Look up API specifications, interface contracts."""
    ...

class SearchKnowledgeBase(Tool):
    """Search project-wide knowledge (past traces, docs, specs)."""
    ...

class ConsultHistory(Tool):
    """Look at past session decisions for guidance."""
    ...
Test: Each tool returns a PramanaCall with correct category and confidence level.

Step 18: Interactive Mode (Satpratipakṣa Escalation)
What: When the agent hits satpratipakṣa and can't resolve it, pause and ask the human.

File: nyaya/cli/interactive.py

class InteractiveEscalation:
    """Handle human-in-the-loop for unresolvable conflicts."""
    
    def escalate(self, step: PancavayavaStep, evidence_a: str, evidence_b: str) -> str:
        """
        Pause execution, display conflict, get human input.
        Returns: human's resolution/guidance.
        """
        console.print(Panel(
            f"[bold red]Conflicting Evidence — Cannot Resolve Automatically[/]\n\n"
            f"[bold]Step {step.step_id}:[/] {step.pratijna}\n\n"
            f"[bold]Evidence A:[/]\n{evidence_a}\n\n"
            f"[bold]Evidence B:[/]\n{evidence_b}\n\n"
            f"The agent cannot determine which is correct.",
            title="⚠️  ESCALATION"
        ))
        
        response = click.prompt("Your guidance (or 'abort' to stop)")
        return response
Integration: When _escalate_to_human is called in failure router:

Set session status to "paused"
Save state
Display conflict via rich
Wait for input
Resume with human's guidance as additional context
Test: Manually trigger escalation, provide input, verify execution resumes.

PHASE 4: Polish (Steps 19-24)
Step 19: Rich Terminal Display
What: Professional terminal output matching the vision from the architecture doc.

File: nyaya/cli/display.py

class HarnessDisplay:
    """Rich terminal output for the harness execution."""
    
    def show_goal(self, goal: str): ...
    def show_plan(self, plan: list[PancavayavaShell]): ...
    def show_step_start(self, step_id: int, pratijna: str): ...
    def show_tool_call(self, pramana_call: PramanaCall): ...
    def show_verification(self, result: VerificationResult): ...
    def show_validity(self, result: KaranataResult): ...
    def show_step_pass(self, step: PancavayavaStep): ...
    def show_step_fail(self, step: PancavayavaStep): ...
    def show_failure_classification(self, classification: dict): ...
    def show_recovery(self, recovery: RecoveryResult): ...
    def show_replan(self, new_steps: list): ...
    def show_completion(self, state: SessionState): ...
    def show_trace(self, state: SessionState): ...
The display should look like:

╭─── Nyaya Agent ─── Goal: ... ────────────────────────────────╮
│ ...                                                           │
╰───────────────────────────────────────────────────────────────╯

📋 Plan:
  1. [pratijñā text]
  2. [pratijñā text]
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⟐ Step 1: [pratijñā]
  ├─ Hetu: [source]
  ├─ Tool: pratyaksha.read_file(path) → [summary] ✓
  ├─ Tool: anumana.infer_cause(obs) → [result] ✓
  ├─ Nigamana: [what was produced]
  ├─ Verify: ✅ anvaya ✓ | composability ✓
  └─ Validity: ✓ pūrva | ✓ niyata | ✓ ananya

⟐ Step 3: [pratijñā]
  ├─ ...
  ├─ Nigamana: [wrong output]
  ├─ Verify: ❌ FAIL — nigamana contradicts pratijñā
  │
  ├─ 🔍 Classifying: VIRUDDHA (wrong approach)
  │   "The method moves away from goal because..."
  │
  ├─ 🔧 Recovery: ABANDON + REPLAN
  │   Tool: shabda.read_docs(alternative) → [new approach]
  │   New udāharaṇa: [description of new method]
  │
  └─ ♻️  Replanned steps 3-5 with new approach

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Goal achieved in 6 steps (1 failure, 1 recovery)
Step 20: Configuration
What: .nyaya.toml for project-level config, env vars for secrets.

# .nyaya.toml (project root)
[agent]
model = "claude-sonnet-4-20250514"
max_steps = 20
max_failures_per_step = 3
max_total_failures = 10

[display]
verbose = false
show_tool_output = true
show_validity = true

[tools]
command_timeout = 30
allowed_commands = ["*"]  # or whitelist
workspace_boundary = "."  # don't access files outside this

[recovery]
auto_escalate_after = 2   # escalate to human after 2 failed recoveries
save_abandoned_approaches = true
Step 21: Resume + Session Management
What: Robust session lifecycle.

nyaya run "fix the bug"          # starts new session
nyaya status                      # shows current session state
nyaya resume                      # resume paused/interrupted session
nyaya trace                       # show last session trace
nyaya trace --session abc123      # show specific session
nyaya sessions                    # list all sessions
nyaya clean                       # remove .nyaya/ directory
Step 22: Error Boundaries + Graceful Degradation
What: Handle infrastructure failures (API down, timeout, permission denied).

# In harness loop:
try:
    result = self._execute_cycle(step)
except LLMError as e:
    # API failure — not a logical failure
    # Retry with backoff, or pause
    ...
except ToolExecutionError as e:
    # Tool crashed (permission denied, timeout)
    # Record as pratyaksha failure, classify
    ...
except KeyboardInterrupt:
    # Save state, allow resume
    self.state.set_status("paused")
    self.state.save()
    ...
Step 23: Testing Suite
What: Tests for each component independently + integration tests.

tests/
├── unit/
│   ├── test_schemas.py           ← all models serialize/deserialize
│   ├── test_tools_pratyaksha.py  ← file ops work correctly
│   ├── test_tools_anumana.py     ← inference returns structured output
│   ├── test_validity_gate.py     ← three conditions checked
│   ├── test_verifier.py          ← anvaya-vyatireka logic
│   └── test_failure_router.py    ← each type routes correctly
│
├── integration/
│   ├── test_happy_path.py        ← simple task completes
│   ├── test_failure_recovery.py  ← each failure type triggers+recovers
│   ├── test_state_persistence.py ← save/load/resume works
│   └── test_cascade_check.py     ← badhita cascades correctly
│
└── e2e/
    ├── test_create_file.py       ← "create hello.py"
    ├── test_read_and_summarize.py
    └── test_fix_simple_bug.py    ← end-to-end bug fix
Step 24: Documentation + Examples
Files:

README.md — installation, quickstart, architecture overview
docs/architecture.md — full Nyaya mapping explanation
docs/failure-types.md — the five types with real examples
examples/ — walkthrough notebooks showing actual traces
Build Order Summary (For Claude Code)
┌─────────────────────────────────────────────────────────────┐
│                     BUILD SEQUENCE                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PHASE 1: GET IT RUNNING (Steps 1-7)                       │
│  ─────────────────────────────────────                      │
│  1. Project skeleton + deps                                 │
│  2. All Pydantic schemas                                    │
│  3. Tool base + pratyaksha tools                            │
│  4. LLM client (basic Claude wrapper)                       │
│  5. State manager (JSON persistence)                        │
│  6. Minimal harness loop (plan → execute → record)          │
│  7. CLI entry point                                         │
│                                                             │
│  CHECKPOINT: "nyaya run 'create hello.py'" works            │
│                                                             │
│  PHASE 2: MAKE IT SAFE (Steps 8-12)                        │
│  ─────────────────────────────────────                      │
│  8. Verifier (anvaya-vyatireka)                             │
│  9. Validity gate (karaṇatā)                              │
│  10. Wire verification into harness loop                    │
│  11. State persistence + resume                             │
│  12. Trace display command                                  │
│                                                             │
│  CHECKPOINT: Steps verified before commit, trace viewable   │
│                                                             │
│  PHASE 3: MAKE IT ROBUST (Steps 13-18)                     │
│  ─────────────────────────────────────                      │
│  13. Failure classifier (5 types)                           │
│  14. Recovery handlers (one per type)                       │
│  15. Wire failure router into harness                       │
│  16. Failure/recovery state recording                       │
│  17. Anumāna + upamāna + śabda tools                     │
│  18. Interactive escalation (satpratipaksha)                │
│                                                             │
│  CHECKPOINT: Failures classified + recovered automatically  │
│                                                             │
│  PHASE 4: MAKE IT USABLE (Steps 19-24)                     │
│  ─────────────────────────────────────                      │
│  19. Rich terminal display                                  │
│  20. Configuration (.nyaya.toml)                            │
│  21. Resume + session management                            │
│  22. Error boundaries + graceful degradation                │
│  23. Testing suite                                          │
│  24. Documentation + examples                               │
│                                                             │
│  CHECKPOINT: Production-quality CLI tool                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
The Prompt for Claude Code
Give this as the initial prompt:

I'm building nyaya-harness — a terminal-based AI agent (like Claude Code / Aider) with a principled internal architecture for step verification and failure recovery.

User experience: User types nyaya run "fix the login bug" in terminal. Agent plans, executes, verifies, recovers from failures, and produces results autonomously.

Internal architecture:

Every step has 5 parts (pañcāvayava):
Pratijñā (output contract — stated BEFORE execution)
Hetu (verified inputs — confirmed BEFORE execution)
Udāharaṇa (method/rule — confirmed BEFORE execution)
Upanaya (execution trace — recorded DURING execution)
Nigamana (actual output — recorded AFTER execution)
All knowledge acquisition is through categorized tool calls (pramāṇas):
Pratyaksha (direct observation): read_file, run_command, run_test, etc.
Anumana (inference): infer_cause, infer_effect, trace_dependency — LLM-backed
Upamana (pattern matching): find_similar, match_error_pattern — retrieval + LLM
Shabda (authority): read_docs, query_spec, search_kb — documentation lookup
Every tool call is recorded with: tool name, input, output, confidence level, what it was used for
Verification uses anvaya-vyatireka:
Anvaya: does nigamana satisfy pratijñā? (positive check)
Vyatireka: could output exist without this step? (negative check)
Composability: does nigamana feed next step's hetu?
Validity gate (karaṇatā) — 3 conditions before commit:
Pūrvavartitva: input existed before execution
Niyatatva: output is consistent with method
Ananyathasiddhatva: step was genuinely necessary
Five failure types with specific recoveries:
Savyabhicāra (erratic) → decompose + strengthen → use anumāna
Viruddha (wrong approach) → abandon + replan → use upamāna/śabda
Satpratipakṣa (conflicting evidence) → gather more / escalate → switch pramāṇa
Asiddha (missing dependency) → go upstream → use pratyakṣa
Bādhita (falsified assumption) → update rule + cascade check → pratyakṣa overrides
State records 3 things per step:
Full pañcāvayava (5 parts + verification + validity)
Epistemology log (all tool calls with category, confidence, used_for)
Failure/recovery record (type, evidence, recovery action, outcome)
Orchestration loop:
Phase 0: Plan (backward chain goal → steps)
Phase 1: Read (load prev nigamana, validate preconditions)
Phase 2: Determine (confirm method still applies)
Phase 3: Execute (make tool calls, record upanaya)
Phase 4: Verify (anvaya-vyatireka)
Phase 5: Advance (validity gate → commit → next step)
Phase 6: Failure (classify → route → recover)
Start with Phase 1 (Steps 1-7): project skeleton, schemas, pratyaksha tools, LLM client, state manager, minimal harness loop, and CLI.

Here is the complete project structure and schema definitions: [paste the project structure and Step 2 schemas from above]

Then for each subsequent phase, give it the relevant section of this plan.

Final Verification: Is Everything Accounted For?
✓ Pañcāvayava — 5 members, written at correct times (before/during/after)
✓ Pramāṇas — 4 categories as tool calls, recorded with metadata
✓ Hetvābhāsa — 5 types, each with detection + recovery + state recording
✓ Vyāpti chain — nigamana of step i → hetu of step i+1
✓ Sādhya-sādhana — backward planning in Phase 0
✓ Karaṇatā — 3 validity conditions in validity gate
✓ Anvaya-vyatireka — positive AND negative verification
✓ State (3-part) — pañcāvayava + epistemology log + failure record
✓ Cascade check — bādhita checks other steps with same rule
✓ Upstream walk — asiddha walks backward through trace
✓ Step revision tracking — revised flag + previous value
✓ Escalation — satpratipakṣa → human in the loop
✓ Tool call recording — every call logged with used_for
✓ Recovery routing — failure type → specific action → specific pramāṇa
✓ Plan modification — insert substeps, replace from step, revise upstream
✓ Session management — save, load, resume, trace display
✓ Budget/limits — max failures per step, max total, auto-abort