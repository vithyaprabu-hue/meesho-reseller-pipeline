\# Agent Specification: Meesho Reseller Growth \& Alert Intelligence Agent



\## 1. Core Agent Components



\- \*\*Goal\*\*: Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every message before it goes out.

\- \*\*Tools\*\*:

&#x20; - `validate\_feed(csv\_path)`: Part 2 data guardrail checking headers, missing values, and numeric ranges.

&#x20; - `mom\_growth(previous, current)`: Part 2 numeric Month-on-Month percentage growth calculation.

&#x20; - `is\_flagged(mom\_pct, threshold=8.0)`: Part 2 3-state growth decision function.

&#x20; - `prompt\_pack\_fill(category, prev\_rev, curr\_rev, mom\_pct, month, prev\_month)`: Part 3 offline deterministic narrative formatter.

\- \*\*Memory / State\*\*: Retains prior month revenue per category across execution runs to compute subsequent MoM deltas without recalculating base tables.

\- \*\*Planner\*\*: Deterministic sequence of 8 subtasks ensuring guardrails run prior to narrative drafting.

\- \*\*Feedback Loop\*\*: Human-in-the-loop checkpoint where every drafted category update is flagged as `drafted\_and\_held\_for\_approval` before delivery.



\## 2. Guardrails



\- \*\*Input Guardrail\*\*: `validate\_feed` must pass with zero errors. If validation fails, execution triggers a Hard Stop immediately without running downstream calculations.

\- \*\*Action Guardrail\*\*: Automated actions are restricted to drafting messages. No outbound delivery (email/chat) is executed automatically.

\- \*\*Output Guardrail\*\*: Every numerical figure in the drafted narrative strictly traces to input feed numbers and exact MoM calculations; zero hallucinated figures.



\## 3. Stopping Conditions



\- \*\*Success Stopping Condition\*\*: Pipeline finishes drafting updates for up to top 3 flagged categories, suppresses excess flagged categories, records exact-boundary cases, and produces a structured JSON output with `action\_taken: "drafted\_and\_held\_for\_approval"`.

\- \*\*Error Stopping Condition\*\*: Input validation fails (`validate\_feed` returns `False`), halting the pipeline immediately with `action\_taken: "hard\_stop"` and listing all validation errors.



\## 4. Agent-Level Given-When-Then Specifications



1\. \*\*Ethnic Wear Spike (May vs April)\*\*:

&#x20;  - \*Given\* April Ethnic Wear revenue of 104520.77 and May revenue of 185107.61.

&#x20;  - \*When\* the agent evaluates the growth engine.

&#x20;  - \*Then\* it computes MoM growth of +77.1%, marks it as `flagged`, drafts a narrative, and holds it for approval.



2\. \*\*Beauty \& Personal Care Stability (June vs May)\*\*:

&#x20;  - \*Given\* May Beauty \& Personal Care revenue of 35542.11 and June revenue of 37559.07.

&#x20;  - \*When\* the agent evaluates the growth engine.

&#x20;  - \*Then\* it computes MoM growth of +5.67%, marks it as `not\_flagged`, and excludes it from both drafts and suppressed lists.



3\. \*\*Synthetic Exact Threshold Boundary\*\*:

&#x20;  - \*Given\* prior revenue of 100000.0 and current revenue of 108000.0.

&#x20;  - \*When\* the agent evaluates the growth engine against the 8.0% threshold.

&#x20;  - \*Then\* it computes MoM growth of exactly 8.0%, classifies it as `escalate\_exact\_boundary`, and appends the category to `escalated\_categories` without drafting an alert.



4\. \*\*Corrupted Feed Feed Guardrail\*\*:

&#x20;  - \*Given\* an input feed with negative revenue, missing category, and blank revenue fields.

&#x20;  - \*When\* the agent executes subtask 1.

&#x20;  - \*Then\* `validate\_feed` returns `False`, execution halts as `hard\_stop`, and exactly 3 structured error messages are logged.

