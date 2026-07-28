from catbob_mini.risk import (
    RiskLevel,
    TaskProfile,
    classify_risk,
    requires_human_approval,
)


def test_default_profile_is_r0():
    assert classify_risk(TaskProfile()) == RiskLevel.R0


def test_missing_tests_escalates_by_one():
    assert classify_risk(TaskProfile(has_tests=False)) == RiskLevel.R1


def test_billing_escalates_by_two():
    assert classify_risk(TaskProfile(touches_billing=True)) == RiskLevel.R2


def test_auth_escalates_by_two():
    assert classify_risk(TaskProfile(touches_auth=True)) == RiskLevel.R2


def test_irreversible_production_change_is_always_r4():
    profile = TaskProfile(touches_production_data=True, reversible=False, has_tests=True)
    assert classify_risk(profile) == RiskLevel.R4


def test_level_never_exceeds_r4():
    profile = TaskProfile(
        touches_auth=True,
        touches_billing=True,
        touches_production_data=True,
        has_tests=False,
        reversible=False,
    )
    assert classify_risk(profile) == RiskLevel.R4


def test_r0_and_r1_do_not_require_human_approval():
    assert requires_human_approval(RiskLevel.R0) is False
    assert requires_human_approval(RiskLevel.R1) is False


def test_r2_and_above_require_human_approval():
    assert requires_human_approval(RiskLevel.R2) is True
    assert requires_human_approval(RiskLevel.R4) is True
