# -*- coding: utf-8 -*-

""" #+begin_org
* ~[Summary]~ :: CS commands for cbmProc --- cbm_* control and status verbs
  for gating whether a CBM leaf will materialize when walked.
#+end_org """

####+BEGIN: b:py3:cs:file/dblockControls :classification "cs-u"
""" #+begin_org
* [[elisp:(org-cycle)][| /Control Parameters Of This File/ |]] :: dblk ctrls classifications=cs-u
#+end_org """
####+END:

if 'csInfo' not in globals(): import typing ; csInfo: typing.Dict[str, typing.Any] = { 'moduleName': ['loadAs'], }
csInfo['version'] = '202608150001'
csInfo['status']  = 'inDev'

import typing
import collections
import subprocess

from bisos import b
from bisos.b import cs
from bisos.b import b_io

from bisos.capability import cbmProc_seedInfo


###############################################################################
# Helpers
###############################################################################

def _params() -> cbmProc_seedInfo.CbmProcParams:
    """Resolve CbmProcParams from the planted path at dispatch time."""
    return cbmProc_seedInfo.paramsFromPlantPath()


###############################################################################
# commonParamsSpecify --- register CS parameters used by cbm_* Cmnds.
###############################################################################

def commonParamsSpecify(
        csParams: cs.param.CmndParamDict,
) -> None:
    # cbm_control (write mode) takes the target state as an argument, not a
    # parameter, so no --parName wiring is required here. Kept as a hook for
    # future cbm_* parameters.
    pass


###############################################################################
# cbm_enable --- write cbmProc.control = enabled
###############################################################################

class cbm_enable(cs.Cmnd):
    """Write cbmProc.control = enabled at the planted leaf."""
    cmndParamsMandatory = []
    cmndParamsOptional = []
    cmndArgsLen = {'Min': 0, 'Max': 0}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(
        self,
        rtInv: cs.RtInvoker,
        cmndOutcome: b.op.Outcome,
        argsList: typing.Optional[list[str]] = None,
    ) -> b.op.Outcome:
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        p = _params()
        cbmProc_seedInfo.controlWrite(p.plantDir, cbmProc_seedInfo.ControlState.Enabled)
        b_io.ann.note(f"cbmProc.control = enabled at {p.plantDir}")
        return cmndOutcome.set(opError=b.op.OpError.Success, opResults="enabled")


###############################################################################
# cbm_disable --- write cbmProc.control = disabled (passive; no cleanup)
###############################################################################

class cbm_disable(cs.Cmnd):
    """Write cbmProc.control = disabled at the planted leaf.

    Passive: walker will skip this leaf, but any previously-materialized
    state is left in place. Use cbs_unMaterialize explicitly to tear down.
    """
    cmndParamsMandatory = []
    cmndParamsOptional = []
    cmndArgsLen = {'Min': 0, 'Max': 0}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(
        self,
        rtInv: cs.RtInvoker,
        cmndOutcome: b.op.Outcome,
        argsList: typing.Optional[list[str]] = None,
    ) -> b.op.Outcome:
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        p = _params()
        cbmProc_seedInfo.controlWrite(p.plantDir, cbmProc_seedInfo.ControlState.Disabled)
        b_io.ann.note(f"cbmProc.control = disabled at {p.plantDir}")
        return cmndOutcome.set(opError=b.op.OpError.Success, opResults="disabled")


###############################################################################
# cbm_available --- write cbmProc.control = available (pre-enabled state)
###############################################################################

class cbm_available(cs.Cmnd):
    """Write cbmProc.control = available at the planted leaf.

    Reset state --- present but not yet activated; walker will skip.
    """
    cmndParamsMandatory = []
    cmndParamsOptional = []
    cmndArgsLen = {'Min': 0, 'Max': 0}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(
        self,
        rtInv: cs.RtInvoker,
        cmndOutcome: b.op.Outcome,
        argsList: typing.Optional[list[str]] = None,
    ) -> b.op.Outcome:
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        p = _params()
        cbmProc_seedInfo.controlWrite(p.plantDir, cbmProc_seedInfo.ControlState.Available)
        b_io.ann.note(f"cbmProc.control = available at {p.plantDir}")
        return cmndOutcome.set(opError=b.op.OpError.Success, opResults="available")


###############################################################################
# cbm_isEnabled --- exit 0 iff cbmProc.control = enabled, else 1
###############################################################################

class cbm_isEnabled(cs.Cmnd):
    """Predicate: exit 0 iff cbmProc.control is enabled at the planted leaf."""
    cmndParamsMandatory = []
    cmndParamsOptional = []
    cmndArgsLen = {'Min': 0, 'Max': 0}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(
        self,
        rtInv: cs.RtInvoker,
        cmndOutcome: b.op.Outcome,
        argsList: typing.Optional[list[str]] = None,
    ) -> b.op.Outcome:
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        p = _params()
        state = cbmProc_seedInfo.controlRead(p.plantDir)
        isEnabled = (state == cbmProc_seedInfo.ControlState.Enabled)
        # NOTE: shell exit-code propagation from cs.Cmnd is a known limitation
        # (see bisos.fileObj AI-DevStatus.org Stage 2 #C TODO). Reporting via
        # opResults so callers can test "isEnabled == True" in Python; for
        # shell-side test, grep the printed result.
        b_io.ann.write(f"cbmProc.control = {state.value} (isEnabled={isEnabled})")
        if isEnabled:
            return cmndOutcome.set(opError=b.op.OpError.Success, opResults=True)
        return cmndOutcome.set(opError=b.op.OpError.Success, opResults=False)


