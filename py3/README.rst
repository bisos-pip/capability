=============================================================================================
bisos.capability: BISOS Capabilities Bundles – Abstraction, Specification and Materialization
=============================================================================================

.. contents::
   :depth: 3
..

Overview
========

bisos.capability is the python package for BISOS **Capability Bundles**.
A BISOS capability is a complete piece of functionality (a systemd
service + its packages + its DNS entry + its nginx vhost, or a
non-service software induction like LaTeX+LCNT) declared once and
materialized in one shot on a target host.

The package covers a three-way triad of abstractions — CBA at the bottom
(the framework, this pip package), CBS in the middle (one ``-cbs.pcs``
executable per capability), CBM at the top (one ``cbmProc.spcs`` planted
per capability leaf). CBM subprocess-invokes CBS at materialization time
and does **not** duplicate CBS content.

Each of the three tiers in detail:

-  **CBA** — Capability Bundle *Abstraction*. The framework layer.
   Provides ``cba_seed.py`` (base CBS singleton), ``cba_sysd_seed.py``
   (flavor extension for systemd services), ``cba_csu.py`` (the
   ``cbs_*`` verb family: ``cbs_load``, ``cbs_sbom``, ``cbs_assemble``,
   ``cbs_materialize``, ``cbs_reMaterialize``, ``cbs_unMaterialize``,
   ``cbs_deMaterialize``, ``cbs_type``, ``cbs_isMaterialized``).

-  **CBS** — Capability Bundle *Specification*. A standalone executable
   ``-cbs.pcs`` file that declares one capability's contents. Uses
   ``cba_seed.setup(seedType``\ …, sbom=…, …)= and (for services)
   ``cba_sysd_seed.setup(sysdUnitsList``\ […])=. Invocable as
   ``./foo-cbs.pcs -i cbs_materialize`` to install / configure / start
   the whole capability. Example:
   ``/bisos/asc/web/bin/airflow-cbs.pcs``.

-  **CBM** — Capability Bundle *Materialization*. A ``cbmProc.spcs``
   planted at a leaf of the CBM tree
   (``sys/cbm/<realm>/<capabilityType>/<capability>/``), gated by a
   sibling ``cbmProc.control`` file. **Points to** a CBS via
   ``cbsSpec``; does NOT duplicate CBS content. When materialized,
   subprocess-invokes the CBS. Provides the ``cbm_*`` verb family:

   -  ``cbm_control`` / ``cbm_status`` / ``cbm_isEnabled`` — read state
   -  ``cbm_enable`` / ``cbm_disable`` / ``cbm_available`` — write state
      (gate manipulation; never gated themselves)
   -  ``cbm_materialize`` / ``cbm_reMaterialize`` /
      ``cbm_unMaterialize`` / ``cbm_sbom`` — gated; subprocess-invoke
      ``<cbsSpec> -i cbs_<verb>``

**Load-bearing principle: CBM sits on top of CBS. It does not duplicate
CBS content.** A ``cbmProc.spcs`` is a ~10-line pointer file
(``capabilityName`` + ``cbsSpec``); the actual CBS content lives in the
referenced ``-cbs.pcs`` executable and stays put.

Files in this package
---------------------

