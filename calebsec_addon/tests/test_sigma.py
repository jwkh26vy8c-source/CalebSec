from pathlib import Path

from calebsec.core.models import LogEvent
from calebsec.sigma.rules import load_rules


def test_failed_login_rule_matches():
    rules = load_rules(Path("rules"))
    event = LogEvent(source="linux", message="Failed password for root from 10.0.0.5", user="root")
    matches = [r for r in rules if r.match(event)[0]]
    assert matches
