# -*- coding: utf-8 -*-

""" #+begin_org
* ~[Summary]~ :: cba_sysd_csu.py :: cba_ (Capabilities Bundle Abstraction) sysd_ (systemd) csu (Command Services Unit)
#+end_org """

####+BEGIN: b:py3:cs:file/dblockControls :classification "cs-u"
""" #+begin_org
* [[elisp:(org-cycle)][| /Control Parameters Of This File/ |]] :: dblk ctrls classifications=cs-u
#+BEGIN_SRC emacs-lisp
(setq-local b:dblockControls t) ; (setq-local b:dblockControls nil)
(put 'b:dblockControls 'py3:cs:Classification "cs-u") ; one of cs-mu, cs-u, cs-lib, bpf-lib, pyLibPure
#+END_SRC
#+RESULTS:
: cs-u
#+end_org """
####+END:

####+BEGIN: b:prog:file/proclamations :outLevel 1
""" #+begin_org
* *[[elisp:(org-cycle)][| Proclamations |]]* :: Libre-Halaal Software --- Part Of BISOS ---  Poly-COMEEGA Format.
** This is Libre-Halaal Software. © Neda Communications, Inc. Subject to AGPL.
** It is part of BISOS (ByStar Internet Services OS)
** Best read and edited  with Blee in Poly-COMEEGA (Polymode Colaborative Org-Mode Enhance Emacs Generalized Authorship)
#+end_org """
####+END:

####+BEGIN: b:prog:file/particulars :authors ("./inserts/authors-mb.org")
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: Authors, version
** This File: /bisos/git/bxRepos/bisos-pip/capability/py3/bisos/capability/cbm_csu.py
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """
####+END:

####+BEGIN: b:py3:file/particulars-csInfo :status "inUse"
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars-csInfo |]]*
#+end_org """
import typing
csInfo: typing.Dict[str, typing.Any] = { 'moduleName': ['seedIf'], }
csInfo['version'] = '202409222401'
csInfo['status']  = 'inUse'
csInfo['panel'] = 'seedIf-Panel.org'
csInfo['groupingType'] = 'IcmGroupingType-pkged'
csInfo['cmndParts'] = 'IcmCmndParts[common] IcmCmndParts[param]'
####+END:

""" #+begin_org
* [[elisp:(org-cycle)][| ~Description~ |]] :: [[file:/bisos/git/auth/bxRepos/blee-binders/bisos-core/COMEEGA/_nodeBase_/fullUsagePanel-en.org][BISOS COMEEGA Panel]]
Module description comes here.
** Relevant Panels:
** Status: In use with BISOS
** /[[elisp:(org-cycle)][| Planned Improvements |]]/ :
*** TODO complete fileName in particulars.
#+end_org """

####+BEGIN: b:prog:file/orgTopControls :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Controls |]] :: [[elisp:(delete-other-windows)][(1)]] | [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]]

#+end_org """
####+END:

####+BEGIN: b:py3:file/workbench :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Workbench |]] :: [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pydoc ./%s" (bx:buf-fname))))][pydoc]] || [[elisp:(python-check (format "/bisos/pipx/bin/pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "/bisos/pipx/bin/pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "/bisos/pipx/bin/pycodestyle %s" (bx:buf-fname))))][pycodestyle]] | [[elisp:(python-check (format "/bisos/pipx/bin/flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "/bisos/pipx/bin/pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: b:py3:cs:framework/imports :basedOn "classification"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CsFrmWrk   [[elisp:(outline-show-subtree+toggle)][||]] *Imports* =Based on Classification=cs-u=
#+end_org """
from bisos import b
from bisos.b import cs
from bisos.b import b_io
from bisos.common import csParam

import collections
####+END:

import os
import subprocess
import json
import pathlib
# import time

# import os
# import sys

from pathlib import Path
from bisos.bpo import bpo
from bisos.platform import platformBases_csu
from bisos.platform import platformBases
from bisos.basics import pathPlus
from bisos.capability import cbmVerify


