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

import subprocess
# import time

# import os
# import sys

from pathlib import Path
from bisos.bpo import bpo
from bisos.platform import platformBases_csu
from bisos.platform import platformBases
from bisos.basics import pathPlus


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

    cs.examples.menuSection("*Full Dispatch  Cap Specification and Full Cap Materialization*")

    cmnd('fullCapSpecAndMatDispatch')

    cs.examples.menuSection("*SysChar Deploy Cap Specification -- Based on Platform's Abode and Purpose*")

    cmnd('fullCapSpecDispatch')

    cs.examples.menuSection("*Cap Materialization -- Based on sys/bin sys/cap sys/pbs*")

    cmnd('fullCapMatDispatch')
    cmnd('preBinDispatch')
    cmnd('cbmDispatch')
    cmnd('pbsDispatch')
    cmnd('postBinDispatch')

""" #+begin_org
*  ---- Devider ----
#+end_org """



####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "CmndSvcs" :anchor ""  :extraInfo "Full Capability Specifications and Materialization Dispatch"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _CmndSvcs_: |]]  Full Capability Specifications and Materialization Dispatch  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "fullCapSpecAndMatDispatch" :extent "verify" :comment "stdin as input" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv "methodInvokeArg"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<fullCapSpecAndMatDispatch>>  *stdin as input*  =verify= ro=cli pyInv=methodInvokeArg   [[elisp:(org-cycle)][| ]]
#+end_org """
class fullCapSpecAndMatDispatch(cs.Cmnd):
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

        fullCapSpecDispatch().pyCmnd()
        fullCapMatDispatch().pyCmnd()

        return cmndOutcome.set(
            opError=b.op.OpError.Success,
            opResults=None,
        )


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "CmndSvcs" :anchor ""  :extraInfo "SysChar Deploy Cap Specification"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _CmndSvcs_: |]]  SysChar Deploy Cap Specification  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:


def whichOrDefaultBinPathNOT (
        progName: str,
        defaultPath: Path,
) -> Path | None:
    """ """

    result: Path | None = None

    cmndOutcome = b.subProc.WOpW(invedBy=None, log=0).bash(
        f"""set -o pipefail; which -a {progName} | grep -v '\./{progName}' | head -1""",
    )
    if cmndOutcome.isProblematic():
        if defaultPath.exists():
            result = defaultPath
        else:
            result = None
    else:
         result = Path(cmndOutcome.stdout.strip())

    return result


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "fullCapSpecDispatch" :extent "verify" :comment "stdin as input" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv "methodInvokeArg"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<fullCapSpecDispatch>>  *stdin as input*  =verify= ro=cli pyInv=methodInvokeArg   [[elisp:(org-cycle)][| ]]
#+end_org """
class fullCapSpecDispatch(cs.Cmnd):
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
  materializationDispatch.cs  -i fullCapSpecDispatch