###############################################################################
# cbm_status --- print current cbmProc.status contents
###############################################################################

class cbm_status(cs.Cmnd):
    """Print current cbmProc.status contents at the planted leaf."""
    cmndParamsMandatory = []
    cmndParamsOptional = []
    cmndArgsLen = {'Min': 0, 'Max': 0}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(
        self,
        rtInv: cs.RtInvoker,
        cmndOutcome: b.op.Outcome,
        argsList: typing.Optional[list[str]] = None,
    ) -> b.op.Outcome:
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        p = _params()
        contents = cbmProc_seedInfo.statusRead(p.plantDir)
        if not contents:
            b_io.ann.write(f"[{p.capabilityName}] cbmProc.status is empty or absent")
        else:
            b_io.ann.write(f"[{p.capabilityName}] cbmProc.status:\n{contents}")
        return cmndOutcome.set(opError=b.op.OpError.Success, opResults=contents)


###############################################################################
# cbm_control --- print current cbmProc.control (or write with arg)
###############################################################################

class cbm_control(cs.Cmnd):
    """Read cbmProc.control (no args) or write a state (1 arg: available|enabled|disabled)."""
    cmndParamsMandatory = []
    cmndParamsOptional = []
    cmndArgsLen = {'Min': 0, 'Max': 1}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(
        self,
        rtInv: cs.RtInvoker,
        cmndOutcome: b.op.Outcome,
        argsList: typing.Optional[list[str]] = None,
    ) -> b.op.Outcome:
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        p = _params()

        if argsList and len(argsList) == 1:
            requested = argsList[0].strip().lower()
            try:
                targetState = cbmProc_seedInfo.ControlState(requested)
            except ValueError:
                validOptions = [s.value for s in cbmProc_seedInfo.ControlState]
                b_io.eh.problem_usageError(
                    f"Unknown control state {requested!r}. Valid: {validOptions}"
                )
                return b_io.eh.badOutcome(cmndOutcome)
            cbmProc_seedInfo.controlWrite(p.plantDir, targetState)
            b_io.ann.note(f"cbmProc.control = {targetState.value} at {p.plantDir}")
            return cmndOutcome.set(opError=b.op.OpError.Success, opResults=targetState.value)

        # Read-only path
        state = cbmProc_seedInfo.controlRead(p.plantDir)
        b_io.ann.write(f"[{p.capabilityName}] cbmProc.control = {state.value}")
        return cmndOutcome.set(opError=b.op.OpError.Success, opResults=state.value)


###############################################################################
# _dispatchCbs --- shared body for the cbm_materialize family
#
# Model:
#   CBM (this leaf) sits on top of CBS (a separate executable). We do NOT
#   duplicate CBS content at the leaf; we subprocess-invoke the CBS with the
#   requested verb. Non-Python CBS is thus welcome too --- we just exec it.
#
#   1. Gate check: cbmProc.control must be Enabled. If not, statusWrite a
#      skip line and return success (skip is not an error).
#   2. Resolve cbsSpec (absolute path passed through; basename resolved via
#      shutil.which). If unresolvable, statusWrite a failure line and return
#      an error outcome.
#   3. subprocess.run([cbs, '-i', verb, *extraArgs]). Log outcome to
#      cbmProc.status.
###############################################################################

def _dispatchCbs(
        verb: str,
        rtInv: cs.RtInvoker,
        cmndOutcome: b.op.Outcome,
        extraArgs: list[str] | None = None,
) -> b.op.Outcome:
    p = _params()
    plantDir = p.plantDir

    # --- 1. Gate check ---
    state = cbmProc_seedInfo.controlRead(plantDir)
    if state != cbmProc_seedInfo.ControlState.Enabled:
        cbmProc_seedInfo.statusWrite(
            plantDir, f"skipped: control={state.value} at {verb}"
        )
        b_io.ann.write(
            f"[{p.capabilityName}] {verb} skipped (cbmProc.control = "
            f"{state.value}). Run 'cbm_enable' first."
        )
        return cmndOutcome.set(
            opError=b.op.OpError.Success,
            opResults=f"skipped: control={state.value}",
        )

    # --- 2. Resolve cbsSpec ---
    try:
        cbsExec = cbmProc_seedInfo.resolveCbsSpec()
    except ValueError as exc:
        cbmProc_seedInfo.statusWrite(
            plantDir, f"failed: {verb} cbsSpec-unresolvable: {exc}"
        )
        b_io.eh.problem_usageError(str(exc))
        return b_io.eh.badOutcome(cmndOutcome)

    # --- 3. Subprocess dispatch ---
    argv = [str(cbsExec), '-i', verb]
    if extraArgs:
        argv.extend(extraArgs)
    b_io.ann.note(f"[{p.capabilityName}] running: {' '.join(argv)}")
    completed = subprocess.run(argv, check=False)
    rc = completed.returncode

    if rc == 0:
        cbmProc_seedInfo.statusWrite(plantDir, f"ran: {verb} ok")
        return cmndOutcome.set(
            opError=b.op.OpError.Success, opResults=f"ran: {verb} ok"
        )
    else:
        cbmProc_seedInfo.statusWrite(plantDir, f"ran: {verb} failed rc={rc}")
        b_io.ann.write(
            f"[{p.capabilityName}] {verb} failed (subprocess rc={rc})"
        )
        return b_io.eh.badOutcome(cmndOutcome)


