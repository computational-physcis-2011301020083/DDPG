import numpy as np
from Global_List import *


class Pipe:
    def __init__(self, L, angle):
        self.length = L
        self.angle = angle * math.pi / 180
        self.delta = 0.05e-3   #管道相对粗糙度

        self.discreteNumber = 1000
        self.l = self.length / self.discreteNumber

        self.rhoList = np.ones([self.discreteNumber, 1]) * rhoWater
        self.con = np.zeros([self.discreteNumber, 1])
        self.rho = 1    #管内平均密度
        self.Cv = 0     #管内平均浓度

        self.velocity = 0      #管内流速
        self.loss = 0

    def CalCv(self):
        #计算管内的平均浓度
        for i in range(self.discreteNumber):
            self.con[i,0] = (self.rhoList[i,0] - rhoWater) / (rhoSand - rhoWater)

        self.Cv = np.sum(self.con) / len(self.con)

    def CalUpsilon_m(self):
        #计算管内泥浆容重
        self.upsilon_m = np.sum(self.rhoList) / (self.discreteNumber * rhoWater)

    def CalVelocity(self, Q):
        #计算管内流速
        self.velocity = Q / (0.25 * math.pi * diameter * diameter)

    def CalLoss(self, Q):
        self.CalVelocity(Q)
        self.CalUpsilon_m()
        self.CalCv()

        Re = self.velocity * diameter / viscosity
        lmbda = (68 / Re + self.delta / diameter + math.pow((28 * 68 / Re), 14)) / (115 * math.pow((28 * 68 / Re), 10) + 1)
        lmbda = 0.11 * math.pow(lmbda, 0.25)
        If = lmbda * self.velocity * self.velocity / (2 * diameter * 9.81)

        Kd = 30.25 * math.pow(d_m, -0.24) * math.pow(diameter, -0.44)

        Im = self.velocity * self.velocity * math.sqrt(9.81 * d_50 * (upsilon_s / upsilon - 1))
        Im = math.pow(Im / (9.81 * diameter * v_t), -3 / 2)
        Im = Kd * Im * self.Cv * If + If

        M = 0.5
        self.loss = If + (Im - If) * math.pow(math.cos(self.angle), 1 + M) + self.Cv * (S_s - 1) * math.sin(self.angle)

        self.loss = self.loss * self.length

    def Move(self, Q, rhoIn = -99, rhoInList = np.zeros([1,1])):
        dis = int(round(Q * DeltaT / (0.25 * math.pi * diameter * diameter)))
        if dis > self.rhoList.shape[0]:
            dis = self.rhoList.shape[0]

        rhoOut = np.zeros([dis, 1])
        rhoOut[:dis, 0] = self.rhoList[-dis:, 0]

        newRho = np.zeros([self.rhoList.shape[0], 1])
        for i in range(self.rhoList.shape[0] - dis):
            newRho[dis + i, 0] = self.rhoList[i, 0]

        if rhoIn == -99:
            newRho[:dis, 0] = rhoInList[:dis, 0]
        else:
            rhoInList = np.ones([dis, 1]) * rhoIn
            newRho[:dis, 0] = rhoInList[:dis, 0]

        self.rhoList = newRho
        self.rho = np.sum(self.rhoList) / len(self.rhoList)

        return rhoOut
