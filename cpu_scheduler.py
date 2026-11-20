"""
CPU Scheduling Simulator - PT 101 Final Project (Topic 2)
Algorithms: FCFS, non-preemptive SJF, preemptive SRTF, Round Robin (RR)

Run GUI :  python cpu_scheduler.py          (modern interface, opens in your browser)
Run Tk  :  python cpu_scheduler.py --tk     (simple tkinter window)
Run CLI :  python cpu_scheduler.py --cli    (console menu)

Formulas:
    TAT = CT - AT
    WT  = TAT - BT
    RT  = first start time - AT
"""
import sys
from dataclasses import dataclass, field


# ----------------------------------------------------------------------
# DATA MODEL
# ----------------------------------------------------------------------
@dataclass
class Process:
    pid: str
    at: int
    bt: int
    ct: int = 0
    tat: int = 0
    wt: int = 0
    rt: int = -1          # -1 = not started yet


@dataclass
class Result:
    name: str
    processes: list
    timeline: list                      # [(pid or "Idle", start, end)]
    rr_trace: list = field(default_factory=list)
    quantum: int = 0

    @property
    def avg_tat(self):
        return sum(p.tat for p in self.processes) / len(self.processes)

    @property
    def avg_wt(self):
        return sum(p.wt for p in self.processes) / len(self.processes)

    @property
    def avg_rt(self):
        return sum(p.rt for p in self.processes) / len(self.processes)


def validate(procs, quantum=None):
    """Validate user input. Raises ValueError with a readable message."""
    if not procs:
        raise ValueError("Enter at least one process.")
    seen = set()
    for p in procs:
        if not p.pid.strip():
            raise ValueError("Process ID cannot be empty.")
        if p.pid in seen:
            raise ValueError(f"Duplicate process ID: {p.pid}")
        seen.add(p.pid)
        if p.at < 0:
            raise ValueError(f"{p.pid}: arrival time cannot be negative.")
        if p.bt <= 0:
            raise ValueError(f"{p.pid}: burst time must be greater than 0.")
    if quantum is not None and quantum <= 0:
        raise ValueError("Time quantum must be greater than 0.")


def clone(procs):
    return [Process(p.pid, p.at, p.bt) for p in procs]


def finalize(procs):
    for p in procs:
        p.tat = p.ct - p.at
        p.wt = p.tat - p.bt


def merge(timeline):
    """Merge adjacent segments that belong to the same process."""
    out = []
    for pid, s, e in timeline:
        if out and out[-1][0] == pid and out[-1][2] == s:
            out[-1] = (pid, out[-1][1], e)
        else:
            out.append((pid, s, e))
    return out


# ----------------------------------------------------------------------
# ALGORITHMS
# ----------------------------------------------------------------------
def fcfs(src):
    procs = clone(src)
    order = sorted(procs, key=lambda p: (p.at, src_index(src, p)))
    t, tl = 0, []
    for p in order:
        if t < p.at:
            tl.append(("Idle", t, p.at))
            t = p.at
        p.rt = t - p.at
        tl.append((p.pid, t, t + p.bt))
        t += p.bt
        p.ct = t
    finalize(procs)
    return Result("FCFS", procs, merge(tl))


def sjf(src):
    """Non-preemptive Shortest Job First. Tie: earlier arrival, then input order."""
    procs = clone(src)
    done, t, tl = set(), 0, []
    while len(done) < len(procs):
        ready = [p for p in procs if p.pid not in done and p.at <= t]
        if not ready:
            nxt = min(p.at for p in procs if p.pid not in done)
            tl.append(("Idle", t, nxt))
            t = nxt
            continue
        p = min(ready, key=lambda x: (x.bt, x.at, src_index(src, x)))
        p.rt = t - p.at
        tl.append((p.pid, t, t + p.bt))
        t += p.bt
        p.ct = t
        done.add(p.pid)
    finalize(procs)
    return Result("SJF (Non-Preemptive)", procs, merge(tl))


def srtf(src):
    """Preemptive SJF. Tie: earlier arrival, then input order."""
    procs = clone(src)
    remaining = {p.pid: p.bt for p in procs}
    t, finished, tl = 0, 0, []
    while finished < len(procs):
        ready = [p for p in procs if remaining[p.pid] > 0 and p.at <= t]
        if not ready:
            nxt = min(p.at for p in procs if remaining[p.pid] > 0)
            tl.append(("Idle", t, nxt))
            t = nxt
            continue
        p = min(ready, key=lambda x: (remaining[x.pid], x.at, src_index(src, x)))
        if p.rt == -1:
            p.rt = t - p.at
        tl.append((p.pid, t, t + 1))
        remaining[p.pid] -= 1
        t += 1
        if remaining[p.pid] == 0:
            p.ct = t
            finished += 1
    finalize(procs)
    return Result("SRTF (Preemptive SJF)", procs, merge(tl))
