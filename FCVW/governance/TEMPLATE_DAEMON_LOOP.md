# Template: Declarative Daemon Loop

## Loop Name

<name>

## Purpose

<why this loop exists>

## Entry Conditions

- 

## Iteration Steps

1. 
2. 
3. 

## Stop Conditions

- 

## Maximum Scope per Iteration

<one plan, one document group, one validation class, etc.>

## Evidence

- 

## Forbidden Behavior

- no background execution;
- no script execution;
- no file modification without plan;
- no destructive action without approval;
- no reading outside allowed paths;
- no package installation;
- no Git hook installation;
- no CI/CD workflow creation.

## Scenario 1 Compliance

- [ ] This loop is a Markdown-only operating procedure.
- [ ] This loop does not run as a service, watcher, scheduled task, or daemon process.
