# Team Assignments and Commit Plan

Roles are from `team-assignments.png`.

| Member | Role | Owns |
|---|---|---|
| Ezekiel Lazaro | Project Manager / Fullstack | Repo setup, README, tests, CLI, tkinter window, merging |
| Mark Aldred Magtibay | Backend | Data model, validation, FCFS, SJF, SRTF (`cpu_scheduler.py`) |
| Red Sepillo | Backend | Round Robin, run_all, `simulate()`, HTTP server (`web_ui.py`) |
| Stephen Andre Glovo | Frontend | HTML layout and CSS in `web_ui.py` |
| Hannah Catapang | Frontend | JavaScript, Gantt chart and results display in `web_ui.py` |

## Suggested commits

### Ezekiel Lazaro
- `chore: initialize repository, .gitignore and VS Code launch config`
- `docs: add README with run instructions and output interpretation`
- `test: add test_cpu_scheduler.py`
- `feat: add CLI menu and tkinter window`
- `chore: merge branches and fix integration issues`

### Mark Aldred Magtibay
- `feat: add Process and Result dataclasses with avg TAT/WT/RT`
- `feat: add input validation (validate, clone, finalize, merge)`
- `feat: implement FCFS and non-preemptive SJF`
- `feat: implement SRTF with idle-gap handling`

### Red Sepillo
- `feat: implement Round Robin with quantum and tie rule`
- `feat: add run_all for algorithm comparison`
- `feat: add simulate() and JSON result conversion`
- `feat: add HTTP Handler and serve() on port 8765`

### Stephen Andre Glovo
- `feat: add page layout, input form and process table`
- `style: add theme, colors and responsive CSS`
- `feat: add algorithm selection and time quantum controls`

### Hannah Catapang
- `feat: add add/delete/clear row and load-sample buttons`
- `feat: send form data to backend and handle errors`
- `feat: render Gantt chart including Idle blocks`
- `feat: render results table and algorithm comparison`

## Workflow
1. One branch per person (`feature/backend-rr`, `feature/frontend-gantt`, ...).
2. `git pull` before every push.
3. Open a pull request into `main`; Ezekiel merges.
4. Run `python -m unittest -v test_cpu_scheduler` before pushing backend changes.
