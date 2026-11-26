# -*- coding: utf-8 -*-

""" #+begin_org
* ~[Summary]~ :: cbmVerify --- is this platform healthy? Evidence for a CBM leaf, the platform-wide
  checks, the report and the comparison of two reports. Pure functions; the Cmnds are cbm_verify
  (cbmProc_csu.py) and fullyVerify / verifyCompare (sysCbmManage_csu.py). AI-WorkPlan.org Stage 5.
#+end_org """

####+BEGIN: b:py3:cs:file/dblockControls :classification "cs-u"
""" #+begin_org
* [[elisp:(org-cycle)][| /Control Parameters Of This File/ |]] :: dblk ctrls classifications=cs-u
#+end_org """
####+END:

####+BEGIN: b:prog:file/proclamations :outLevel 1
""" #+begin_org
* *[[elisp:(org-cycle)][| Proclamations |]]* :: Libre-Halaal Software --- Part Of BISOS ---  Poly-COMEEGA Format.
** This is Libre-Halaal Software. © Neda Communications, Inc. Subject to AGPL.
** It is part of BISOS (ByStar Internet Services OS)
#+end_org """
####+END:

if 'csInfo' not in globals(): import typing ; csInfo: typing.Dict[str, typing.Any] = { 'moduleName': ['loadAs'], }
csInfo['version'] = '202611260001'
csInfo['status']  = 'inDev'

import typing
import datetime
import json
import os
import pathlib
import re
import socket
import subprocess
import time
import urllib.error
import urllib.request

from bisos.capability import cbmProc_seedInfo


###############################################################################
# Verdicts
#
# A verdict comes from evidence --- an HTTP status, systemctl is-active, a check's verdict line ---
# never from an exit code: today every PyCS command exits 0 (bisos-pip/b Stage 4). Exit codes are
# recorded beside the verdict (materializeRc, a check's rc), so that a report taken before Stage 4
# and one taken after it show what Stage 4 changed.
#
#   ok         every check passed
#   fail       a check failed (or the leaf never materialized, or its status says failed)
#   skip       the gate is not enabled: not materialized by design
#   unchecked  enabled and materialized, but the leaf declares nothing to check
#   notRun     (fullyVerify only) the walk did not reach the leaf in this run
###############################################################################

VERIFY_FILENAME = "cbmProc.verify"
REPORT_BASE = cbmProc_seedInfo.STATUS_BASE / "verify"

# The last line of a check, "<name> verify: ok|fail <detail>": the convention every verifySpec follows.
VERDICT_RE = re.compile(r"^(\S+) verify: (ok|fail)\b\s*(.*)$")

# An answer is good when it is not an error: a redirect to a login page (grafana) or 401 are fine.
HTTP_GOOD = set(range(200, 400)) | {401}


def now() -> str:
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def hereFqdn(hereName: str) -> str:
    """The .internal name of a hereName, from bisos.banna when it is there (it is the one source). A name
    that already has the suffix (a PALS's uri/here/value, e.g. example.org.internal) is kept."""
    try:
        from bisos.banna import tcpPorts
        fqdn = tcpPorts.hereFqdn
    except ImportError:
        def fqdn(name): return f"{name}.internal"
    suffix = fqdn("x")[1:]
    return hereName if hereName.endswith(suffix) else fqdn(hereName)


