"""Test cases (expected vs actual) for the CPU Scheduling Simulator."""
import unittest
from cpu_scheduler import Process, fcfs, sjf, srtf, round_robin


def procs(*rows):
    return [Process(a, b, c) for a, b, c in rows]


def ct(r):
    return [p.ct for p in r.processes]


class TestScheduler(unittest.TestCase):
    def test1_round_robin_guideline_sample(self):
        r = round_robin(procs(("P1", 0, 7), ("P2", 1, 4), ("P3", 2, 3), ("P4", 3, 5)), 3)
        self.assertEqual(ct(r), [17, 16, 9, 19])
        self.assertEqual([p.wt for p in r.processes], [10, 11, 4, 11])
        self.assertEqual([p.rt for p in r.processes], [0, 2, 4, 9])
        self.assertEqual([t[0] for t in r.timeline],
                         ["P1", "P2", "P3", "P1", "P4", "P2", "P1", "P4"])

    def test2_fcfs_convoy_effect(self):
        r = fcfs(procs(("P1", 0, 24), ("P2", 0, 3), ("P3", 0, 3)))
        self.assertEqual(ct(r), [24, 27, 30])
        self.assertAlmostEqual(r.avg_wt, 17.0)
        self.assertAlmostEqual(r.avg_tat, 27.0)

    def test3_sjf_and_srtf(self):
        s = procs(("P1", 0, 7), ("P2", 1, 4), ("P3", 2, 3), ("P4", 3, 5))
        self.assertEqual(ct(sjf(s)), [7, 14, 10, 19])
        self.assertAlmostEqual(sjf(s).avg_wt, 6.25)
        self.assertEqual(ct(srtf(s)), [19, 5, 8, 13])
        self.assertAlmostEqual(srtf(s).avg_wt, 5.0)

    def test4_idle_gap(self):
        r = srtf(procs(("A", 2, 3), ("B", 10, 2)))
        self.assertEqual(r.timeline[0], ("Idle", 0, 2))
        self.assertEqual(ct(r), [5, 12])


if __name__ == "__main__":
    unittest.main()
