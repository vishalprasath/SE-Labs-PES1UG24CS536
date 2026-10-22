# SE-Labs-PES1UG24CS536

Name: Vishal Prasath
SRN: PES1UG24CS536

## Lab-1: Requirements Engineering & UML Use-Case Modelling

### Problem Statement
**#44 – Database Query Performance Profiler**

A database observability tool that ingests slow query logs, parses SQL execution plans, identifies missing index candidates, and generates weekly performance optimization digests.

### Contents

#### submissions/
- `Complete_Requirements_Table.pdf` – 5 Functional Requirements + 2 Non-Functional Requirements
- `UML_Use-Case_Diagram.pdf` – Use-case diagram with actors and relationships
- `Use-Case_Flow_Specification.pdf` – Use-case flow for UC-04 (Generate Weekly Digest)

#### problem_statement/
- `44_SE_Lab1_SE_Problem_Statements.pdf` – original problem statement

## Lab-2: Agile Backlog Creation & Sprint Simulation in Jira

### Contents

#### submissions/
- `Lab2_JIRA_PES1UG24CS536.pdf` – Contains Epics, User Stories with Fibonacci estimations, and Jira screenshots for Backlog, Sprint 1, Sprint 2 boards and Burndown charts.

#### problem_statement/
- `lab2_handout.pdf` – Lab instructions and requirements.

## Lab-3: Architecture Pattern Selection & UML Component Diagram

### Contents
- `Lab3_Component_Diagram.pdf` – UML Component Diagram illustrating the Microservices architecture for Problem Statement #44 (Database Query Performance Profiler).
- `Lab3_Architecture_Justification.pdf` / `Lab3_Architecture_Justification.docx` – Architectural justification document explaining the selection of Microservices pattern over Layered and Client-Server styles to satisfy high-volume log ingestion and independent scaling NFRs.

## Lab-4: Pair Programming with LLMs – Real-Time Simple Platformer Game

### Contents
- `main.py` & `game/` – Pygame implementation with swept vertical collision detection, game over overlay screen, difficulty replay options (Easy/Medium/Hard), and procedural sound effects.
- `before.mov` – Gameplay recording before bug fixes showcasing collision tunneling.
- `after.mov` – Gameplay recording after fixes demonstrating all 4 tasks and new features.
- `llm_chat_link/LLM_Chat_Link.md` – Link to complete Claude pair-programming conversation history.
- `README.md` – Detailed instructions, setup, and task breakdown for the platformer game.


## Lab-5: Static Code Analysis with Pylint, Bandit & Flake8

### Problem Statement
**#44 – Employee Payroll System**

An employee salary and payroll manager that logs bonuses, deducts penalties, checks eligibility thresholds, computes net salaries, and exports payroll summaries.

### Contents
- `employee_payroll_system.py` – Cleaned version of the script with all Bandit, Pylint, and Flake8 issues fixed.
- `issues.md` – Table of identified issues (type, lines, description, fix approach), prioritised by severity.
- `reports/before/` – Pylint, Bandit, and Flake8 reports on the original code.
- `reports/after/` – Reports after fixes (Pylint 10.00/10, 0 Bandit issues, 0 Flake8 issues).
- `README.md` – Original lab instructions for the assigned repo.
