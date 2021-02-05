"""
第一题，哲学家就餐问题
"""
from threading import Lock


class DiningPhilosophers:
    def __init__(self):
        self.ForkList = [Lock() for _ in range(5)]

    def wantsToEat(self,
                    philosopher,
                    pickLeftFork,
                    pickRightFork,
                    eat,
                    putLeftFork,
                    putRightFork):

        self.ForkList[philosopher % 5].acquire()
        pickRightFork()
        self.ForkList[(philosopher + 1) % 5].acquire()
        pickLeftFork()
        eat()
        putLeftFork()
        self.ForkList[(philosopher + 1) % 5].release()
        putRightFork()
        self.ForkList[philosopher % 5].release()