Framework (existing; ship as-is, don't edit):

-  ``cba_seed.py`` — ``CbaSeedInfo`` singleton + ``setup()``
-  ``cba_sysd_seed.py`` — ``SysdUnit``, ``SysdSeedInfo``, sysd flavor
-  ``cba_csu.py`` — ``cbs_*`` verb classes
-  ``cba_sysd_csu.py`` — ``sysdUnitsProc``
-  ``cbm_csu.py`` — ``cbmBase``, ``processCbs``

CBM machinery (additive, non-invasive to the above):

-  ``cbmProc_seedInfo.py`` — ``CbmProcSeedInfo`` singleton,
   ``ControlState`` enum (``available=/=enabled=/=disabled``),
   ``paramsFromPlantPath()``, ``controlRead/Write``,
   ``statusRead/Write``, ``resolveCbsSpec()``, ``leafProcessorNames()``,
   ``walkExamples()``
-  ``cbmProc_seed.py`` — atexit registrar for ``cbmProc-seed.cs``
-  ``cbmProc_csu.py`` — ``cbm_*`` Cmnd classes + ``_dispatchCbs()``
   helper
-  ``bin/cbmProc-seed.cs`` — the CBM-aware seed CSXU

Canonical exemplar
------------------

Airflow at
``/bisos/git/auth/bxRepos/bxObjects/bro_rawBisos/bro_rawBisosPlatform/sys/cbm/collective/hereWeb/airflow/``
— three-file CBM leaf pointing to ``airflow-cbs.pcs``. See
`bro\ rawBisosPlatform/README.org </bisos/git/auth/bxRepos/bxObjects/bro_rawBisos/bro_rawBisosPlatform/README.org>`__
for the realm/capabilityType layering.

Tests
-----

``py3/tests/verify.sh`` — 54-assertion smoke suite covering the
singleton, Cmnd class presence, control/status roundtrips,
paramsFromPlantPath, walkExamples coverage, and ``cbsSpec`` resolution
across absolute-path/slash-path/basename forms.

Package Documentation At Github
===============================

The information below is a subset of the full of documentation for this
bisos-pip package. More complete documentation is available at:
https://github.com/bisos-pip/capability-cs

Realted Resources
=================

+-----------------------------+---------------------------------------+
| bisos Capabilities Panel    | file:/panels/capabili                 |
|                             | ties/_nodeBase_/fullUsagePanel-en.org |
+-----------------------------+---------------------------------------+
|                             |                                       |
+-----------------------------+---------------------------------------+
| CBM airflow exemplar        | /bisos/git/auth/bxRe                  |
|                             | pos/bxObjects/bro\ :sub:`rawBisos`/br |
|                             | o\ :sub:`rawBisosPlatform`/README.org |
+-----------------------------+---------------------------------------+
| Legacy airflow CBS          | /bisos/asc/web/bin/airflow-cbs.pcs    |
+-----------------------------+---------------------------------------+
| FTO walker (planted leaves) | *biso                                 |
|                             | s/git/auth/bxRepos/bisos-pip/fileObj* |
+-----------------------------+---------------------------------------+

.. _table-of-contents:

Table of Contents TOC
=====================

-  `Overview <#overview>`__

   -  `Files in this package <#files-in-this-package>`__
   -  `Canonical exemplar <#canonical-exemplar>`__
   -  `Tests <#tests>`__

-  `Package Documentation At
   Github <#package-documentation-at-github>`__
-  `Realted Resources <#realted-resources>`__
-  `Installation <#installation>`__

   -  `Installation With pip <#installation-with-pip>`__
   -  `Installation With pipx <#installation-with-pipx>`__

-  `Part of BISOS and ByStar — ByStar Internet Services Operating
   System <#part-of-bisos-and-bystar-----bystar-internet-services-operating-system>`__
-  `bisos.capability as a Standalone Piece of
   BISOS <#bisoscapability-as-a-standalone-piece-of-bisos>`__
-  `Documentation and Blee-Panels <#documentation-and-blee-panels>`__

   -  `bisos.capability Blee-Panels <#bisoscapability-blee-panels>`__

-  `Support <#support>`__

Installation
============

The sources for the bisos.capability pip package is maintained at:
https://github.com/bisos-pip/capability.

The bisos.capability pip package is available at PYPI as
https://pypi.org/project/bisos.capability

You can install bisos.capability with pip or pipx.

Installation With pip
---------------------

If you need access to bisos.capability as a python module, you can
install it with pip:

.. code:: bash

   pip install bisos.capability

Installation With pipx
----------------------

If you only need access to bisos.capability as a command on
command-line, you can install it with pipx:

.. code:: bash

   pipx install bisos.capability

The following commands are made available:

-  seedCapability.cs
-  exmpl-capability.cs

Part of BISOS and ByStar — ByStar Internet Services Operating System
====================================================================

| Layered on top of Debian, **BISOS**: (By\* Internet Services Operating
  System) is a unified and universal framework for developing both
  internet services and software-service continuums that use internet
  services. See `Bootstrapping ByStar, BISOS and
  Blee <https://github.com/bxGenesis/start>`__ for information about
  getting started with BISOS.
| **BISOS** is a foundation for **The Libre-Halaal ByStar Digital
  Ecosystem** which is described as a cure for losses of autonomy and
  privacy in a book titled: `Nature of
  Polyexistentials <https://github.com/bxplpc/120033>`__

*bisos.capability* is part of BISOS.

bisos.capability as a Standalone Piece of BISOS
===============================================

bisos.capability is a standalone piece of BISOS. It can be used as a
self-contained Python package separate from BISOS. Follow the
installation and usage instructions below for your own use.

Documentation and Blee-Panels
=============================

bisos.capability is part of ByStar Digital Ecosystem
http://www.by-star.net.

This module's primary documentation is in the form of Blee-Panels.
Additional information is also available in:
http://www.by-star.net/PLPC/180047

bisos.capability Blee-Panels
----------------------------

bisos.capability Blee-Panels are in ./panels directory. From within Blee
and BISOS these panels are accessible under the Blee "Panels" menu.

Support
=======

| For support, criticism, comments and questions; please contact the
  author/maintainer
| `Mohsen Banan <http://mohsen.1.banan.byname.net>`__ at:
  http://mohsen.1.banan.byname.net/contact
