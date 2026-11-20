# CPU Scheduling Simulator (PT 101 - Topic 2)
FCFS, SJF (non-preemptive), SRTF (preemptive), Round Robin. Python 3.9+, no extra installs.

## Run in VS Code
1. File > Open Folder... > this folder. Install the **Python** extension.
2. Press **F5** and pick *Run GUI*, *Run CLI* or *Run Tests*
   (or in the terminal: `python cpu_scheduler.py`, `python cpu_scheduler.py --cli`,
   `python -m unittest -v test_cpu_scheduler`).
3. *Run GUI* starts the simulator and opens it in your browser (http://127.0.0.1:8765).
   Press Ctrl+C in the terminal to stop it.
4. Optional simple tkinter window: `python cpu_scheduler.py --tk`.

## Inputs
Process ID, Arrival Time (>= 0), Burst Time (> 0), Time Quantum (> 0, RR / Compare All).

## Output interpretation
Gantt chart (Idle = CPU gap), per-process AT, BT, CT, TAT = CT-AT, WT = TAT-BT,
RT = first start-AT, averages, RR slice trace, and an algorithm comparison.
RR tie rule: a preempted process is queued before a process arriving at the same instant.
