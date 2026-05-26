# Template: AI Feature Specification

Copy this content to a new file or inside a plan when defining a new AI feature.

```markdown
# AI Feature: <Name>

## Objective

- <Describe the practical goal of the feature.>

## Usage Type

`simple chat` / `chat with context` / `RAG` / `continuous learning` / `agent with tools`

## Inputs

- <Describe what the user sends or what is captured from the system.>

## Outputs

- <Describe the expected format of the response (text, JSON, action).>

## Model/Runtime

- <e.g., gpt-4o, claude-3.5-sonnet, ollama/llama3.>

## Context Used

- <Which files, history, or databases are sent to the model.>

## Sources Displayed

- <How the user will know the origin of the information.>

## Action Boundaries

- <What the feature CANNOT do (e.g., delete without confirmation).>

## Risks

- <Hallucination, cost, latency, context leakage.>

## Minimum Tests

- <Mandatory test cases for this feature.>
```
