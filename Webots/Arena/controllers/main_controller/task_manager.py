class Task():
    def __init__(self, target=None, args=[], kwargs={}):
        self.target = target
        self.args = args
        self.kwargs = kwargs
    
    def execute_task(self):
        return self.target(*self.args, **self.kwargs)


class TaskManager():
    def __init__(self, tasks):
        """Add tasks in reverse
        tasks: arrays of Task
        """
        self.stack = list(reversed(tasks))
    
    def push_task(self, task):
        self.stack.append(task)

    def push_tasks_in_reverse(self, tasks):
        self.stack.append(tasks.reverse())

    def next_task(self):
        """Pops the task from the list of tasks and executes the next task"""
        # print(self.stack)
        if self.stack == []:
            return False
        task = self.stack.pop()
        # Execute task and push back to stack if not completed
        if not task.execute_task():
            self.stack.append(task)
        return True