#+end_src
#+RESULTS:
:
        #+end_org """)

        if ( execPath := pathPlus.whichOrDefaultBinPath(
            "facter-cbs-is-p-sysd.cs",
            Path("/bisos/venv/py3/bisos3/bin/facter-cbs-is-p-sysd.cs")
        )) is None:
            return(b_io.eh.badOutcome(cmndOutcome))

        if b.subProc.WOpW(invedBy=self, log=1).bash(
            f"""{execPath}  -i cbmSymlinkToThisCbs enable""",
        ).isProblematic(): return(b_io.eh.badOutcome(cmndOutcome))

        return cmndOutcome.set(
            opError=b.op.OpError.Success,
            opResults=None,
        )


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "CmndSvcs" :anchor ""  :extraInfo "Capability Materialization - Based on sys/bin,cap,pbs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _CmndSvcs_: |]]  Capability Materialization - Based on sys/bin,cap,pbs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "fullCapMatDispatch" :extent "verify" :comment "stdin as input" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv "methodInvokeArg"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<fullCapMatDispatch>>  *stdin as input*  =verify= ro=cli pyInv=methodInvokeArg   [[elisp:(org-cycle)][| ]]
#+end_org """
class fullCapMatDispatch(cs.Cmnd):
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

        preBinDispatch().pyCmnd()
        cbmDispatch().pyCmnd()
        pbsDispatch().pyCmnd()
        postBinDispatch().pyCmnd()

        return cmndOutcome.set(
            opError=b.op.OpError.Success,
            opResults=None,
        )


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "preBinDispatch" :extent "verify" :comment "stdin as input" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv "methodInvokeArg"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<preBinDispatch>>  *stdin as input*  =verify= ro=cli pyInv=methodInvokeArg   [[elisp:(org-cycle)][| ]]
#+end_org """
class preBinDispatch(cs.Cmnd):
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

        platformBaseDir = platformBases.platformBasePath()
        # /bisos/platform/sys/bin
        platformSysBin  = platformBaseDir.joinpath("sys/bin")

        platformSysBinPreDispatch  = platformSysBin.joinpath("preDispatch.sh")

        if platformSysBinPreDispatch.is_file():
            if b.subProc.WOpW(invedBy=self, log=1).bash(
                    f"""{platformSysBinPreDispatch} -i fullUpdate""",
            ).isProblematic(): return(b_io.eh.badOutcome(cmndOutcome))
        else:
            print(f"Skipped: Missing {platformSysBinPreDispatch}")
            # b_io.warning(f"Skipped: Missing {platformSysBinPreDispatch}")

        return cmndOutcome.set(
            opError=b.op.OpError.Success,
            opResults=None,
        )


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "postBinDispatch" :extent "verify" :comment "stdin as input" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv "methodInvokeArg"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<postBinDispatch>>  *stdin as input*  =verify= ro=cli pyInv=methodInvokeArg   [[elisp:(org-cycle)][| ]]
#+end_org """
class postBinDispatch(cs.Cmnd):
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

        platformBaseDir = platformBases.platformBasePath()
        # /bisos/platform/sys/bin
        platformSysBin  = platformBaseDir.joinpath("sys/bin")

        platformSysBinPostDispatch = platformSysBin.joinpath("postDispatch.sh")

        if platformSysBinPostDispatch.is_file():
            if b.subProc.WOpW(invedBy=self, log=1).bash(
                    f"""{platformSysBinPostDispatch} -i fullUpdate""",
            ).isProblematic(): return(b_io.eh.badOutcome(cmndOutcome))
        else:
            print(f"Skipped: Missing {platformSysBinPostDispatch}")
            # b_io.warning(f"Skipped: Missing {platformSysBinPostDispatch}")

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

        if b.subProc.WOpW(invedBy=self, log=1).bash(
            f"""/bisos/venv/py3/bisos3/bin/cbm-materialize-cbs.cs -i processCbs materialize all""",
        ).isProblematic(): return(b_io.eh.badOutcome(cmndOutcome))

        return cmndOutcome.set(
            opError=b.op.OpError.Success,
            opResults=None,
        )


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "pbsDispatch" :extent "verify" :comment "stdin as input" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv "methodInvokeArg"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<pbsDispatch>>  *stdin as input*  =verify= ro=cli pyInv=methodInvokeArg   [[elisp:(org-cycle)][| ]]
#+end_org """
class pbsDispatch(cs.Cmnd):
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

        binsMaterializeCmnd="echo pbsDispatch NOTYET -- Place holder for now."

        if b.subProc.WOpW(invedBy=self, log=1).bash(
            f"""{binsMaterializeCmnd}""",
        ).isProblematic(): return(b_io.eh.badOutcome(cmndOutcome))

        return cmndOutcome.set(
            opError=b.op.OpError.Success,
            opResults=None,
        )


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "preBinDipatch" :extent "verify" :comment "stdin as input" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv "methodInvokeArg"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<preBinDipatch>>  *stdin as input*  =verify= ro=cli pyInv=methodInvokeArg   [[elisp:(org-cycle)][| ]]
#+end_org """
class preBinDipatch(cs.Cmnd):
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

        binsMaterializeCmnd="echo NOTYET"

        if b.subProc.WOpW(invedBy=self, log=1).bash(
            f"""{binsMaterializeCmnd}""",
        ).isProblematic(): return(b_io.eh.badOutcome(cmndOutcome))

        return cmndOutcome.set(
            opError=b.op.OpError.Success,
            opResults=None,
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
