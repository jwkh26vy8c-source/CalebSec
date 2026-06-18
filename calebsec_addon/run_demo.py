from pathlib import Path

from calebsec.core.config import RULES_DIR
from calebsec.core.models import LogEvent
from calebsec.ingestion.engine import IngestionEngine
from calebsec.sigma.rules import load_rules

engine = IngestionEngine()
engine.set_rules(load_rules(RULES_DIR))

sample = LogEvent(
    source="linux-auth",
    message="Failed password for root from 10.0.0.5",
    user="root",
    src_ip="10.0.0.5",
)
alerts = engine.ingest(sample)
print(f"Rules loaded: {len(engine.rules)}")
print(f"Alerts generated: {len(alerts)}")
for alert in alerts:
    print(f"- [{alert.level}] {alert.title} ({alert.rule_id}) matched {alert.matched_fields}")