####+BEGIN: b:py3:cs:orgItem/section :title "CSU-Lib Examples" :comment "-- Providing examples_csu"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *CSU-Lib Examples* -- Providing examples_csu  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: bx:dblock:python:func :funcName "commonParamsSpecify" :funcType "ParSpec" :retType "" :deco "" :argsList "csParams"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-ParSpec  [[elisp:(outline-show-subtree+toggle)][||]] /commonParamsSpecify/ retType= argsList=(csParams)  [[elisp:(org-cycle)][| ]]
#+end_org """
def commonParamsSpecify(
    csParams,
):
####+END:
    pass

####+BEGIN: b:py3:cs:func/typing :funcName "examples_csu" :funcType "eType" :retType "" :deco "default" :argsList ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-eType  [[elisp:(outline-show-subtree+toggle)][||]] /examples_csu/  deco=default  [[elisp:(org-cycle)][| ]]
#+end_org """
@cs.track(fnLoc=True, fnEntry=True, fnExit=True)
def examples_csu(
####+END:
        sectionTitle: typing.AnyStr = "default",
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ] Examples of Service Access Instance Commands.
    #+end_org """

    od = collections.OrderedDict
    cmnd = cs.examples.cmndEnter
    # literal = cs.examples.execInsert

    if sectionTitle == 'default':
        cs.examples.menuChapter('*Materialization Dispatch Commands*')

    cs.examples.menuSection("*Full Dispatch Full Cap Materialization*")

    cmnd('fullyMaterialize')

    cs.examples.menuSection("*Verify --- is this platform healthy? (read-only; AI-WorkPlan.org Stage 5)*")

    cmnd('fullyVerify', comment=" # every leaf's cbm_verify + platform checks + log scan -> /bisos/var/cbm/verify/latest/")
    cmnd('fullyVerify', args="~/sysCbmFullyMaterialize-*-log.org", comment=" # with these logs scanned")
    cmnd('verifyCompare', comment=" # the previous report against the latest")
    cmnd('verifyCompare', args="/bisos/var/cbm/verify/<old> /bisos/var/cbm/verify/<new>", comment=" # two given reports")


""" #+begin_org
*  ---- Devider ----
#+end_org """

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "fullyMaterialize" :extent "verify" :comment "stdin as input" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv "methodInvokeArg"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<fullyMaterialize>>  *stdin as input*  =verify= ro=cli pyInv=methodInvokeArg   [[elisp:(org-cycle)][| ]]
#+end_org """
class fullyMaterialize(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             methodInvokeArg: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:
        """stdin as input"""
        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return failed(cmndOutcome)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]] Process list of CBSs. arg1 is action for processing. args2 to N are Cbs.
When arg2 is all, list of args is obtained. After args, stdin (or methodInvokeArg) is expected to have a list of Cbs as lines.
This pattern is called listOfArgs subject to Action.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  cbm-materialize-cbs.cs  -i processCbs report /bisos/platform/sys/cbm/facter-cbs-is-p-sysd.cs
#+end_src
#+RESULTS:
:
        #+end_org """)

        cbmDispatch().pyCmnd()

        # Then the verify: read-only, so a fully materialized platform always ends with its report.
        fullyVerify().pyCmnd()

        return cmndOutcome.set(
            opError=b.op.OpError.Success,
            opResults=None,
        )



####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "cbmDispatch" :extent "verify" :comment "stdin as input" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv "methodInvokeArg"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<cbmDispatch>>  *stdin as input*  =verify= ro=cli pyInv=methodInvokeArg   [[elisp:(org-cycle)][| ]]
#+end_org """
class cbmDispatch(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             methodInvokeArg: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:
        """stdin as input"""
        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return failed(cmndOutcome)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]] Process list of CBSs. arg1 is action for processing. args2 to N are Cbs.