def environment() -> str:
    """Container, Vm or Box --- some leaves skip parts by design in a container."""
    if os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv"):
        return "Container"
    try:
        virt = subprocess.run(["systemd-detect-virt"], capture_output=True, text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        virt = ""
    if virt in ("docker", "podman", "lxc", "systemd-nspawn"):
        return "Container"
    if virt and virt != "none":
        return "Vm"
    return "Box"


###############################################################################
# Evidence
###############################################################################

def resolves(fqdn: str) -> str | None:
    """The address fqdn resolves to (through /etc/hosts), None when it does not."""
    try:
        return socket.gethostbyname(fqdn)
    except OSError:
        return None


# nginx's default site answers every .internal name that has no vhost of its own, with 200.
NGINX_DEFAULT_RE = re.compile(rb"<title>Welcome to nginx!</title>")
NO_VHOST = "nginx default page (no vhost)"


def httpStatus(url: str, attempts: int = 3, pause: float = 5.0, timeout: float = 10.0) -> int | str:
    """The HTTP status of url, retried: services are slow to answer right after a walk. NO_VHOST when
    what answered is nginx's default page, not the capability."""
    last: int | str = "no answer"
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                if NGINX_DEFAULT_RE.search(resp.read(4096)):
                    return NO_VHOST
                return resp.status
        except urllib.error.HTTPError as e:
            if e.code in HTTP_GOOD:
                return e.code
            last = e.code
        except (urllib.error.URLError, OSError) as e:
            last = f"no answer ({getattr(e, 'reason', e)})"
        if attempt + 1 < attempts:
            time.sleep(pause)
    return last


def httpCheck(fqdn: str) -> dict:
    url = f"http://{fqdn}/"
    addr = resolves(fqdn)
    if addr is None:
        return {"kind": "http", "target": url, "ok": False, "detail": f"{fqdn} does not resolve"}
    status = httpStatus(url)
    return {"kind": "http", "target": url, "ok": status in HTTP_GOOD, "detail": f"{status} ({addr})"}


def unitCheck(unit: str) -> dict:
    try:
        state = subprocess.run(["systemctl", "is-active", unit], capture_output=True, text=True,
                               timeout=30).stdout.strip() or "unknown"
    except (OSError, subprocess.TimeoutExpired) as e:
        state = f"not run ({e})"
    return {"kind": "unit", "target": unit, "ok": state == "active", "detail": state}


def specCheck(verifySpec: str, cwd: pathlib.Path, timeout: int = 900) -> dict:
    """Run a leaf's verifySpec (a shell command) and read its last verdict line; its rc is only recorded."""
    try:
        proc = subprocess.run(["bash", "-c", verifySpec], cwd=cwd, capture_output=True, text=True,
                              timeout=timeout)
        out, rc = (proc.stdout or "") + (proc.stderr or ""), proc.returncode
    except subprocess.TimeoutExpired:
        return {"kind": "check", "target": verifySpec, "ok": False, "rc": None,
                "detail": f"timed out after {timeout}s"}
    verdicts = [m for m in (VERDICT_RE.match(line.strip()) for line in out.splitlines()) if m]
    if not verdicts:
        return {"kind": "check", "target": verifySpec, "ok": False, "rc": rc,
                "detail": "no '<name> verify: ok|fail' line in its output"}
    last = verdicts[-1]
    return {"kind": "check", "target": verifySpec, "ok": last.group(2) == "ok", "rc": rc,
            "detail": last.group(0)}


def materializeRc(statusText: str) -> int | None:
    """The exit code the last cbs_materialize had, from cbmProc.status: recorded, not trusted."""
    for line in reversed(statusText.splitlines()):
        m = re.search(r"ran: cbs_(?:re)?[mM]aterialize (ok|failed rc=(-?\d+))", line)
        if m:
            return 0 if m.group(1) == "ok" else int(m.group(2))
    return None


###############################################################################
# leafVerify --- the record of one leaf (cbm_verify writes it to cbmProc.verify)
###############################################################################

def leafVerify(
        plantDir: pathlib.Path,
        capabilityName: str,
        hereName: str | None,
        verifyUnits: list[str] | None,
        verifySpec: str | None,
) -> dict:
    gate = cbmProc_seedInfo.controlRead(plantDir).value
    statusText = cbmProc_seedInfo.statusRead(plantDir)
    lastStatus = statusText.splitlines()[-1] if statusText.strip() else ""
    record = {
        "capabilityName": capabilityName,
        "leaf": str(plantDir),
        "leafRel": str(cbmProc_seedInfo.leafRel(plantDir)),
        "at": now(),
        "gate": gate,
        "lastStatus": lastStatus,
        "materializeRc": materializeRc(statusText),
        "checks": [],
    }
    if gate != cbmProc_seedInfo.ControlState.Enabled.value:
        record.update(verdict="skip", detail=f"control={gate}: not materialized by design")
        return _withRcAgreement(record)

    checks = record["checks"]
    notes = []
    # The leaf's own word: its last materialize could not even start. No record at all is only a note
    # when the evidence below says it works (the status moved to /bisos/var/cbm on 2026-11-24, so a
    # host materialized before has none), and a failure when there is no other evidence.
    if not lastStatus:
        notes.append("no materialize record in cbmProc.status")
    elif re.search(r"\sfailed: ", lastStatus):
        checks.append({"kind": "status", "target": "cbmProc.status", "ok": False, "detail": lastStatus})

    name = hereName or capabilityName
    fqdn = hereFqdn(name)
    if hereName or resolves(fqdn):        # declared, or a name this host has: it must answer
        checks.append(httpCheck(fqdn))
    for unit in verifyUnits or []:
        checks.append(unitCheck(unit))
    if verifySpec:
        checks.append(specCheck(verifySpec, plantDir))

    if not checks and notes:
        checks.append({"kind": "status", "target": "cbmProc.status", "ok": False,
                       "detail": "enabled, never materialized, and nothing else to check"})
        notes = []
    record["notes"] = notes
    failed = [c for c in checks if not c["ok"]]
    noteText = "".join(f"; note: {n}" for n in notes)
    if failed:
        record.update(verdict="fail", detail="; ".join(f"{c['kind']} {c['target']}: {c['detail']}"
                                                       for c in failed) + noteText)
    elif checks:
        record.update(verdict="ok", detail=f"{len(checks)} check(s)" + noteText)
    else:
        record.update(verdict="unchecked", detail="no hereName, verifyUnits or verifySpec declared")
    return _withRcAgreement(record)


def _withRcAgreement(record: dict) -> dict:
    """Whether the exit code told the truth: 'masked' is a failure that exited 0 (bisos-pip/b Stage 4)."""
    rc, verdict = record["materializeRc"], record["verdict"]
    if verdict in ("skip", "unchecked") or rc is None:
        record["rcAgrees"] = None
    elif verdict == "fail" and rc == 0:
        record["rcAgrees"] = "masked"
    else:
        record["rcAgrees"] = (verdict == "ok") == (rc == 0)
    return record


def verifyPath(plantDir: pathlib.Path) -> pathlib.Path:
    return cbmProc_seedInfo.statusDir(plantDir) / VERIFY_FILENAME


def verifyWrite(plantDir: pathlib.Path, record: dict) -> pathlib.Path:
    """Write the record as cbmProc.verify, next to cbmProc.status (overwritten: it is the latest)."""
    cbmProc_seedInfo._statusDirEnsure(plantDir)
    path = verifyPath(plantDir)
    isNew = not path.exists()
    path.write_text(json.dumps(record, indent=2) + "\n")
    if isNew:
        os.chmod(path, 0o664)
    return path


def verifyRead(plantDir: pathlib.Path) -> dict | None:
    path = verifyPath(plantDir)
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


###############################################################################
# Platform: the leaves of a walk root, the checks no leaf owns
###############################################################################

def leavesUnder(root: pathlib.Path) -> list[pathlib.Path]:
    """The plant directories (resolved) of every cbmProc.spcs under root, symlinked dirs followed."""
    found = []
    for dirPath, dirNames, fileNames in os.walk(root, followlinks=True):
        dirNames[:] = sorted(d for d in dirNames if not d.startswith((".", "__")))
        if "cbmProc.spcs" in fileNames:
            found.append(pathlib.Path(dirPath).resolve())
    return found


PALS_LIST = pathlib.Path("/bisos/var/palsHere/uri.list")


def hereNames() -> list[tuple[str, str, str]]:
    """(fqdn, expected address, source) of every name this host serves: banna's, then the PALS'."""
    names = []
    try:
        from bisos.banna import tcpPorts
        for ip, name, portNu in tcpPorts.hereEntries():
            names.append((tcpPorts.hereFqdn(name), ip, f"banna port {portNu}"))
    except ImportError:
        pass
    try:
        for line in PALS_LIST.read_text().splitlines():
            parts = line.split()
            if len(parts) >= 2 and not line.lstrip().startswith("#"):
                names.append((parts[1], parts[0], "palsHere"))
    except OSError:
        pass
    return names


def nameChecks(claimed: set[str]) -> list[dict]:
    """Every name must resolve to its address. HTTP only for names no enabled leaf claims (theirs is in
    the leaf's record), and then as information: a _dev name answers only while its dev server runs."""
    results = []
    for fqdn, ip, source in hereNames():
        addr = resolves(fqdn)
        if addr != ip:
            results.append({"kind": "name", "target": fqdn, "ok": False,
                            "detail": f"resolves to {addr or 'nothing'}, {source} assigns {ip}"})
            continue
        if fqdn in claimed:
            continue
        status = httpStatus(f"http://{fqdn}/", attempts=1, timeout=5)
        results.append({"kind": "name", "target": fqdn, "ok": True, "info": True,
                        "detail": f"no enabled leaf; http {status}"})
    return results


def nginxCheck() -> dict | None:
    if not os.path.exists("/usr/sbin/nginx"):
        return None
    proc = subprocess.run(["sudo", "-n", "/usr/sbin/nginx", "-t"], capture_output=True, text=True, timeout=60)
    out = (proc.stdout + proc.stderr).strip()
    ok = "test is successful" in out
    return {"kind": "nginx", "target": "nginx -t", "ok": ok,
            "detail": "test is successful" if ok else (out.splitlines()[-1] if out else "no output")}


def failedUnitsCheck() -> list[dict]:
    proc = subprocess.run(["systemctl", "--failed", "--plain", "--no-legend", "--no-pager"],
                          capture_output=True, text=True, timeout=60)
    results = []
    for line in proc.stdout.splitlines():
        if line.strip():
            unit = line.split()[0]
            results.append({"kind": "systemd", "target": unit, "ok": False, "detail": "failed"})
    return results


###############################################################################
# logScan --- what a person reads a run's log for (AI-WorkPlan.org 5.4)
#
# The log echoes each script's source before running it ("** cmnd=" blocks), so the patterns are
# anchored to what a program prints at the start of a line, never to text a script contains
# (=echo "banna: ERROR: ..."= is indented and starts with echo). A problem is attributed to the
# leaf whose "[<leaf>] running:" line came last; when that leaf's next line is "ran: ... ok", the
# failure was masked (reported as success).
###############################################################################

LOG_PATTERNS = [
    ("ehProblem",   re.compile(r"^(\* EH_Problem|EH_,\S+: PROBLEM)")),
    ("badOutcome",  re.compile(r"^io\.eh\.badOutcome: .*Operation Failed")),
    ("checkFail",   re.compile(r"^\s{1,4}[\w-]+(?: [\w-]+)?\s+FAIL\s")),
    ("notComplete", re.compile(r"\bNOT complete\b")),
    ("verifyFail",  re.compile(r"^\S+ verify: fail\b")),
    ("systemd",     re.compile(r"^Failed to \S+ \S+: ")),
    ("apt",         re.compile(r"^E: ")),
    ("traceback",   re.compile(r"^Traceback \(most recent call last\)")),
    ("leafFailed",  re.compile(r"^ran: \S+ failed rc=|^failed: \S+ ")),
]
LEAF_RE = re.compile(r"^\[(\S+)\] (?:running|bootstrap): ")
RAN_OK_RE = re.compile(r"^ran: \S+ ok$")


def logScan(paths: list[pathlib.Path]) -> list[dict]:
    hits = []
    for path in paths:
        try:
            lines = path.read_text(errors="replace").splitlines()
        except OSError:
            continue
        leaf = None
        open_: list[dict] = []          # this leaf's hits, until its "ran: ... ok"
        for n, line in enumerate(lines, 1):
            m = LEAF_RE.match(line)
            if m:
                leaf, open_ = m.group(1), []
                continue
            if RAN_OK_RE.match(line):
                for hit in open_:
                    hit["masked"] = True
                open_ = []
                continue
            for kind, pattern in LOG_PATTERNS:
                if pattern.search(line):
                    hit = {"kind": kind, "file": str(path), "line": n, "leaf": leaf,
                           "text": line.strip()[:200], "masked": False}
                    hits.append(hit)
                    open_.append(hit)
                    break
    return hits


def defaultLogs(home: pathlib.Path | None = None, maxAgeHours: float = 24.0) -> list[pathlib.Path]:
    """The newest raw-bisos and sysCbmFullyMaterialize logs in ~ (as those scripts name them), when written
    in the last maxAgeHours: an older one is another run's (a build and its walk take a few hours)."""
    home = home or pathlib.Path.home()
    logs = []
    for prefix in ("raw-bisos", "sysCbmFullyMaterialize"):
        found = sorted(home.glob(f"{prefix}-*-log.org"))
        if found and time.time() - found[-1].stat().st_mtime < maxAgeHours * 3600:
            logs.append(found[-1])
    return logs


###############################################################################
# The report
###############################################################################

def report(leaves: list[dict], platform: list[dict], logHits: list[dict], logs: list[pathlib.Path]) -> dict:
    counts: dict[str, int] = {}
    for leaf in leaves:
        counts[leaf["verdict"]] = counts.get(leaf["verdict"], 0) + 1
    platformProblems = [c for c in platform if not c["ok"]]
    masked = [leaf["capabilityName"] for leaf in leaves if leaf.get("rcAgrees") == "masked"]
    ok = counts.get("fail", 0) == 0 and counts.get("notRun", 0) == 0 and not platformProblems
    return {
        "schema": "bisos.capability.cbmVerify/1",
        "generatedAt": now(),
        "host": socket.gethostname(),
        "environment": environment(),
        "verdict": "ok" if ok else "fail",
        "counts": counts,
        "platformProblems": len(platformProblems),
        "maskedFailures": masked,
        "leaves": leaves,
        "platform": platform,
        "logs": [str(p) for p in logs],
        "logHits": logHits,
    }


def reportOrg(rep: dict) -> str:
    out = [f"#+title: CBM Verify Report --- {rep['host']} --- {rep['generatedAt']}", "",
           f"Environment: {rep['environment']}.  Verdict: *{rep['verdict']}*.  Leaves: "
           + ", ".join(f"{k} {v}" for k, v in sorted(rep["counts"].items()))
           + f".  Platform problems: {rep['platformProblems']}.", ""]
    if rep["maskedFailures"]:
        out += [f"Masked (failed, yet materialize exited 0): {', '.join(rep['maskedFailures'])}", ""]
    out += ["* Leaves", "", "| leaf | verdict | rc | detail |", "|-"]
    for leaf in rep["leaves"]:
        rc = "" if leaf["materializeRc"] is None else str(leaf["materializeRc"])
        detail = leaf["detail"].replace("|", "/")[:160]
        out.append(f"| {leaf['capabilityName']} | {leaf['verdict']} | {rc} | {detail} |")
    out += ["", "* Platform", "", "| check | target | ok | detail |", "|-"]
    for c in rep["platform"]:
        ok = "info" if c.get("info") else ("yes" if c["ok"] else "NO")
        out.append(f"| {c['kind']} | {c['target']} | {ok} | {str(c['detail']).replace('|', '/')[:120]} |")
    out += ["", "* Log hits", ""]
    if not rep["logHits"]:
        out.append("None" + ("" if rep["logs"] else " (no logs given or found)") + ".")
    for hit in rep["logHits"]:
        masked = "  MASKED" if hit["masked"] else ""
        out.append(f"- {pathlib.Path(hit['file']).name}:{hit['line']} [{hit['leaf'] or '-'}] "
                   f"{hit['kind']}{masked}: ={hit['text'][:140]}=")
    return "\n".join(out) + "\n"


def reportWrite(rep: dict, base: pathlib.Path = REPORT_BASE) -> pathlib.Path:
    """<base>/<yymmddHHMMSS>/report.json and report.org; <base>/latest points at the newest."""
    tag = datetime.datetime.now().strftime("%y%m%d%H%M%S")
    runDir = base / tag
    for d in reversed([runDir, *runDir.parents]):
        if not d.exists():
            d.mkdir()
            os.chmod(d, 0o2775)
    (runDir / "report.json").write_text(json.dumps(rep, indent=2) + "\n")
    (runDir / "report.org").write_text(reportOrg(rep))
    latest = base / "latest"
    tmp = base / f".latest.{os.getpid()}"
    tmp.symlink_to(tag)
    os.replace(tmp, latest)
    return runDir


###############################################################################
# compare --- what changed between two reports (the CI step, and the bisos.b Stage 4 measurement)
###############################################################################

def compare(old: dict, new: dict) -> dict:
    def byLeaf(rep):
        return {leaf["leafRel"]: leaf for leaf in rep["leaves"]}
    oldL, newL = byLeaf(old), byLeaf(new)
    changes = {"newFailures": [], "fixed": [], "stillFailing": [], "verdictChanged": [],
               "rcChanged": [], "added": [], "removed": []}
    for key, leaf in newL.items():
        prev = oldL.get(key)
        name = leaf["capabilityName"]
        if prev is None:
            changes["added"].append(name)
            continue
        if leaf["verdict"] == "fail" and prev["verdict"] != "fail":
            changes["newFailures"].append(f"{name}: {leaf['detail']}")
        elif prev["verdict"] == "fail" and leaf["verdict"] != "fail":
            changes["fixed"].append(name)
        elif leaf["verdict"] == "fail":
            changes["stillFailing"].append(name)
        if leaf["verdict"] != prev["verdict"]:
            changes["verdictChanged"].append(f"{name}: {prev['verdict']} -> {leaf['verdict']}")
        if leaf.get("rcAgrees") != prev.get("rcAgrees") or leaf["materializeRc"] != prev["materializeRc"]:
            changes["rcChanged"].append(f"{name}: rc {prev['materializeRc']} -> {leaf['materializeRc']}, "
                                        f"agrees {prev.get('rcAgrees')} -> {leaf.get('rcAgrees')}")
    changes["removed"] = [oldL[k]["capabilityName"] for k in oldL if k not in newL]
    oldP = {(c["kind"], c["target"]) for c in old["platform"] if not c["ok"]}
    newP = {(c["kind"], c["target"]) for c in new["platform"] if not c["ok"]}
    changes["platformNew"] = sorted(f"{k} {t}" for k, t in newP - oldP)
    changes["platformFixed"] = sorted(f"{k} {t}" for k, t in oldP - newP)
    return changes


def compareText(old: dict, new: dict, changes: dict) -> str:
    out = [f"compare: {old['generatedAt']} ({old['verdict']}) -> {new['generatedAt']} ({new['verdict']})"]
    for key, title in (("newFailures", "new failures"), ("fixed", "fixed"), ("stillFailing", "still failing"),
                       ("verdictChanged", "verdicts changed"), ("rcChanged", "exit codes changed"),
                       ("platformNew", "platform: new problems"), ("platformFixed", "platform: fixed"),
                       ("added", "leaves added"), ("removed", "leaves removed")):
        if changes[key]:
            out.append(f"{title} ({len(changes[key])}):")
            out += [f"  {item}" for item in changes[key]]
    if len(out) == 1:
        out.append("no change")
    return "\n".join(out)


def reportRead(path: pathlib.Path) -> dict:
    path = pathlib.Path(path)
    if path.is_dir():
        path = path / "report.json"
    return json.loads(path.read_text())


def reportRuns(base: pathlib.Path = REPORT_BASE) -> list[pathlib.Path]:
    """The run directories under base, oldest first."""
    if not base.is_dir():
        return []
    return sorted(p for p in base.iterdir() if p.is_dir() and not p.is_symlink() and re.fullmatch(r"\d{12}", p.name))


###############################################################################
# End
###############################################################################

### local variables:
### no-byte-compile: t
### end:
