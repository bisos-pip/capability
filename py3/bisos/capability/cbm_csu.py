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
from bisos.capability import cba_seed

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
        sectionTitle: typing.AnyStr = "",
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ] Examples of Service Access Instance Commands.
    #+end_org """

    od = collections.OrderedDict
    cmnd = cs.examples.cmndEnter
    # literal = cs.examples.execInsert

    if sectionTitle == 'default':
        cs.examples.menuChapter('*CBM  Bases -- Update, Obtain, List*')

    cs.examples.menuSection(f'=Capability Base Materialization Base=')

    cmnd('cbmBase', args="mkdir")
    cmnd('cbmBase', args="obtain")
    cmnd('cbmBase', args="list")

    cs.examples.menuChapter(f'=Process CBSs=')

    listOfCbs = cbmBase().pyCmnd(argsList=["list"]).results


    for eachCbs in listOfCbs:

        if (outcome := b.subProc.WOpW(invedBy=None, log=0).bash(
                f"""{eachCbs}  -i cbs_type""",
        )).isProblematic(): continue
        cbsSeedType = outcome.stdout.strip()

        cs.examples.menuSection(f'=Process CBS {eachCbs}=')
        cmnd('processCbs', args=f"type {eachCbs}", comment=f" # {cbsSeedType}")
        cmnd('processCbs', args=f"report {eachCbs}", comment=f"")
        cmnd('processCbs', args=f"report", wrapper=f"echo {eachCbs}",  comment=f"")
        cmnd('processCbs', args=f"load {eachCbs}", comment=f"")
        cmnd('processCbs', args=f"sbom {eachCbs}", comment=f"")
        cmnd('processCbs', args=f"assemble {eachCbs}", comment=f"")
        if cbsSeedType == "systemd":
            cmnd('processCbs', args=f"sysdEnsure {eachCbs}", comment=f"")
        cmnd('processCbs', args=f"materialize {eachCbs}", comment=f"")

    if len(listOfCbs) != 0:
        listOfCbsStr = [ str(i) for i in listOfCbs ]
        joinedListOfCbs = " ".join(listOfCbsStr)
        cs.examples.menuSection(f'=Process All CBS=')
        cmnd('processCbs', args=f"report", wrapper=f"echo {joinedListOfCbs} |",  comment=f"")
        cmnd('processCbs', args=f"report all", comment=f"")
        cmnd('processCbs', args=f"materialize", wrapper=f"echo {joinedListOfCbs} |",  comment=f"")
        cmnd('processCbs', args=f"materialize all", comment=f"")


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "CmndSvcs" :anchor ""  :extraInfo "Command Services Section"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _CmndSvcs_: |]]  Command Services Section  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "cbmBase" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<cbmBase>>  =verify= argsMin=1 argsMax=1 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class cbmBase(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        if self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  With bpoId update or obtain /bisos/var/platform/bpo and /bisos/platform.
        #+end_org """): return(cmndOutcome)

        action = self.cmndArgsGet("0&1", cmndArgsSpecDict, argsList)[0]

        platformBaseDir = platformBases.platformBasePath()

        # outcome = platformBases_csu.platformBase().pyCmnd(argsList=["obtain"])
        # platformBaseDir = outcome.results

        # /bisos/platform/sys/cbm
        cbmBaseDir = platformBaseDir.joinpath("sys/cbm")

        if action == "mkdir":
            cbmBaseDir.mkdir(parents=True, exist_ok=True)
            return cmndOutcome.set(opResults=cbmBaseDir)

        elif action == "obtain":
            return cmndOutcome.set(opResults=cbmBaseDir)

        elif action == "list":
            p = cbmBaseDir.glob('**/*')
            filesList = [x for x in p if x.is_file()]
            return cmndOutcome.set(opResults=filesList)

        else:
            return failed(cmndOutcome)


####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&1",
            argName="action",
            argDefault='',
            argChoices=['mkdir', 'obtain', 'list'],
            argDescription="One argument, as action"
        )
        return cmndArgsSpecDict



####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "processCbs" :extent "verify" :comment "stdin as input" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv "methodInvokeArg"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<processCbs>>  *stdin as input*  =verify= argsMin=1 argsMax=9999 ro=cli pyInv=methodInvokeArg   [[elisp:(org-cycle)][| ]]
#+end_org """
class processCbs(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 9999,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
             methodInvokeArg: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:
        """stdin as input"""
        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
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

        self.captureRunStr(""" #+begin_org
#+begin_src sh :results output :session shared
  echo  /bisos/platform/sys/cbm/facter-cbs-is-p-sysd.cs | cbm-materialize-cbs.cs  -i processCbs report
#+end_src
#+RESULTS:
:
        #+end_org """)


        if self.justCaptureP(): return cmndOutcome

        action = self.cmndArgsGet("0", cmndArgsSpecDict, argsList)
        listOfCbs = self.cmndArgsGet("1&9999", cmndArgsSpecDict, argsList)

        if listOfCbs:
            if listOfCbs[0] == "all":
                listOfCbs = cbmBase().pyCmnd(argsList=["list"]).results

        # methodInvokeArg is expected to be a string of lines.1
        if not methodInvokeArg:
            methodInvokeArg = b_io.stdin.read()

        processedCount = 0

        b.comment.orgMode(""" #+begin_org
*****  [[elisp:(org-cycle)][| *Note:* | ]] Process Each based on actions
        #+end_org """)

        def runCbs(cbs, action):
            if b.subProc.WOpW(invedBy=self, log=1).bash(
                    f"""{cbs}  -i cbs_{action}""",
            ).isProblematic(): return(b_io.eh.badOutcome(cmndOutcome))

        def runCbsSysdEnsure(cbs, action):
            if b.subProc.WOpW(invedBy=self, log=1).bash(
                    f"""{cbs}  -i sysdUnitsProc ensure all""",
            ).isProblematic(): return(b_io.eh.badOutcome(cmndOutcome))


        def processEach(eachCbs):
            nonlocal processedCount
            processedCount += 1
            
            if action == "report":
                print(f"{action} -- {eachCbs}")

            elif action == "load":
                runCbs(eachCbs, action)

            elif action == "sbom":
                runCbs(eachCbs, action)

            elif action == "assemble":
                runCbs(eachCbs, action)

            elif action == "sysdEnsure":
                runCbsSysdEnsure(eachCbs, action)

            elif action == "materialize":
                runCbs(eachCbs, action)
                
            else:
                return failed(cmndOutcome)

        for eachCbs in listOfCbs:
            processEach(eachCbs)

        for eachCbs in methodInvokeArg.splitlines():
            processEach(eachCbs)

        return cmndOutcome.set(
            opError=b.op.OpError.Success,
            opResults=processedCount,
        )

####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """  #+begin_org
*** [[elisp:(org-cycle)][| *cmndArgsSpec:* | ]] First arg defines rest
        #+end_org """

        cmndArgsSpecDict = cs.arg.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0",
            argName="action",
            argChoices=['report', 'load', 'sbom', 'assemble', 'materialize'],
            argDescription="Action to be specified by rest"
        )
        cmndArgsSpecDict.argsDictAdd(
            argPosition="1&9999",
            argName="actionArgs",
            argChoices=['all', ''],
            argDescription="Rest of args for use by action"
        )

        return cmndArgsSpecDict


####+BEGIN: bx:icm:py3:section :title "CS-Commands --- Full Update"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *CS-Commands --- Apt Packages*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:


####+BEGIN: b:py3:cs:framework/endOfFile :basedOn "classification"
""" #+begin_org
* [[elisp:(org-cycle)][| *End-Of-Editable-Text* |]] :: emacs and org variables and control parameters
#+end_org """

#+STARTUP: showall

### local variables:
### no-byte-compile: t
### end:
####+END:
