class Server:
    def __init__(self):
        self.task = None

    def assign_task(self, task, time):
        self.task = task
        self.task.started_at = time
        self.task.finished_at = self.task.started_at + self.task.duration
        # print 'TASK ASSIGNED:', self.task

    def clear(self):
        self.task = None

    def is_free(self, time):
        # print 'IS_FREE', time, self.task
        if self.task is None:
            return True
        elif self.task.finished_at > time:
            return False
        else:
            return True