###############################################################################
# cbm_materialize --- gate-check + subprocess to cbsSpec -i cbs_materialize
###############################################################################

class cbm_materialize(cs.Cmnd):
    """Materialize this capability: subprocess cbsSpec -i cbs_materialize.

    Gated by cbmProc.control (must be =enabled=). CBS lives elsewhere ---
    CBM does not duplicate it; it invokes it.
    """
    cmndParamsMandatory = []
    cmndParamsOptional = []
    cmndArgsLen = {'Min': 0, 'Max': 0}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(
        self,
        rtInv: cs.RtInvoker,
        cmndOutcome: b.op.Outcome,
        argsList: typing.Optional[list[str]] = None,
    ) -> b.op.Outcome:
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        return _dispatchCbs('cbs_materialize', rtInv, cmndOutcome)


###############################################################################
# cbm_reMaterialize --- subprocess to cbsSpec -i cbs_reMaterialize
###############################################################################

class cbm_reMaterialize(cs.Cmnd):
    """Re-materialize this capability (unMaterialize + materialize)."""
    cmndParamsMandatory = []
    cmndParamsOptional = []
    cmndArgsLen = {'Min': 0, 'Max': 0}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(
        self,
        rtInv: cs.RtInvoker,
        cmndOutcome: b.op.Outcome,
        argsList: typing.Optional[list[str]] = None,
    ) -> b.op.Outcome:
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        return _dispatchCbs('cbs_reMaterialize', rtInv, cmndOutcome)


###############################################################################
# cbm_unMaterialize --- subprocess to cbsSpec -i cbs_unMaterialize
###############################################################################

class cbm_unMaterialize(cs.Cmnd):
    """Un-materialize this capability (explicit teardown; not triggered by cbm_disable)."""
    cmndParamsMandatory = []
    cmndParamsOptional = []
    cmndArgsLen = {'Min': 0, 'Max': 0}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(
        self,
        rtInv: cs.RtInvoker,
        cmndOutcome: b.op.Outcome,
        argsList: typing.Optional[list[str]] = None,
    ) -> b.op.Outcome:
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        return _dispatchCbs('cbs_unMaterialize', rtInv, cmndOutcome)


###############################################################################
# cbm_sbom --- subprocess to cbsSpec -i cbs_sbom
###############################################################################

class cbm_sbom(cs.Cmnd):
    """Run the sbom (software bill of materials) step of this CBS."""
    cmndParamsMandatory = []
    cmndParamsOptional = []
    cmndArgsLen = {'Min': 0, 'Max': 0}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(
        self,
        rtInv: cs.RtInvoker,
        cmndOutcome: b.op.Outcome,
        argsList: typing.Optional[list[str]] = None,
    ) -> b.op.Outcome:
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        return _dispatchCbs('cbs_sbom', rtInv, cmndOutcome)


###############################################################################
# examples_csu --- registered by the seed's examples Cmnd
###############################################################################

def examples_csu() -> None:
    od = collections.OrderedDict
    cmnd = cs.examples.cmndEnter

    cs.examples.menuChapter('=cbm_*= --- Capability Control (enable/disable/status)')

    cs.examples.menuSection('State readers')
    cmnd('cbm_control',    comment="# read cbmProc.control")
    cmnd('cbm_status',     comment="# read cbmProc.status")
    cmnd('cbm_isEnabled',  comment="# 0 iff enabled")

    cs.examples.menuSection('State writers')
    cmnd('cbm_enable',     comment="# --> enabled")
    cmnd('cbm_disable',    comment="# --> disabled (passive; no cleanup)")
    cmnd('cbm_available',  comment="# --> available")
    cs.examples.execInsert(
        "./cbmProc.spcs -i cbm_control enabled     # equivalent to cbm_enable"
    )

    cs.examples.menuChapter('=cbm_*= --- Materialization (subprocess to cbsSpec)')
    cs.examples.menuSection('Lifecycle')
    cmnd('cbm_materialize',    comment="# subprocess: <cbsSpec> -i cbs_materialize (gated)")
    cmnd('cbm_reMaterialize',  comment="# unMaterialize + materialize")
    cmnd('cbm_unMaterialize',  comment="# explicit teardown")
    cmnd('cbm_sbom',           comment="# just the sbom step")


###############################################################################
# End
###############################################################################

### local variables:
### no-byte-compile: t
### end:
