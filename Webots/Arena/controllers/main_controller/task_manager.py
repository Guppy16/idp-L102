class Task():
    def __init__(self, target, args, kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs
    
    def execute_task(self):
        return self.target(*self.args, **self.kwargs)


class TaskManager():
    def __init__(self, tasks):
        self.stack = [tasks]
    
    def next_task(self):
        """Pops the task from the list of tasks and executes the next task"""
        if self.stack == []:
            return False
        task = self.stack.pop()
        # Execute task and push back to stack if not completed
        if not task.execute_task():
            self.stack.append(task)
        return True
