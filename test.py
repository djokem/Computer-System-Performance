import proba
import simulacija as sim

x = 2

s = [5, 20, 15, 15]
sk = [20]*x
s = s + sk

P1 = [0.1, 0.1, 0.1, 0.1] + [0.6/x]*x
P2 = [0.1, 0.3, 0.5, 0.1] + [0]*x
P3 = [1, 0, 0, 0] + [0]*x
P4 = [1, 0, 0, 0] + [0]*x

P = [P1,P2,P3,P4]
for y in range(x):
    pi = [1] + [0] * 3 + [0] * x
    P.append(pi)

N = 1

for i in range(len(s)):
    sim.Server.servers.append(sim.Server(s[i], P[i]))

for i in range(N):
    sim.Job.jobs.append(sim.Job())

for j in sim.Job.jobs:
    sim.Server.servers[0].addJob(j)

time = 100
while time > 0:

    for s in sim.Server.servers:
        s.work()

    for s in sim.Server.servers:
        s.nextJob()

    time = time - 1