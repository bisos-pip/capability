# -*- coding: utf-8 -*-

""" #+begin_org
* ~[Summary]~ :: SeedInfo for cbmProc --- capability-name declaration,
  path-derived plant directory, and cbmProc.control / cbmProc.status
  file-based enable/disable state for a CBM (Capability Bundle
  Materialization) leaf.
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
csInfo['version'] = '202608150001'
csInfo['status']  = 'inDev'

import typing
import enum
import datetime
import pathlib
import shutil
from dataclasses import dataclass

from bisos.csSeed import seedsLib


###############################################################################
# Control-file states (Q2 --- start with three, refine later)
###############################################################################

@enum.unique
class ControlState(enum.Enum):
    Available = "available"     # present but not activated; walker skips
    Enabled   = "enabled"       # walker materializes
    Disabled  = "disabled"      # walker skips; passive (no auto-un-materialize)


CONTROL_FILENAME = "cbmProc.control"
STATUS_FILENAME  = "cbmProc.status"

# Default when the .control file is absent --- treat as available (safe).
DEFAULT_CONTROL = ControlState.Available


###############################################################################
# CbmProcParams --- what we derive from the planted path
###############################################################################

@dataclass
class CbmProcParams:
    """Parameters derived from a cbmProc.spcs plant path.

    plantPath      --- resolved absolute path to the .spcs file.
    plantDir       --- directory containing the .spcs (where .control /
                       .status also live).
    capabilityName --- from cbmProc_seedInfo.setup(capabilityName=...) if
                       the .spcs called it, else the leaf directory name.
    """
    plantPath: str = ""
    plantDir: pathlib.Path | None = None
    capabilityName: str = ""


###############################################################################
# paramsFromPlantPath --- pure function, no side effects
###############################################################################

def paramsFromPlantPath(plantPath: str | None = None) -> CbmProcParams:
    """Resolve plant path -> CbmProcParams.

    The plant directory is the .spcs file's parent. capabilityName is taken
    from the singleton if the .spcs set it via setup(), else falls back to
    the leaf directory name.
    """
    if plantPath is None:
        plantPath = seedsLib.seededCsxuInfo.plantOfThisSeed
    if plantPath is None:
        raise ValueError("plantPath is None and plantOfThisSeed is not set")

    resolvedFile = pathlib.Path(plantPath).resolve()
    if resolvedFile.is_file():
        plantDir = resolvedFile.parent
    else:
        plantDir = resolvedFile

    capName = cbmProcSeedInfo.capabilityName
    if not capName:
        capName = plantDir.name

    return CbmProcParams(
        plantPath=str(resolvedFile),
        plantDir=plantDir,
        capabilityName=capName,
    )


###############################################################################
# CbmProcSeedInfo --- singleton populated by the .spcs's setup() call
###############################################################################

@dataclass
class CbmProcSeedInfo:
    capabilityName: str | None = None
    cbsSpec: str | None = None
    examplesFuncsList: list[typing.Callable] | None = None

    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


cbmProcSeedInfo = CbmProcSeedInfo()


def setup(
        capabilityName: str | None = None,
        cbsSpec: str | None = None,
        examplesFuncsList: list[typing.Callable] | None = None,
) -> None:
    """Populate the CbmProcSeedInfo singleton from a cbmProc.spcs.

    cbsSpec: path (absolute, or containing a slash) OR basename (PATH-resolved
    via shutil.which). See resolveCbsSpec().
    """
    if capabilityName is not None:
        cbmProcSeedInfo.capabilityName = capabilityName
    if cbsSpec is not None:
        cbmProcSeedInfo.cbsSpec = cbsSpec
    if examplesFuncsList is not None:
        cbmProcSeedInfo.examplesFuncsList = examplesFuncsList


###############################################################################
# resolveCbsSpec --- turn a cbsSpec (path or basename) into an executable path
#
# Rule (deliberately simple, no magic):
#   - Absolute path or path containing '/' --> use as-is (must exist + be executable).
#   - Bare basename --> resolve via shutil.which() against $PATH.
#
# Absolute lets the user pin a CBS to a specific location.
# Basename lets the user rely on deployment putting the CBS on PATH.
###############################################################################

def resolveCbsSpec(cbsSpec: str | None = None) -> pathlib.Path:
    """Resolve cbsSpec to an absolute executable path.

    If cbsSpec is None, reads cbmProcSeedInfo.cbsSpec. Raises ValueError with
    a clear message on unresolvable or missing values (no silent None).
    """
    if cbsSpec is None:
        cbsSpec = cbmProcSeedInfo.cbsSpec
    if cbsSpec is None:
        raise ValueError(
            "cbsSpec is None. The planted cbmProc.spcs must call "
            "cbmProc_seedInfo.setup(cbsSpec=...)."
        )

    if '/' in cbsSpec or cbsSpec.startswith('~'):
        # Explicit path form (absolute or relative-with-slash or ~).
        # Expand ~ and make absolute, but do NOT follow symlinks: a spread-planted CBS (e.g. a PALS's
        # cbm/pals-cbs.spcs -> bisos.pals's generic one) takes its parameters from where it is planted,
        # so it must run by the path it is planted at. Require it to exist.
        resolved = pathlib.Path(cbsSpec).expanduser().absolute()
        if not resolved.exists():
            raise ValueError(
                f"cbsSpec {cbsSpec!r} resolved to {resolved} which does not exist."
            )
        return resolved

    # Basename form: consult PATH.
    onPath = shutil.which(cbsSpec)
    if onPath is None:
        raise ValueError(
            f"cbsSpec {cbsSpec!r} not found on PATH. Either add its directory "
            f"to PATH or use an absolute path in setup(cbsSpec=...)."
        )
    return pathlib.Path(onPath).absolute()   # not resolved: see the explicit-path form above


###############################################################################
# controlRead / controlWrite --- gate-file accessors
#
# Format: plain text, one line, matching a ControlState value.
# NOT JSON (per Q3 decision --- refine later if state grows).
###############################################################################

def controlPath(plantDir: pathlib.Path) -> pathlib.Path:
    return plantDir / CONTROL_FILENAME


def controlRead(plantDir: pathlib.Path) -> ControlState:
    """Read cbmProc.control; return ControlState. Missing file -> DEFAULT_CONTROL."""
    path = controlPath(plantDir)
    if not path.exists():
        return DEFAULT_CONTROL
    raw = path.read_text().strip()
    if not raw:
        return DEFAULT_CONTROL
    try:
        return ControlState(raw)
    except ValueError:
        # Unknown value --- treat as available (safe default). Do NOT raise;
        # callers may be dispatching a cbm_control write that's about to fix it.
        return DEFAULT_CONTROL


def controlWrite(plantDir: pathlib.Path, state: ControlState) -> None:
    """Write cbmProc.control with a single line matching the ControlState value."""
    controlPath(plantDir).write_text(f"{state.value}\n")


###############################################################################
# statusRead / statusWrite --- outcome log
#
# Format: plain text, one line per event (append). Machine-written by the seed
# after each cbs_* dispatch. NOT JSON (per Q4 decision).
###############################################################################

def statusPath(plantDir: pathlib.Path) -> pathlib.Path:
    return plantDir / STATUS_FILENAME


def statusRead(plantDir: pathlib.Path) -> str:
    """Return the full contents of cbmProc.status, or empty string if absent."""
    path = statusPath(plantDir)
    if not path.exists():
        return ""
    return path.read_text()


def statusWrite(plantDir: pathlib.Path, line: str) -> None:
    """Append a timestamped line to cbmProc.status.

    Callers pass a short one-line message like:
      'skipped: control=disabled at cbs_materialize'
      'ran: cbs_materialize ok'
      'ran: cbs_materialize failed rc=1'
    """
    ts = datetime.datetime.now().isoformat(timespec='seconds')
    with statusPath(plantDir).open('a') as fh:
        fh.write(f"{ts}  {line}\n")


###############################################################################
# leafProcessorNames --- for ftoBranch_seedInfo.setup(leafProcessors=...)
###############################################################################

def leafProcessorNames() -> list[str]:
    """Filenames that identify a cbmProc leaf directory (markerless walks)."""
    return ['cbmProc.spcs']


###############################################################################
# walkExamples --- WalkExampleSpec list for fto_forwardToLeaves menus
#
# The leaf's PUBLIC interface is cbm_* only (cbm_* verbs sit on top of and
# subprocess-invoke the underlying cbs_* verbs against the referenced CBS).
# A branch .spcs imports this function and passes the result to
# ftoBranch_seedInfo.setup(leafExamples=...).
###############################################################################

def walkExamples() -> list:
    """Return WalkExampleSpec entries for cbmProc leaves.

    Lazy import of WalkExampleSpec avoids a hard bisos.fileObj dependency
    at cbmProc_seedInfo module-load time.
    """
    from bisos.fileObj.ftoBranch_seedInfo import WalkExampleSpec

    return [
        # -- Read-only (state inspection at leaves) ---------------------
        WalkExampleSpec(
            cmndName='cbm_status',
            comment="# read cbmProc.status at each leaf",
            tags=frozenset({'read-only'}),
        ),
        WalkExampleSpec(
            cmndName='cbm_control',
            comment="# read cbmProc.control at each leaf",
            tags=frozenset({'read-only'}),
        ),
        WalkExampleSpec(
            cmndName='cbm_isEnabled',
            comment="# exit 0 if enabled, else 1",
            tags=frozenset({'read-only'}),
        ),
        # -- Control state changes --------------------------------------
        WalkExampleSpec(
            cmndName='cbm_enable',
            comment="# set cbmProc.control = enabled",
            tags=frozenset({'control'}),
        ),
        WalkExampleSpec(
            cmndName='cbm_disable',
            comment="# set cbmProc.control = disabled (passive)",
            tags=frozenset({'control'}),
        ),
        WalkExampleSpec(
            cmndName='cbm_available',
            comment="# set cbmProc.control = available (pre-enabled)",
            tags=frozenset({'control'}),
        ),
        # -- Materialization lifecycle (subprocess to cbsSpec; gated) ----
        WalkExampleSpec(
            cmndName='cbm_materialize',
            comment="# subprocess: <cbsSpec> -i cbs_materialize (enabled only)",
            tags=frozenset({'destructive', 'materialize'}),
        ),
        WalkExampleSpec(
            cmndName='cbm_reMaterialize',
            comment="# unMaterialize + materialize",
            tags=frozenset({'destructive', 'materialize'}),
        ),
        WalkExampleSpec(
            cmndName='cbm_unMaterialize',
            comment="# explicit teardown",
            tags=frozenset({'destructive'}),
        ),
        WalkExampleSpec(
            cmndName='cbm_sbom',
            comment="# just the sbom step",
            tags=frozenset({}),
        ),
    ]


###############################################################################
# End
###############################################################################

### local variables:
### no-byte-compile: t
### end:
