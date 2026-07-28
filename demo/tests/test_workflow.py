from catbob_mini.audit import AuditLog
from catbob_mini.risk import TaskProfile
from catbob_mini.workflow import DecisionStatus, Executor, Gate, Planner


def _pipeline():
    audit = AuditLog()
    return audit, Planner(audit), Gate(audit), Executor(audit)


def test_low_risk_task_is_auto_approved_and_executed():
    _audit, planner, gate, executor = _pipeline()
    plan = planner.plan("Tippfehler in Doku korrigieren", TaskProfile())
    decision = gate.decide(plan)
    result = executor.execute(plan, decision)

    assert decision.status == DecisionStatus.AUTO_APPROVED
    assert result == "erledigt: Tippfehler in Doku korrigieren"


def test_high_risk_task_is_blocked_without_human_approval():
    _audit, planner, gate, executor = _pipeline()
    plan = planner.plan("Billing-Logik aendern", TaskProfile(touches_billing=True))
    decision = gate.decide(plan, human_approved=False)
    result = executor.execute(plan, decision)

    assert decision.status == DecisionStatus.PENDING_HUMAN
    assert result is None


def test_high_risk_task_runs_after_explicit_human_approval():
    _audit, planner, gate, executor = _pipeline()
    plan = planner.plan("Billing-Logik aendern", TaskProfile(touches_billing=True))
    decision = gate.decide(plan, human_approved=True)
    result = executor.execute(plan, decision)

    assert decision.status == DecisionStatus.AUTO_APPROVED
    assert result is not None


def test_full_pipeline_writes_one_audit_entry_per_stage():
    audit, planner, gate, executor = _pipeline()
    plan = planner.plan("Feature bauen", TaskProfile())
    decision = gate.decide(plan)
    executor.execute(plan, decision)

    actions = [entry.action for entry in audit.entries]
    assert actions == ["plan_created", "auto_approved", "execution_completed"]


def test_blocked_execution_is_also_audited():
    audit, planner, gate, executor = _pipeline()
    plan = planner.plan("Auth-Flow aendern", TaskProfile(touches_auth=True))
    decision = gate.decide(plan)
    executor.execute(plan, decision)

    actions = [entry.action for entry in audit.entries]
    assert actions == ["plan_created", "pending_human", "execution_blocked"]
