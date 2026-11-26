#!/bin/bash -i
#
# Smoke tests for bisos.capability new files: cbmProc_seedInfo,
# cbmProc_seed, cbmProc_csu, cbmProc-seed.cs.
#
# Non-invasive: does NOT test cba_csu / cba_seed / cba_sysd_seed --- those
# ship as they are.

# Safety check: must run from a directory named "tests"
if [[ "$(basename "$PWD")" != "tests" ]]; then
    echo "ERROR: verify.sh must be run from a directory named 'tests'." >&2
    echo "  Current PWD: $PWD" >&2
    exit 1
fi

# --- CS entry points: smoke test (no args → examples/usage, non-zero ok) ---

lpDo ../bin/cbmProc-seed.cs

# --- cbmProc_csu Cmnds: import + class presence smoke test ---

lpDo python3 -c "
from bisos.capability import cbmProc_csu as m
cbmCmnds = [
    'cbm_enable', 'cbm_disable', 'cbm_available',
    'cbm_isEnabled', 'cbm_status', 'cbm_control',
    'cbm_materialize', 'cbm_reMaterialize', 'cbm_unMaterialize', 'cbm_sbom',
    'cbm_bootstrap',
]
failed = 0
for n in cbmCmnds:
    if not hasattr(m, n): print(f'  [FAIL] missing Cmnd: {n}'); failed += 1
    else: print(f'  [PASS] Cmnd present: {n}')
if not hasattr(m, 'commonParamsSpecify'):
    print('  [FAIL] commonParamsSpecify missing'); failed += 1
else:
    print('  [PASS] commonParamsSpecify present')
if not hasattr(m, 'examples_csu'):
    print('  [FAIL] examples_csu missing'); failed += 1
else:
    print('  [PASS] examples_csu present')
import sys; sys.exit(failed)
"

# --- cbmProc_seedInfo: singleton + factories smoke test ---

lpDo python3 -c "
from bisos.capability import cbmProc_seedInfo as si
failed = 0
for sym in ('CbmProcSeedInfo', 'CbmProcParams', 'ControlState',
            'cbmProcSeedInfo', 'setup', 'paramsFromPlantPath',
            'controlRead', 'controlWrite', 'statusRead', 'statusWrite',
            'leafProcessorNames', 'walkExamples', 'resolveCbsSpec',
            'CONTROL_FILENAME', 'STATUS_FILENAME',
            'STATUS_BASE', 'leafRel', 'statusDir', 'statusPath',
            'BOOTSTRAP_FILENAME', 'bootstrapPath'):
    if not hasattr(si, sym): print(f'  [FAIL] missing symbol: {sym}'); failed += 1
    else: print(f'  [PASS] symbol present: {sym}')

# ControlState members
expected = {'Available', 'Enabled', 'Disabled'}
got = {m.name for m in si.ControlState}
if got != expected:
    print(f'  [FAIL] ControlState members: got {got}, expected {expected}'); failed += 1
else:
    print(f'  [PASS] ControlState members = {sorted(got)}')

# leafProcessorNames returns cbmProc.spcs
lps = si.leafProcessorNames()
if lps != ['cbmProc.spcs']:
    print(f'  [FAIL] leafProcessorNames() = {lps}, expected [\"cbmProc.spcs\"]'); failed += 1
else:
    print(f'  [PASS] leafProcessorNames() = {lps}')

import sys; sys.exit(failed)
"

# --- controlRead / controlWrite + statusRead / statusWrite --- scratch dir ---

lpDo python3 -c "
import pathlib, tempfile, sys
from bisos.capability import cbmProc_seedInfo as si