When arg2 is all, list of args is obtained. After args, stdin (or methodInvokeArg) is expected to have a list of Cbs as lines.
This pattern is called listOfArgs subject to Action.
        #+end_org """)

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  cbm-materialize-cbs.cs  -i processCbs report /bisos/platform/sys/cbm/facter-cbs-is-p-sysd.cs
#+end_src
#+RESULTS:
:
        #+end_org """)

        # NOTYET  Problem, When it walk down to hereWeb -- it does not respect orderedBranches
        # walkRoot = "/bisos/platform/sys/cbm/collective"

        # Short Term Workaround
        walkRoot = "/bisos/platform/sys/cbm/collective/hereWeb"

        if b.subProc.WOpW(invedBy=self, cd=walkRoot, log=1).bash(
            f"""echo Capability Materialization Started in $(pwd) at $(date)""",
        ).isProblematic(): return(b_io.eh.badOutcome(cmndOutcome))

        if b.subProc.WOpW(invedBy=self, cd=walkRoot, log=1).bash(
            f"""ftoBranchProc.spcs -i fto_forwardToLeaves --cmndName='cbm_status'""",
        ).isProblematic(): return(b_io.eh.badOutcome(cmndOutcome))

        if b.subProc.WOpW(invedBy=self, cd=walkRoot, log=1).bash(
            f"""ftoBranchProc.spcs -i fto_forwardToLeaves --cmndName='cbm_materialize'""",
        ).isProblematic(): return(b_io.eh.badOutcome(cmndOutcome))

        # Then the pals realm: the CBM leaves bisos.pals plants from each PALS-BXO's declarations
        # (palsOfSys.cs -i palsLeavesPlant). After collective/hereWeb, which brings nginx and Node; so
        # platform.internal's snapshot, taken last in hereWeb, shows the pals leaves' previous outcome.
        # ./ftoBranchProc.spcs: this realm's own branch file, not one found on PATH.
        palsRoot = "/bisos/platform/sys/cbm/pals"
        if os.path.isfile(os.path.join(palsRoot, "ftoBranchProc.spcs")):
            for cmndName in ('cbm_status', 'cbm_materialize'):
                if b.subProc.WOpW(invedBy=self, cd=palsRoot, log=1).bash(
                    f"""./ftoBranchProc.spcs -i fto_forwardToLeaves --cmndName='{cmndName}'""",
                ).isProblematic(): return(b_io.eh.badOutcome(cmndOutcome))

        # Then collective/induct: non-service capabilities (lcnt, Emacs from source, Blee, ...), in the
        # order of its ftoBranchProc.spcs. Last: none of the services above needs them. AI-WorkPlan.org 4.7.
        inductRoot = "/bisos/platform/sys/cbm/collective/induct"
        if os.path.isfile(os.path.join(inductRoot, "ftoBranchProc.spcs")):
            for cmndName in ('cbm_status', 'cbm_materialize'):
                if b.subProc.WOpW(invedBy=self, cd=inductRoot, log=1).bash(
                    f"""./ftoBranchProc.spcs -i fto_forwardToLeaves --cmndName='{cmndName}'""",
                ).isProblematic(): return(b_io.eh.badOutcome(cmndOutcome))

        return cmndOutcome.set(
            opError=b.op.OpError.Success,
            opResults=None,
        )


# The walk roots of a full materialization, in cbmDispatch's order, and how each one's branch file
# is reached there: hereWeb by the ftoBranchProc.spcs on PATH, pals and induct by their own.
verifyWalkRoots = [
    ("/bisos/platform/sys/cbm/collective/hereWeb", "ftoBranchProc.spcs"),
    ("/bisos/platform/sys/cbm/pals", "./ftoBranchProc.spcs"),
    ("/bisos/platform/sys/cbm/collective/induct", "./ftoBranchProc.spcs"),
]


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "fullyVerify" :extent "verify" :comment "is this platform healthy?" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 9999 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<fullyVerify>>  *is this platform healthy?*  =verify= argsMax=9999 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class fullyVerify(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 9999,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
    ) -> b.op.Outcome:
        """is this platform healthy?"""
        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]] Is this platform healthy? Read-only. Walks the roots of fullyMaterialize with
