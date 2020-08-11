from Pipe import Pipe
from Global_List import *
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


class Env:
    def __init__(self):
        self.pumpOmiga = 200    #泵速
        self.visorAngle = 0.6   #耙唇活动罩打开的程度，0->完全打开，1->完全关闭
        self.v_sh = 1           #航速

        self.hz = 25
        self.hd = 3
        self.hi = 4

        self.pipeDown = Pipe(33, 40)
        self.pipeUp = Pipe(30, 40)
        self.Q = 3  #当前时刻流量
        self.pumpH = 0
        self.pipeLoss = 0

        self.rho_i = rhoWater

        self.changePump = 0

    def CalPumpH(self):
        self.pumpH = -0.5902 * math.pow(self.Q, 3) + 1.915 * math.pow(self.Q, 2) + -3.39 * math.pow(self.Q, 1) + 59.34
        if self.changePump == 1:
            self.pumpH = -0.5902 * math.pow(self.Q, 3) + 1.915 * math.pow(self.Q, 2) + -3.39 * math.pow(self.Q, 1) + 63.34

    def CalLossH(self):
        self.pipeDown.CalLoss(self.Q)
        self.pipeUp.CalLoss(self.Q)
        self.pipeLoss = self.pipeDown.loss + self.pipeUp.loss


    def RunOneStep(self):
        #泵吸入密度计算
        a = -3.03493352192820e-10
        b = 0.0551645264442086
        c = 1.33453140871192
        q = 3600 * self.Q

        self.rho_i = self.visorAngle * (a * math.pow(q, 2) + b * self.v_sh + c) + (1 - self.visorAngle) * rhoWater

        rhoAverage = (self.pipeDown.rho * self.pipeDown.discreteNumber + self.pipeUp.rho * self.pipeUp.discreteNumber) / (self.pipeDown.discreteNumber + self.pipeUp.discreteNumber)
        # self.pipeDown.rho = self.rho_i
        # self.pipeUp.rho = self.rho_i
        # self.pipeUp.rhoList *= self.rho_i
        # self.pipeDown.rhoList *= self.rho_i
        # rhoAverage = self.rho_i
        self.CalPumpH()
        self.CalLossH()
        Q_dot = Ap / (rhoAverage * self.pipeUp.length) * (self.pumpH - self.pipeLoss)
        self.Q += Q_dot * DeltaT

        #更新泵内密度分布
        pipeDownOut = self.pipeDown.Move(self.Q, rhoIn=self.rho_i)
        pipeUpOut = self.pipeUp.Move(self.Q, rhoInList=pipeDownOut)

        averageRhoIntoShip = np.sum(pipeUpOut) / len(pipeUpOut)
        self.massInShipOfEachTimeStep = (averageRhoIntoShip - rhoWater) * self.Q

    def RunEnv(self, a):
        self.visorAngle = a[0]
        self.RunOneStep()
        for i in range(200):
            self.RunOneStep()

        state = np.zeros(2)
        # state[0] = (self.pipeDown.rho * self.pipeDown.discreteNumber + self.pipeUp.rho * self.pipeUp.discreteNumber) / (self.pipeDown.discreteNumber + self.pipeUp.discreteNumber)
        state[0] = self.rho_i
        state[1] = self.Q

        r = self.rho_i * self.Q

        return state, r


if __name__ == "__main__":

    # #画F-P曲线
    # #注意要把上面rho_i那一行注释掉
    # s = Env()
    # F = []
    # P = []
    #
    # for j in range(61):
    #     s.rho_i = 1 + j * 0.01
    #     for i in range(1000):
    #         s.RunOneStep()
    #
    #     # print(s.pipeUp.rhoList.T)
    #     # print(s.pipeDown.rhoList.T)
    #
    #     print(s.Q*(s.rho_i-rhoWater), " ", s.Q, " ", s.pipeDown.rho, " ", s.pipeUp.rho, " ", s.pipeDown.loss + s.pipeUp.loss, " ", s.pumpH)
    #     P.append(s.Q*(s.rho_i-rhoWater))
    #     F.append(s.Q)
    #
    # plt.plot(F, P)
    # plt.show()


    #画产量-耙唇角度曲线
    s = Env()
    s.changePump = 1
    rho_s = 1
    s.pipeDown.rho = rho_s
    s.pipeUp.rho = rho_s
    s.pipeDown.rhoList = np.ones([s.pipeDown.discreteNumber, 1]) * rho_s
    s.pipeUp.rhoList = np.ones([s.pipeUp.discreteNumber, 1]) * rho_s
    V = []
    P = []
    for j in range(101):
        s.visorAngle = 0.01 * j
    # for j in range(11):
    #     s.visorAngle = 0.1 * j
        # for i in range(1000):
        #     s.RunOneStep()
        for i in range(200):
            s.RunOneStep()

        print(s.visorAngle, " ", s.Q*s.rho_i, " ", s.Q, " ", s.pipeDown.rho, " ", s.pipeUp.rho, " ", s.pipeDown.loss + s.pipeUp.loss, " ", s.pumpH)
        P.append(s.Q*s.rho_i)
        V.append(s.visorAngle)

    plt.plot(V, P)
    plt.show()


    # # 不同s状态下，验证a和r
    # print("Start!")
    #
    # env = Env()
    # SA = []
    # R = []
    # for i in range(13):
    #     rho = 1 + i * 0.05
    #     for j in range(50):
    #         q = 3 + j * 0.1
    #         for k in range(11):
    #             aa = k/10
    #             sa = [rho, q, aa]
    #             SA.append(sa)
    #
    # SA = np.array(SA)
    # rowsSA = SA.shape[0]
    # print("SA done!")
    # for i in range(rowsSA):
    #     rho_s = SA[i, 0]
    #     env.pipeDown.rho = rho_s
    #     env.pipeUp.rho = rho_s
    #     env.pipeDown.rhoList = np.ones([env.pipeDown.discreteNumber, 1]) * rho_s
    #     env.pipeUp.rhoList = np.ones([env.pipeUp.discreteNumber, 1]) * rho_s
    #     env.Q = SA[i, 1]
    #     env.visorAngle = SA[i, 2]
    #     # for j in range(500):
    #     #     env.RunOneStep()
    #     # for j in range(400):
    #     env.RunOneStep()
    #     print("i: ", i, " ", env.Q*env.rho_i)
    #     R.append(env.Q*env.rho_i)
    #
    # data_SA = pd.DataFrame(SA)
    # writerSA = pd.ExcelWriter('sa_all.xlsx')
    # data_SA.to_excel(writerSA, 'page_1')
    # writerSA.save()
    # writerSA.close()
    #
    # R = np.array(R)
    # data_R = pd.DataFrame(R)
    # writerR = pd.ExcelWriter('r.xlsx')
    # data_R.to_excel(writerR, 'page_1')
    # writerR.save()
    # writerR.close()


    # #多步debug
    # env = Env()
    # rho_s = 1
    # env.pipeDown.rho = rho_s
    # env.pipeUp.rho = rho_s
    # env.pipeDown.rhoList = np.ones([env.pipeDown.discreteNumber, 1]) * rho_s
    # env.pipeUp.rhoList = np.ones([env.pipeUp.discreteNumber, 1]) * rho_s
    # env.Q = 1
    #
    #
    #
    # for i in range(1000):
    #     env.RunOneStep()
    #
    # print(env.rho_i, " ", env.Q, " ", env.rho_i * env.Q)


    print("Press any key to continue......")