---
schema: "fcvw/skill@1"
name: "release-checklist"
description: "Prepare and validate application or framework releases."
version: "1.1.1"
trigger_keywords:
  - "release"
  - "version bump"
  - "changelog"
  - "publish"
  - "publicar versão"
session_types:
  - "release"
---

# Release checklist

## Purpose

Prepare and validate an application or FCVW framework release while keeping version namespaces, migration, rollback, evidence, and publication authority coherent.

## Use conditions

Use for version selection, release-record assembly, tag/release preparation, or publication closeout. Read-only version questions do not authorize a release mutation.

## First decision

Classify the release:

- **Application:** use `changelogs/` and the application's version source.
- **Framework:** use `framework-releases/`, `FRAMEWORK_LOCK.md`, `OWNERSHIP.md`, and `MIGRATIONS.md`.

Never mix the namespaces.

## Inputs

Completed plans, unreleased fragments, target version, test evidence, deployment/rollback information, and publication authority.

## Procedure

1. Select included plans and confirm states.
2. Decide semantic bump and compatibility.
3. Assemble the appropriate release record from its template.
4. Check version source and related links.
5. Run application tests and governance validation appropriate to risk.
6. Confirm migration, backup, deployment, and rollback where applicable.
7. Publish only after target validation and explicit authority.
8. Record external tag/release evidence separately.

## Framework-specific checks

- role manifest/ownership is current;
- clean artifact excludes project records and comparison fixtures;
- schema changes have migrations;
- clean-template validator passes;
- downstream preservation paths are documented;
- artifact checksum is recorded.

## Non-responsibilities

- inferring permission to push, tag, deploy, or publish;
- claiming external publication without evidence;
- bumping the application version for a governance-only framework update by default.

## Required output

Release type, version, included plans, validation, migration/rollback, publication state, and residual gaps.

## Validation and exit

The record is internally coherent, blocking gates pass, and `published` is used only after actual publication.
