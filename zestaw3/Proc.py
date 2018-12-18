import random

from zestaw3.Change import Change
from zestaw3.Server import Server
from zestaw3.Task import Task
from zestaw3.CONSTS import TIME, STEP, AVG_STEP, rev_dyst


class Proc:
    def __init__(self, lam_1, lam_2, k, c=None):
        self.lam_1 = lam_1
        self.lam_2 = lam_2
        self.k = k
        self.c = c
        self.tasks = []
        self.queue = []
        self.populate_loop_time = 0
        self.servers = [Server() for _ in range(k)]
        self.system_time = 0

        self.log_queue_count = []
        self.log_system_count = []

        self.log_queue_count.append(Change(self.system_time, 0))
        self.log_system_count.append(Change(self.system_time, 0))

        self.summary_tasks_in_system_list = []
        self.summary_tasks_in_queue_list = []
        self.summary_avg_tasks_in_system_list = []
        self.summary_avg_tasks_in_queue_list = []

        print self.servers

    def __str__(self):
        return "Proc " + str(self.lam_1) + "/" + str(self.lam_2) + "/" + str(self.k) + "/" + str(self.c)

    def __unicode__(self):
        return str(self)

    def __repr__(self):
        return str(self)

    def display_tasks(self):
        for task in self.tasks:
            print task

    def populate_loop(self, max_time=None):
        self.populate_loop_time += rev_dyst(self.lam_1, random.random())
        task_duration = rev_dyst(self.lam_2, random.random())
        task = Task(self.populate_loop_time, task_duration)
        self.tasks.append(task)
        self.queue.append(task)
        if max_time is None or self.populate_loop_time < max_time:
            return True
        else:
            return False

    def system_loop(self):
        print 'SYSTEM_LOOP TIME IS: ', self.system_time, '| QUEUE:', self.queue_count(),\
            '| WORKING SERVERS:', self.k - self.free_servers_count(), '/', self.k

        for srv in self.servers:
            if srv.is_free(self.system_time):
                srv.clear()
                if self.queue_count() > 0:
                    task = self.queue.pop(0)
                    srv.assign_task(task, max(self.system_time, task.created_at))
        next_finish_time = self.find_next_server_finish_time()
        next_start_time = self.find_next_server_start_time()
        time = next_finish_time
        if next_start_time > self.system_time:
            time = next_start_time
        if self.queue_count() == 0 and time == self.system_time:
            finish_times = map(lambda srv: None if srv.task is None else srv.task.finished_at, self.servers)
            finish_times = filter(lambda t: t > self.system_time, finish_times)
            finish_times.sort()
            # print 'FINISH TIMES:', finish_times
            time = finish_times[0]
        self.system_time = time
        # self.display_tasks()

    def all_servers_free(self):
        for srv in self.servers:
            if not srv.is_free(self.system_time):
                return False
        return True

    def free_servers_count(self):
        count = 0
        for srv in self.servers:
            if srv.is_free(self.system_time):
                count += 1
        return count

    def find_next_server_finish_time(self):
        time = None
        for srv in self.servers:
            if srv.task is not None:
                if time is None or time > srv.task.finished_at:
                    time = srv.task.finished_at
        return time

    def find_next_server_start_time(self):
        time = None
        for srv in self.servers:
            if srv.task is not None:
                if time is None or time > srv.task.started_at:
                    time = srv.task.started_at
        return time

    def queue_count(self):
        return len(self.queue)

    # data extractors

    def tasks_in_system(self, t):  # x
        count = 0
        for task in self.tasks:
            if task.created_at < t < task.finished_at:
                count += 1
        return count

    def tasks_in_queue(self, t):  # x_w
        count = 0
        for task in self.tasks:
            if task.created_at < t < task.started_at:
                count += 1
        return count

    def avg_time_in_system(self):  # E(R)
        sums = map(lambda task: task.finished_at - task.created_at, self.tasks)
        time_sum = reduce(lambda a, b: a + b, sums)
        avg = time_sum / len(self.tasks)
        return avg

    def calculate_summary(self):
        # time in system
        t = 0
        count = []
        while t <= TIME:
            count.append(self.tasks_in_system(t))
            t += STEP
        self.summary_tasks_in_system_list = count

        # time in queue
        t = 0
        count = []
        while t <= TIME:
            count.append(self.tasks_in_queue(t))
            t += STEP
        self.summary_tasks_in_queue_list = count

        # avg time in system
        t = 0
        count = []
        i = 0
        while i < len(self.summary_tasks_in_system_list):
            s = 0
            j = 0
            while j < AVG_STEP / STEP and i + j < len(self.summary_tasks_in_system_list):
                s += self.summary_tasks_in_system_list[i + j]
                j += 1
            count.append(1.0 * s / j)
            i += j
        self.summary_avg_tasks_in_system_list = count

        # avg time in queue
        t = 0
        count = []
        i = 0
        while i < len(self.summary_tasks_in_queue_list):
            s = 0
            j = 0
            while j < AVG_STEP / STEP and i + j < len(self.summary_tasks_in_queue_list):
                s += self.summary_tasks_in_system_list[i + j]
                j += 1
            count.append(1.0 * s / j)
            i += j
        self.summary_avg_tasks_in_queue_list = count