failed = 0
with tempfile.TemporaryDirectory() as td:
    plantDir = pathlib.Path(td)

    # Absent .control file --> DEFAULT_CONTROL (Available)
    state = si.controlRead(plantDir)
    if state != si.ControlState.Available:
        print(f'  [FAIL] absent .control default: got {state}, expected Available'); failed += 1
    else:
        print(f'  [PASS] absent .control default = Available')

    # Write + read enabled
    si.controlWrite(plantDir, si.ControlState.Enabled)
    state = si.controlRead(plantDir)
    if state != si.ControlState.Enabled:
        print(f'  [FAIL] write/read enabled: got {state}'); failed += 1
    else:
        print(f'  [PASS] write/read enabled roundtrip')

    # Write + read disabled
    si.controlWrite(plantDir, si.ControlState.Disabled)
    state = si.controlRead(plantDir)
    if state != si.ControlState.Disabled:
        print(f'  [FAIL] write/read disabled: got {state}'); failed += 1
    else:
        print(f'  [PASS] write/read disabled roundtrip')

    # Write + read available
    si.controlWrite(plantDir, si.ControlState.Available)
    state = si.controlRead(plantDir)
    if state != si.ControlState.Available:
        print(f'  [FAIL] write/read available: got {state}'); failed += 1
    else:
        print(f'  [PASS] write/read available roundtrip')

    # Unknown value --> DEFAULT (safe fallback, no raise)
    (plantDir / si.CONTROL_FILENAME).write_text('junk\n')
    state = si.controlRead(plantDir)
    if state != si.ControlState.Available:
        print(f'  [FAIL] unknown value fallback: got {state}'); failed += 1
    else:
        print(f'  [PASS] unknown value falls back to Available')

    # Status: under STATUS_BASE (here a scratch one), never in the leaf
    si.STATUS_BASE = plantDir / 'var' / 'cbm'

    # Status: empty read
    contents = si.statusRead(plantDir)
    if contents != '':
        print(f'  [FAIL] absent .status: got {contents!r}, expected empty'); failed += 1
    else:
        print(f'  [PASS] absent .status returns empty string')

    # Status: append two lines, both should be present with timestamps
    si.statusWrite(plantDir, 'ran: cbs_materialize ok')
    si.statusWrite(plantDir, 'skipped: control=disabled at cbs_materialize')
    contents = si.statusRead(plantDir)
    lines = [l for l in contents.strip().split('\n') if l]
    if len(lines) != 2:
        print(f'  [FAIL] statusWrite append: got {len(lines)} lines'); failed += 1
    elif 'ran: cbs_materialize ok' not in lines[0]:
        print(f'  [FAIL] statusWrite line 1: {lines[0]!r}'); failed += 1
    elif 'skipped: control=disabled' not in lines[1]:
        print(f'  [FAIL] statusWrite line 2: {lines[1]!r}'); failed += 1
    else:
        print(f'  [PASS] statusWrite appends 2 timestamped lines')

    if (plantDir / si.STATUS_FILENAME).exists():
        print(f'  [FAIL] statusWrite wrote in the leaf'); failed += 1
    else:
        print(f'  [PASS] statusWrite writes nothing in the leaf')
    link = si.statusDir(plantDir) / si.STATUS_LEAF_LINK
    if not (link.is_symlink() and link.resolve() == plantDir.resolve()):
        print(f'  [FAIL] leaf link: {link}'); failed += 1
    else:
        print(f'  [PASS] leaf link points back at the leaf')

# leafRel: the vcMode is dropped; outside bxRepos, _abs_/<path>
for leaf, rel in (
        ('/bisos/git/anon/bxRepos/bxObjects/bro_x/kafka', 'bxObjects/bro_x/kafka'),
        ('/bisos/git/auth/bxRepos/bxObjects/bro_x/kafka', 'bxObjects/bro_x/kafka'),
        ('/home/bystar/site', '_abs_/home/bystar/site')):
    got = str(si.leafRel(pathlib.Path(leaf)))
    if got != rel:
        print(f'  [FAIL] leafRel({leaf}) = {got}, expected {rel}'); failed += 1
    else:
        print(f'  [PASS] leafRel({leaf}) = {got}')

sys.exit(failed)
"

# --- paramsFromPlantPath: resolves plant dir + capabilityName fallback ---

lpDo python3 -c "
import pathlib, tempfile, sys
from bisos.capability import cbmProc_seedInfo as si
from bisos.csSeed import seedsLib

failed = 0
with tempfile.TemporaryDirectory() as td:
    # Build a fake leaf: <td>/airflow/cbmProc.spcs
    leafDir = pathlib.Path(td) / 'airflow'
    leafDir.mkdir()
    plantFile = leafDir / 'cbmProc.spcs'
    plantFile.write_text('# stub\n')

    # Explicit plantPath argument path
    p = si.paramsFromPlantPath(str(plantFile))
    if p.plantDir != leafDir.resolve():
        print(f'  [FAIL] plantDir: got {p.plantDir}, expected {leafDir.resolve()}'); failed += 1
    else:
        print(f'  [PASS] plantDir resolves to leaf directory')

    # capabilityName fallback = leaf dir name when setup() has not been called
    # (the singleton may retain state from earlier tests --- reset it)
    si.cbmProcSeedInfo.capabilityName = None
    p = si.paramsFromPlantPath(str(plantFile))
    if p.capabilityName != 'airflow':
        print(f'  [FAIL] capabilityName fallback: got {p.capabilityName!r}, expected airflow'); failed += 1
    else:
        print(f'  [PASS] capabilityName fallback = airflow (from dir name)')

    # setup() override wins
    si.setup(capabilityName='someOtherName')
    p = si.paramsFromPlantPath(str(plantFile))
    if p.capabilityName != 'someOtherName':
        print(f'  [FAIL] setup() override: got {p.capabilityName!r}'); failed += 1
    else:
        print(f'  [PASS] setup(capabilityName=...) overrides fallback')

    # plantPath is None + plantOfThisSeed unset --> ValueError
    seedsLib.seededCsxuInfo.plantOfThisSeed = None
    try:
        si.paramsFromPlantPath()
        print(f'  [FAIL] None plantPath + unset seededCsxuInfo: should raise'); failed += 1
    except ValueError:
        print(f'  [PASS] None plantPath raises ValueError')

