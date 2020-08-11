import math


DeltaT = 1
d_m = 0.0025e-3     #平均粒径mm
d_50 = 0.0025e-3    #中值粒径mm
upsilon_s = 1.7     #固体容重
upsilon = 1         #清水容重
upsilon_m = 2.65    #泥浆容重
# v_t = 6e-3          #颗粒静水中沉降速度mm/s
v_t = 6e-6          #颗粒静水中沉降速度m/s
S_s = 2.65          #固体颗粒比重t/m3
rhoSand = 1.75      #土颗粒密度t/m3
rhoWater = 1        #水密度
viscosity = 6e-3    #粘性系数

diameter = 1        #船上均使用1米管
Ap = 1 / 4 * math.pi * diameter *diameter

# MAX_EPISODES = 200
# MAX_EP_STEPS = 200
MAX_EPISODES = 2
MAX_EP_STEPS = 3000
LR_A = 0.001    # learning rate for actor
LR_C = 0.002    # learning rate for critic
GAMMA = 0.9     # reward discount
TAU = 0.01      # soft replacement
MEMORY_CAPACITY = 256
BATCH_SIZE = 64
# MEMORY_CAPACITY = 1024
# BATCH_SIZE = 1024

rho_min = 1
rho_max = 1.6
Q_min = 3
Q_max = 6
r_min = 5
r_max = 6