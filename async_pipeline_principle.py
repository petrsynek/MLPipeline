import asyncio
import datetime
import random
import time


def fire_and_forget(f):
    """self explaining wrapper"""

    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, *kwargs)

    return wrapped


def foo(i):
    """some difficult computational task :D"""
    print(f"Process {i} started")
    time.sleep(random.randint(0, 20))
    print(f"Process {i} completed")


class Pipeline:

    def __init__(self):
        """creates several tasks in que at init,, just lazy here..."""
        self.tasks_to_run = {f'{i}': foo for i in range(10)}
        self.tasks_running = {}
        self.tasks_complete = {}

    def run(self):
        """this is basically the crudest async scheduler implementation that I could find
        but again - no imports - you asked for it, and I am not going to reinvent wheel"""
        time_start = datetime.datetime.now()
        # while there are tasks in queue or tasks running
        while self.tasks_to_run or self.tasks_running:
            print(f"\nScheduler ticks... \nElapsed time {(datetime.datetime.now() - time_start).seconds} \n"
                  f"TTR: {list(self.tasks_to_run.keys())} \n"
                  f"TRU: {list(self.tasks_running.keys())} \n"
                  f"TCO: {list(self.tasks_complete.keys())} \n"
                  f"\nMeanwhile:"
                  )
            # each tick I launch 1 task from queue
            if self.tasks_to_run:
                i = list(self.tasks_to_run.keys())[0]
                self.task_launcher(i, self.tasks_to_run.pop(i))
            # tick - tock
            time.sleep(1)

        # and finishing remarks...
        print(
            f"Process finished in {(datetime.datetime.now() - time_start).seconds} seconds\n"
            f"TTR: {list(self.tasks_to_run.keys())} \n"
            f"TRU: {list(self.tasks_running.keys())} \n"
            f"TCO: {list(self.tasks_complete.keys())} \n"
        )

    @fire_and_forget
    def task_launcher(self, i, task):
        # this async function have access to Pipeline attributes, in real world it would be DB
        # i move task to running
        self.tasks_running.update({i: task})
        # wait for it
        task(i)
        # move the task to completed
        self.tasks_running.pop(i)
        self.tasks_complete.update({i: task})


if __name__ == '__main__':
    dummy_pipeline = Pipeline()
    dummy_pipeline.run()