sys.exit(failed)
"

# --- walkExamples: returns non-empty list of WalkExampleSpec entries ---

lpDo python3 -c "
from bisos.capability import cbmProc_seedInfo as si
from bisos.fileObj.ftoBranch_seedInfo import WalkExampleSpec
specs = si.walkExamples()
failed = 0
if not isinstance(specs, list) or len(specs) == 0:
    print(f'  [FAIL] walkExamples returned empty/non-list'); failed += 1
else:
    print(f'  [PASS] walkExamples returned {len(specs)} entries')
for i, s in enumerate(specs):
    if not isinstance(s, WalkExampleSpec):
        print(f'  [FAIL] spec[{i}] is not WalkExampleSpec: {type(s)}'); failed += 1

# Coverage: expect both cbm_* and cbs_* verbs present
names = {s.cmndName for s in specs}
for expected in ('cbm_enable', 'cbm_disable', 'cbm_status', 'cbm_materialize', 'cbm_reMaterialize', 'cbm_unMaterialize'):
    if expected not in names:
        print(f'  [FAIL] walkExamples missing verb: {expected}'); failed += 1
    else:
        print(f'  [PASS] walkExamples includes: {expected}')
import sys; sys.exit(failed)
"

# --- cbsSpec: setup() roundtrip + resolveCbsSpec() forms ---

lpDo python3 -c "
import pathlib, tempfile, os, sys
from bisos.capability import cbmProc_seedInfo as si

failed = 0

# setup() records cbsSpec in the singleton
si.setup(cbsSpec='airflow-cbs.pcs')
if si.cbmProcSeedInfo.cbsSpec != 'airflow-cbs.pcs':
    print(f'  [FAIL] cbsSpec singleton write: got {si.cbmProcSeedInfo.cbsSpec!r}'); failed += 1
else:
    print(f'  [PASS] setup(cbsSpec=...) records into singleton')

# resolveCbsSpec: absolute path form
with tempfile.TemporaryDirectory() as td:
    fake = pathlib.Path(td) / 'fake-cbs.pcs'
    fake.write_text('#!/bin/sh\nexit 0\n')
    fake.chmod(0o755)
    got = si.resolveCbsSpec(str(fake))
    if got != fake.resolve():
        print(f'  [FAIL] resolveCbsSpec absolute: got {got}, expected {fake.resolve()}'); failed += 1
    else:
        print(f'  [PASS] resolveCbsSpec: absolute path passes through')

    # Path with slash but not absolute --- also 'explicit path form'
    rel = os.path.relpath(str(fake), start=os.getcwd())
    if '/' in rel:
        got = si.resolveCbsSpec(rel)
        # absolute, not resolved (2026-10-19: a spread-planted CBS runs by the path it is planted at)
        if not got.is_absolute() or got.resolve() != fake.resolve():
            print(f'  [FAIL] resolveCbsSpec relative-with-slash: got {got}'); failed += 1
        else:
            print(f'  [PASS] resolveCbsSpec: relative path with slash resolves')

# resolveCbsSpec: absolute path that does NOT exist --- ValueError
try:
    si.resolveCbsSpec('/definitely/does/not/exist/xyz-cbs.pcs')
    print(f'  [FAIL] resolveCbsSpec nonexistent absolute: should raise'); failed += 1
except ValueError as e:
    print(f'  [PASS] resolveCbsSpec: nonexistent absolute raises ValueError')

# resolveCbsSpec: basename via shutil.which --- use a real basename we know is on PATH.
# .resolve() follows symlinks (e.g. sh -> dash), so we check it returned SOMETHING
# absolute and executable rather than an exact basename match.
got = si.resolveCbsSpec('sh')
if not got.is_absolute() or not os.access(str(got), os.X_OK):
    print(f'  [FAIL] resolveCbsSpec basename \"sh\": got {got} (not absolute or not executable)'); failed += 1
