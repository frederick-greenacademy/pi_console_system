# import sched, time

# def myTask(m,n):
#   print(n + ' ' + m)

# def periodic_queue(interval,func,args=(),priority=1):
#   s = sched.scheduler(time.time, time.sleep)
#   periodic_task(s,interval,func,args,priority)
#   s.run()

# def periodic_task(scheduler,interval,func,args,priority):
#   func(*args)
#   scheduler.enter(interval,priority,periodic_task,
#                    (scheduler,interval,func,args,priority))

# periodic_queue(1,myTask,('world','hello'))

import pkgutil
search_path = ['.src/'] # set to None to see all modules importable from sys.path
all_modules = [x[1] for x in pkgutil.iter_modules(path=search_path)]
print(all_modules)