\# Meesho Reseller Growth \& Alert Intelligence Pipeline



An end-to-end automated monitoring pipeline designed for Meesho's reseller-operations team to monitor monthly revenue shifts, apply strict numerical guardrails, mask sensitive merchant data, and draft deterministic AI alerts.



\## Project Structure \& Workflow Patterns

\- \*\*Part 1 -> Part 2 (`SQL to Python Engine`)\*\*: Mirrors the "compute ground truth numbers via SQL first, then hand off" pattern.

\- \*\*Part 2 -> Part 3 (`Guardrail to Narrative`)\*\*: Implements strict data validation, MoM percentage change detection, and deterministic template narrative generation without hallucinations.

\- \*\*Part 4 (`Agentic Workflow`)\*\*: Ties all components together into an intake -> validation -> planning -> draft -> hold-for-approval reporting cycle.



\## Zero API Keys Requirement

This repository requires \*\*zero API keys\*\*, external subscriptions, or third-party cloud services. All narrative generation runs offline using deterministic template filling.



\## How to Run the Pipeline (Step-by-Step)



\### 1. Regenerate Dataset (Part 1)

```bash

python data/generate\_dataset.py