else:
    print(f'  [PASS] resolveCbsSpec: basename \"sh\" resolves via PATH -> {got}')

# resolveCbsSpec: basename NOT on PATH --- ValueError
try:
    si.resolveCbsSpec('definitely-not-on-path-xyz-cbs.pcs')
    print(f'  [FAIL] resolveCbsSpec missing basename: should raise'); failed += 1
except ValueError:
    print(f'  [PASS] resolveCbsSpec: missing basename raises ValueError')

# resolveCbsSpec: None + singleton unset --- ValueError
si.cbmProcSeedInfo.cbsSpec = None
try:
    si.resolveCbsSpec()
    print(f'  [FAIL] resolveCbsSpec(None) + singleton None: should raise'); failed += 1
except ValueError:
    print(f'  [PASS] resolveCbsSpec: None arg + unset singleton raises ValueError')

sys.exit(failed)
"

# --- cbmVerify (Stage 5): cbm_verify, fullyVerify, verifyCompare; the pure functions ---

lpDo python3 -c "
import sys, pathlib, tempfile
from bisos.capability import cbmVerify as v, cbmProc_csu, cbmProc_seedInfo as si, sysCbmManage_csu as scm
failed = 0
def check(ok, what):
    global failed
    print(('  [PASS] ' if ok else '  [FAIL] ') + what); failed += 0 if ok else 1

check(hasattr(cbmProc_csu, 'cbm_verify'), 'Cmnd present: cbm_verify')
check(hasattr(scm, 'fullyVerify') and hasattr(scm, 'verifyCompare'), 'Cmnds present: fullyVerify, verifyCompare')
check('verifySpec' in si.setup.__code__.co_varnames and 'verifyUnits' in si.setup.__code__.co_varnames
      and 'hereName' in si.setup.__code__.co_varnames, 'setup() takes hereName, verifyUnits, verifySpec')

# The verdict line convention
m = v.VERDICT_RE.match('grafana verify: fail 2 problem(s): not installed')
check(m and m.group(2) == 'fail' and m.group(3).startswith('2 problem'), 'VERDICT_RE reads a fail line')
check(v.VERDICT_RE.match('    echo grafana verify: ok') is None, 'VERDICT_RE ignores an indented echo')

# The exit code of the last materialize: recorded, not trusted
st = '2026-11-26T03:50:27  ran: cbs_materialize ok\n2026-11-26T04:00:00  ran: cbs_materialize failed rc=5\n'
check(v.materializeRc(st) == 5 and v.materializeRc('') is None, 'materializeRc reads the last outcome')

# A PALS name keeps its suffix; a banna name gets it
check(v.hereFqdn('example.org.internal') == 'example.org.internal', 'hereFqdn keeps a full .internal name')
check(v.hereFqdn('grafana').endswith('.internal') and v.hereFqdn('grafana').count('.') == 1, 'hereFqdn adds the suffix')

# A masked failure: rc 0, evidence fail
rec = v._withRcAgreement({'materializeRc': 0, 'verdict': 'fail'})
check(rec['rcAgrees'] == 'masked', 'rc 0 with verdict fail is masked')

# logScan: finds a leaf failure, marks it masked, and does not match echoed script source
log = '\n'.join(['[demo] running: /x/demo-cbs.pcs -i cbs_materialize',
                 '        echo \'banna: ERROR: uid 503 is held\' >&2',
                 'io.eh.badOutcome:  -- InvokedBy NOTYET, Operation Failed: Stdcmnd=x Error=5 -- None',
                 'ran: cbs_materialize ok'])
with tempfile.NamedTemporaryFile('w', suffix='-log.org', delete=False) as f:
    f.write(log + '\n')
hits = v.logScan([pathlib.Path(f.name)])
check(len(hits) == 1 and hits[0]['leaf'] == 'demo' and hits[0]['masked'], 'logScan: one masked hit, the echo ignored')

# compare: a new failure and a fix
leaf = lambda name, verdict: {'leafRel': 'x/' + name, 'capabilityName': name, 'verdict': verdict, 'detail': 'd',
                              'materializeRc': 0, 'rcAgrees': None}
old = {'generatedAt': 't0', 'verdict': 'fail', 'leaves': [leaf('a', 'ok'), leaf('b', 'fail')], 'platform': []}
new = {'generatedAt': 't1', 'verdict': 'fail', 'leaves': [leaf('a', 'fail'), leaf('b', 'ok')], 'platform': []}
c = v.compare(old, new)
check([x.split(':')[0] for x in c['newFailures']] == ['a'] and c['fixed'] == ['b'], 'compare: new failure a, fixed b')

sys.exit(failed)
"
