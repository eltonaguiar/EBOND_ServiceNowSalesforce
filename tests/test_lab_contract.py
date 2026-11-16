from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "lab"
SF = LAB / "salesforce" / "force-app" / "main" / "default"


def test_required_artifacts_exist():
    required = [
        LAB / "README.md",
        LAB / ".env.example",
        LAB / "scripts" / "curl_level1.sh",
        LAB / "servicenow" / "scripted_rest_bond_case.js",
        LAB / "servicenow" / "business_rule_async_sync.js",
        LAB / "servicenow" / "rest_message_notes.md",
        SF / "classes" / "SnowIncidentService.cls",
        SF / "classes" / "SnowIncidentRest.cls",
        SF / "classes" / "CaseTriggerHandler.cls",
        SF / "classes" / "CaseEscalationQueueable.cls",
        SF / "triggers" / "CaseTrigger.trigger",
        SF / "objects" / "Case" / "fields" / "Snow_Sys_Id__c.field-meta.xml",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    assert missing == []


def test_every_apex_class_has_meta_and_tests_cover_production():
    classes = {p.stem for p in (SF / "classes").glob("*.cls")}
    metas = {p.name[: -len(".cls-meta.xml")] for p in (SF / "classes").glob("*.cls-meta.xml")}
    assert classes == metas
    production = {n for n in classes if not n.endswith("Test") and n != "SnowCalloutMock"}
    tests = {n for n in classes if n.endswith("Test")}
    uncovered = {n for n in production if n + "Test" not in tests}
    assert uncovered == set()


def test_loop_guard_and_external_id_present():
    handler = (SF / "classes" / "CaseTriggerHandler.cls").read_text()
    rest = (SF / "classes" / "SnowIncidentRest.cls").read_text()
    sn = (LAB / "servicenow" / "business_rule_async_sync.js").read_text()
    field = (SF / "objects" / "Case" / "fields" / "Snow_Sys_Id__c.field-meta.xml").read_text()
    assert "servicenow" in handler
    assert "enqueueJob" in handler
    assert "upsert row Snow_Sys_Id__c" in rest
    assert "u_sync_source" in sn
    assert "<externalId>true</externalId>" in field
    assert "<unique>true</unique>" in field


def test_no_secrets_committed():
    banned = ("client_secret=", "BEGIN PRIVATE KEY", "password\": \"")
    hits = []
    for p in LAB.rglob("*"):
        if not p.is_file() or p.suffix in {".png", ".jpg"}:
            continue
        text = p.read_text(errors="ignore")
        for token in banned:
            if token in text and p.name != ".env.example":
                hits.append(f"{p}:{token}")
    assert hits == []


def test_readme_pages_link():
    readme = (ROOT / "README.md").read_text()
    assert "https://eltonaguiar.github.io/EBOND_ServiceNowSalesforce/" in readme
