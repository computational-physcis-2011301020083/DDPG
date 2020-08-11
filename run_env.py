from Pipe import Pipe
from Global_List import *
from Env import Env
import numpy as np
from ddpg import DDPG
import pandas as pd
import time


s_dim = 2
a_dim = 1
# sig = 0.3333
sig = 1
P = 1   #随机选择action的概率

ddpg = DDPG(a_dim, s_dim)
LST = []
# RANDOM = True
RANDOM = False
env = Env()
env.changePump = 0
s = np.ones(2)
for i in range(MAX_EPISODES):
    if i == 1:
        env.changePump = 1
        # RANDOM = True
        # ddpg.pointer = 0
        sig = 1
    ep_reward = 0
    for j in range(MAX_EP_STEPS):
        print("i:", i, "j:", j)
        lst = []
        a = ddpg.choose_action(s)
        print(a)
        if RANDOM == True:
            a = ddpg.RandomChooseAction(a, P)
        else:
            a = np.clip(np.random.normal(a, sig), 0, 1)

        s_, r = env.RunEnv(a)
        ddpg.store_transition(s, a, r, s_)
        lst.append(s[0])
        lst.append(s[1])
        lst.append(a[0])
        lst.append(r)
        lst.append(s_[0])
        lst.append(s_[1])
        LST.append(lst)
        if ddpg.pointer == MEMORY_CAPACITY:
            RANDOM = False

        if ddpg.pointer > MEMORY_CAPACITY:
            sig *= 0.995
            for k in range(10):
                ddpg.learn()

        print(s, " ", a, " ", r, " ", s_)
        print("------------------------华丽丽的分割线------------------------")
        s = s_
        ep_reward += r

LST = np.array(LST)
data_LST = pd.DataFrame(LST)
writerLST = pd.ExcelWriter('LST_0606-2.xlsx')
data_LST.to_excel(writerLST, 'page_1')
writerLST.save()
writerLST.close()


S = []
SA = []
for i in range(61):
    rho = 1 + i * 0.01
    for j in range(50):
        q = 3 + j * 0.1
        for k in range(11):
            aa = k/10
            sa = [rho, q, aa]
            SA.append(sa)
        ss = [rho, q]
        S.append(ss)
S = np.array(S)
SA = np.array(SA)
A = []
for i in range(61*50):
    a = ddpg.choose_action(S[i, :])
    A.append(a)

Q = []
for i in range(61*50*10):
    q = ddpg.testQnet(SA[i, :])
    q_sque = np.squeeze(q)
    Q.append(q_sque)

Q = np.array(Q)
data_SA = pd.DataFrame(SA)
writerSA = pd.ExcelWriter('sa.xlsx')
data_SA.to_excel(writerSA, 'page_1')
writerSA.save()
writerSA.close()

data_Q = pd.DataFrame(Q)
writerQ = pd.ExcelWriter('q.xlsx')
data_Q.to_excel(writerQ, 'page_1')
writerQ.save()
writerQ.close()

# print(A)