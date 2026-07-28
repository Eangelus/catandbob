from catbob_mini.audit import AuditLog


def test_new_log_is_empty():
    assert len(AuditLog()) == 0


def test_record_appends_entry():
    log = AuditLog()
    log.record(actor="tester", action="did_something", reason="because")
    assert len(log) == 1
    assert log.entries[0].actor == "tester"
    assert log.entries[0].action == "did_something"


def test_entries_returns_a_copy_not_the_internal_list():
    log = AuditLog()
    log.record(actor="a", action="b", reason="c")
    snapshot = log.entries
    snapshot.append("tampered")  # darf das interne Log nicht veraendern
    assert len(log) == 1


def test_entries_are_immutable():
    log = AuditLog()
    log.record(actor="a", action="b", reason="c")
    entry = log.entries[0]
    try:
        entry.actor = "changed"  # type: ignore[misc]
        assert False, "AuditEntry sollte frozen sein"
    except AttributeError:
        pass
