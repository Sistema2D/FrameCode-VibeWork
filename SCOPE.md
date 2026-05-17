# SCOPE.md

General scope of the application according to the current state of the project.

This document describes the purpose, boundaries, modules, screens, and main contents of the application. It does not replace `README.md`, `STACK.md`, `DESIGN.md`, or `PLANNING.md`; its role is to consolidate the functional scope view to guide future analysis, planning, and evolution.

> This is a template. Replace the fields between `<...>` with the actual information of the project.

## Overview

`<Describe in two or three sentences what the application is, its main stack, and its execution context.>`

## General Objective

`<Describe the main objective of the application in one or two sentences.>`

## Specific Objectives

- `<objective 1>`
- `<objective 2>`
- `<objective 3>`

## Limits of Current Scope

- `<limit 1>`
- `<limit 2>`
- `<limit 3>`

## High-Level Architecture

### Frontend

`<Describe the technology, main responsibilities, and relevant files. Remove if not applicable.>`

### Backend

`<Describe the framework, local port, main endpoints, and relevant modules. Remove if not applicable.>`

### Local or Remote AI

`<Describe the runtime, the AI's roles in the application, and usage limits. Remove if not applicable.>`

### Vault / Knowledge Base

`<Describe the location, format, and structure. Remove if not applicable.>`

## Modules and Screens

### `<Module or screen name 1>`

Objective: `<objective>`

Content and features:

- `<item 1>`
- `<item 2>`

### Public API and Exported Contracts

`<Remove when not a library or SDK.>`

`<Describe the contracts that external consumers see: exported functions, public endpoints, events, schemas, or interfaces. Changes here require a major version increment.>`

### `<Module or screen name 2>`

Objective: `<objective>`

Content and features:

- `<item 1>`
- `<item 2>`

## Cross-Cutting Components

### Navigation

`<Describe how the user navigates between screens or modules.>`

### Local Persistence

`<Describe what data is persisted, where, and in what format.>`

### Local Security

`<Describe authentication controls, local token, CORS, and path validation.>`

### Build and Execution

`<Describe how to build and execute the application.>`

### Document Governance

The application maintains a versioned document layer to guide planning, implementation, validation, release, and continuous learning of the project itself.

Main components:

- official documents at the root of the repository;
- plans in `Plans/{status}`;
- changelogs in `changelogs/`;
- issue records in `troubleshooting/`;
- governance wiki in `wiki/`;
- reusable empty templates in `governance/`.

## Related Documents

- `README.md`: overview, requirements, build, execution, and troubleshooting.
- `STACK.md`: technical stack and architecture.
- `DESIGN.md`: visual and experience rules.
- `PLANNING.md`: mandatory methodology for changes.
- `AGENTS.md`: operational guide for humans and agents.
- `TROUBLESHOOTING.md`: failure registration and handling process.
- `VERSIONING.md`: version, release, and changelog rules.
- `MANIFEST.md`: identity and governance synthesis of the project.
