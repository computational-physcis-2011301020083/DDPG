from matplotlib import pyplot as plt
from Pipe import Pipe
from Global_List import *
import math
import numpy as np
from matplotlib.pyplot import MultipleLocator


# p = Pipe(40, 30)
# rho_i = 1.9
# p.Cv = (rho_i - rhoWater) / (rhoSand - rhoWater)
# qq = []
# Im = []
# If = []
# l = []
# h = []
# Re = []
# for q in range(2, 6, 1):
#     qq.append(q)
#     p.CalLoss(q)
#     Im.append(p.Im)
#     If.append(p.If)
#     l.append(p.loss)
#     # pumpH = 0.07576 * math.pow(q, 4) - 0.6566 * math.pow(q, 3) - 3.333 * math.pow(q, 2) + 3.113 * q + 700
#     # pumpH = -0.3125 * math.pow(q, 4) + 4.884 * math.pow(q, 3) - 28.78 * math.pow(q, 2) + 45.3 * q + 509.2
#     # pumpH = -0.3125 * math.pow(q, 4) + 4.884 * math.pow(q, 3) - 28.78 * math.pow(q, 2) + 45.3 * q + 19.2
#     pumpH = -0.4377 * math.pow(q, 3) + 1.3402 * math.pow(q, 2) + 2.7264 * math.pow(q, 1) + 46.5307
#     h.append(pumpH)
#
# # plt.plot(qq, Im)
# # plt.plot(qq, If)
# plt.plot(qq, l)
# plt.plot(qq, h)
# plt.show()


# # 测试耙头吸入密度
# v_sh = 2
# a = -3.03493352192820e-10
# b = 0.0551645264442086
# c = 1.33453140871192
#
# fig, ax = plt.subplots()
#
# for v in range(11):
#     RHO = []
#     Q = []
#     visorAngle = 0.1 * v
#     for i in range(10,61):
#         q = i/10 * 3600
#         Q.append(q)
#         rho_i = visorAngle * (a * math.pow(q, 2) + b * v_sh + c) + (1 - visorAngle) * rhoWater
#         RHO.append(rho_i)
#     plt.plot(Q, RHO)
#
#
# X_ticks = np.arange(3600, 25200, 3600)
# plt.xticks(X_ticks, [i for i in range(1,7,1)])
# x_major_locator=MultipleLocator(3600)
# ax.xaxis.set_major_locator(x_major_locator)
# plt.xlabel("Flow m³/s")
# plt.ylabel("Density  *10³kg/m³")
# lgnd = plt.legend(["VA=0.0", "VA=0.1", "VA=0.2", "VA=0.3", "VA=0.4", "VA=0.5", "VA=0.6", "VA=0.7", "VA=0.8", "VA=0.9", "VA=1.0"], bbox_to_anchor=(1.05, 1), loc=2)
# fig.subplots_adjust(right=0.75)
# plt.show()


# # 测试耙头吸入密度（虚拟三角函数）
# Q = []
# RHO = []
# for i in range(20):
#     q = 0.1 * i + 8
#     Q.append(q)
#     rho_i = (math.sin(2*math.pi*q-16*math.pi) + 1) * 0.8
#     RHO.append(rho_i)
#
# plt.plot(Q, RHO)
# plt.show()
# print(Q)


# # 画泵扬程曲线管路损失曲线
# length = 63
# angle = 40 * math.pi / 180
# rho_i = 1.9
# Cv = (rho_i - rhoWater) / (rhoSand - rhoWater)
# delta = 0.05e-3
# Q_list = []
# H = []
# for i in range(0, 71, 10):
#     rho_i = 1 + i * 0.01
#     Cv = (rho_i - rhoWater) / (rhoSand - rhoWater)
#     Q_list = []
#     L = []
#     H = []
#     for Q in range(1, 80, 10):
#         Q = Q / 10
#         Q_list.append(Q)
#         velocity = Q / (0.25 * math.pi * diameter * diameter)
#         Re = velocity * diameter / viscosity
#         lmbda = (68 / Re + delta / diameter + math.pow((28 * 68 / Re), 14)) / (115 * math.pow((28 * 68 / Re), 10) +1)
#         lmbda = 0.11 * math.pow(lmbda, 0.25)
#         If = lmbda * velocity * velocity / (2 * diameter * 9.81)
#         Kd = 30.25 * math.pow(d_m, -0.24) * math.pow(diameter, -0.44)
#         Im = velocity * velocity * math.sqrt(9.81 * d_50 * (upsilon_s / upsilon - 1))
#         Im = math.pow(Im / (9.81 * diameter * v_t), -3/2)
#         Im = Kd * Im * Cv * If + If
#         M = 0.5
#         loss = If + (Im - If) * math.pow(math.cos(angle), 1 + M) + Cv * (S_s - 1) * math.sin(angle)
#         loss = loss * length
#         L.append(loss)
#         # pumpH = -0.5902 * math.pow(Q, 3) + 1.915 * math.pow(Q, 2) + -3.39 * math.pow(Q, 1) + 59.34
#         pumpH = -0.5902 * math.pow(Q, 3) + 1.915 * math.pow(Q, 2) + -3.39 * math.pow(Q, 1) + 61.34
#         H.append(pumpH)
#     plt.plot(Q_list, L)
# plt.plot(Q_list, H)
# plt.show()


# #测试损失曲线
# p = Pipe(40, 30)
# rho_i = 1.9
# p.Cv = (rho_i - rhoWater) / (rhoSand - rhoWater)
#
# for i in range(1, 10, 8):
#     Q = []
#     L = []
#     rho_i = 1 + i * 0.1
#     p.Cv = (rho_i - rhoWater) / (rhoSand - rhoWater)
#     for q in range(1, 10, 1):
#         Q.append(q)
#         p.CalLoss(q)
#         L.append(p.loss)
#         plt.plot(Q, L)
#
#     print(L)
#
# plt.show()


# # test Gauss Distribution
# a = 0.5
# sig = 0.025
# for i in range(100):
#     p = np.random.normal(a, sig)
#     print(p)

# print(s)