cbm_verify (each leaf writes cbmProc.verify), adds the checks no leaf owns (every .internal name
resolves to its address, nginx -t, systemctl --failed), scans the logs given as args (default: the
newest ~/raw-bisos-*-log.org and ~/sysCbmFullyMaterialize-*-log.org), and writes
/bisos/var/cbm/verify/<yymmddHHMMSS>/report.json and report.org (latest -> the newest).
Verdicts come from evidence, never exit codes (bisos-pip/b Stage 4); exit codes are recorded beside
them. The last line is "fullyVerify verify: ok|fail ...".
        #+end_org """)

        runStart = cbmVerify.now()

        # 1. Every leaf verifies itself, in walk order.
        leafDirs: list[pathlib.Path] = []
        for root, branchProc in verifyWalkRoots:
            if not os.path.isfile(os.path.join(root, "ftoBranchProc.spcs")):
                continue
            subprocess.run(f"{branchProc} -i fto_forwardToLeaves --cmndName='cbm_verify'",
                           shell=True, cwd=root, check=False)
            leafDirs += cbmVerify.leavesUnder(pathlib.Path(root))

        # 2. Collect what each leaf wrote in this run. A leaf the walk did not reach is notRun.
        leaves = []
        for plantDir in dict.fromkeys(leafDirs):
            record = cbmVerify.verifyRead(plantDir)
            if record is None or record.get("at", "") < runStart:
                record = {"capabilityName": plantDir.name, "leaf": str(plantDir),
                          "leafRel": str(cbmVerify.cbmProc_seedInfo.leafRel(plantDir)), "at": runStart,
                          "gate": cbmVerify.cbmProc_seedInfo.controlRead(plantDir).value,
                          "lastStatus": "", "materializeRc": None, "checks": [], "rcAgrees": None,
                          "verdict": "notRun", "detail": "the walk did not reach it (no cbmProc.verify of this run)"}
            leaves.append(record)

        # 3. The platform: names, nginx, failed units.
        claimed = {check["target"].split("/")[2] for leaf in leaves for check in leaf["checks"]
                   if check["kind"] == "http"}
        platform = cbmVerify.nameChecks(claimed)
        nginx = cbmVerify.nginxCheck()
        if nginx:
            platform.append(nginx)
        platform += cbmVerify.failedUnitsCheck()

        # 4. The logs.
        logs = [pathlib.Path(os.path.expanduser(a)) for a in (argsList or [])] or cbmVerify.defaultLogs()
        logHits = cbmVerify.logScan(logs)

        rep = cbmVerify.report(leaves, platform, logHits, logs)
        runDir = cbmVerify.reportWrite(rep)

        print(cbmVerify.reportOrg(rep))
        counts = ", ".join(f"{k} {v}" for k, v in sorted(rep["counts"].items()))
        masked = f"; masked: {', '.join(rep['maskedFailures'])}" if rep["maskedFailures"] else ""
        print(f"fullyVerify: leaves {counts}; platform problems {rep['platformProblems']}; "
              f"log hits {len(logHits)}{masked}; report: {runDir}")
        print(f"fullyVerify verify: {rep['verdict']} {counts}")

        return cmndOutcome.set(
            opError=b.op.OpError.Success,
            opResults=str(runDir),
        )


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "verifyCompare" :extent "verify" :comment "what changed between two reports" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 2 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<verifyCompare>>  *what changed between two reports*  =verify= argsMax=2 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class verifyCompare(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 2,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
    ) -> b.op.Outcome:
        """what changed between two reports"""
        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]] Compare two fullyVerify reports (a run directory or its report.json): new
failures, fixed, still failing, changed verdicts and exit codes, platform problems. No args: the two
newest runs under /bisos/var/cbm/verify/. One arg: it against the newest. The comparison of a run
before and one after bisos-pip/b Stage 4 is that stage's test (AI-WorkPlan.org 5.6).
        #+end_org """)

        args = list(argsList or [])
        runs = cbmVerify.reportRuns()
        if len(args) == 2:
            oldPath, newPath = args
        elif len(args) == 1 and runs:
            oldPath, newPath = args[0], runs[-1]
        elif len(runs) >= 2:
            oldPath, newPath = runs[-2], runs[-1]
        else:
            print(f"verifyCompare: need two reports; {cbmVerify.REPORT_BASE} has {len(runs)}")
            return failed(cmndOutcome)
        try:
            old, new = cbmVerify.reportRead(oldPath), cbmVerify.reportRead(newPath)
        except (OSError, ValueError) as e:
            print(f"verifyCompare: cannot read a report: {e}")
            return failed(cmndOutcome)
        changes = cbmVerify.compare(old, new)
        print(cbmVerify.compareText(old, new, changes))
        return cmndOutcome.set(
            opError=b.op.OpError.Success,
            opResults=json.dumps(changes),
        )


####+BEGIN: b:py3:cs:framework/endOfFile :basedOn "classification"
""" #+begin_org
* [[elisp:(org-cycle)][| *End-Of-Editable-Text* |]] :: emacs and org variables and control parameters
#+end_org """

#+STARTUP: showall

### local variables:
### no-byte-compile: t
### end:
####+END:
