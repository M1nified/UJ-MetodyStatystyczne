class Task:
    def __init__(self, created_at, duration):
        self.created_at = created_at
        self.duration = duration
        self.started_at = None
        self.finished_at = None

    def __str__(self):
        return "Task " + str(self.created_at) + " " + str(self.duration) + " " + str(self.started_at) + " " +\
               str(self.finished_at)

    def __unicode__(self):
        return str(self)

    def __repr__(self):
        return str(self)
