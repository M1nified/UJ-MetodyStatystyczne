#!/usr/bin/python2.7

import matplotlib.pyplot as plt
import math

from zestaw3.CONSTS import TIME, SIMULATIONS, STEP, AVG_STEP, lam_1, lam_2
from zestaw3.Proc import Proc


# def f(t):
#     return lam * math.exp(-lam * t)


def simulate():
    proc = Proc(lam_1, lam_2, 1)
    print proc

    while proc.populate_loop(TIME):
        pass

    proc.display_tasks()

    print 'START SYSTEM'

    while proc.queue_count() > 0 or not proc.all_servers_free():
        print "-----------------------------------------------"
        proc.system_loop()
        # raw_input("-----------------------------------------------")
    proc.system_loop()

    print 'RESULT:'
    proc.display_tasks()

    proc.calculate_summary()
    return proc


procs = []
for i in range(SIMULATIONS):
    p = simulate()
    procs.append(p)

# print

ran = map(lambda t: t * STEP, range(int(math.floor(TIME / STEP))))
ran2 = map(lambda t: t * AVG_STEP, range(int(math.floor(TIME / AVG_STEP))))

proc = procs[0]

plt.figure(10)
plt.xlabel("time")
plt.ylabel("tasks in system")
plt.title("Tasks in system")
print len(ran), len(proc.summary_tasks_in_system_list)
values = proc.summary_tasks_in_system_list
while len(values) > len(ran):
    values.pop()
plt.plot(ran, values, '.')
# plt.bar(ran, values)


plt.figure(11)
plt.xlabel("time")
plt.ylabel("tasks in queue")
plt.title("Tasks in queue")
print len(ran), len(proc.summary_tasks_in_queue_list)
values = proc.summary_tasks_in_queue_list
while len(values) > len(ran):
    values.pop()
plt.plot(ran, values, '.')

plt.figure(10)
plt.xlabel("time")
plt.ylabel("tasks in system")
plt.title("AVG Tasks in system")
values = proc.summary_avg_tasks_in_system_list
print len(ran2), len(values)
while len(values) > len(ran2):
    values.pop()
plt.plot(ran2, values, '.')
plt.bar(ran2, values, width=AVG_STEP, color="red")

plt.figure(21)
plt.xlabel("time")
plt.ylabel("tasks in queue")
plt.title("AVG Tasks in queue")
values = proc.summary_avg_tasks_in_queue_list
print len(ran2), len(values)
while len(values) > len(ran2):
    values.pop()
plt.plot(ran2, values, '.')

plt.show()
