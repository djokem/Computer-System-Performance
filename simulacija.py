import numpy as np


class Job:
    ID = 1
    jobs = []

    def __init__(self):
        self.id = Job.ID
        Job.ID = Job.ID + 1


class Server:
    servers = []
    ID = 1

    def __init__(self, s, pi):
        self.buffer = []
        self.current_job = None
        self.remaining_s = 0  # preostalo vreme za obradu posla
        self.probabilities = []
        self.busy = False
        self.id = Server.ID
        Server.ID = Server.ID + 1
        self.s = s  # prosecno vreme obrade na serveru

        for i in range(len(pi)):
            self.probabilities.append(self.probabilities[i - 1] + pi[i] if i > 0 and pi[i] > 0 else pi[i])

    def print_server_info(self):
        print("Server ", self.id, " info:")
        print("S=", self.s)
        print("Probabilities: ", str(self.probabilities), "\n")

    def addJob(self, job):
        self.buffer.append(job)

    def nextJob(self):
        if not self.busy and len(self.buffer) > 0:
            self.current_job = self.buffer.pop(0)
            self.busy = True
            print("Pocinje obrada posla id =", self.current_job.id, " na serveru id =", self.id, "\n")

    def endCurrentJob(self):

        p = np.random.uniform(0, 1)
        next_server = next(x for x, val in enumerate(self.probabilities) if val >= p)  # dohvatanje prvog elementa veceg od 'p' tj. index servera na ciji red treba poslati posao
        Server.servers[next_server].addJob(self.current_job)  # slanje trenutno zavrsenog posla na naredni server
        print("Zavrsena obrada posla id =", self.current_job.id, " na serveru id =", self.id,
              ". Posao ide u red za cekanje servera id =", next_server + 1, "\n")
        self.current_job = None
        self.busy = False


    def work(self):
        if not self.busy:
            self.nextJob()
            if self.current_job is not None:
                self.remaining_s = np.random.exponential(scale=self.s)
        else:
            self.remaining_s = self.remaining_s - 1
            if self.remaining_s <= 0.5:
                self.endCurrentJob()


