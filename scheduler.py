from datetime import datetime

class Scheduler:

    def should_run(self):
        return True

    def now(self):
        return datetime.now()

scheduler = Scheduler()
