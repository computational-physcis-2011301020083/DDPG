clear
clc
close all


DeltaT = 1;
d_m = 0.0025e-3;     
d_50 = 0.0025e-3;   
upsilon_s = 1.7;    
upsilon = 1;         
upsilon_m = 2.65;
v_t = 6e-6;          
S_s = 2.65;      
rhoWater = 1;
rhoSand = 1.75;      
viscosity = 6e-3;
diameter = 1;
length = 40;
angle = 40 * pi / 180;
rho_i = 1.9;
Cv = (rho_i - rhoWater) / (rhoSand - rhoWater);
delta = 0.05e-3;

Q_list = zeros(60,10);
L = zeros(60,10);
H = zeros(60,10);
for i = 1:1:10
    rho_i = 0.9 + i * 0.1;
    Cv = (rho_i - rhoWater) / (rhoSand - rhoWater);
    Q = 1;
    for j = 1:1:60
        Q_list(j,i) = Q;
        velocity = Q / (0.25 * pi * diameter * diameter);

        Re = velocity * diameter / viscosity;
        lmbda = (68 / Re + delta / diameter + ((28 * 68 / Re)^14)) / (115 * ((28 * 68 / Re)^10) +1);
        lmbda = 0.11 * (lmbda^0.25);
        If = lmbda * velocity * velocity / (2 * diameter * 9.81);

        Kd = 30.25 * power(d_m, -0.24) * (diameter^-0.44);

        Im = velocity * velocity * sqrt(9.81 * d_50 * (upsilon_s / upsilon - 1));
        Im = power(Im / (9.81 * diameter * v_t), -3/2);
        Im = Kd * Im * Cv * If + If;

        M = 0.5;
        loss = If + (Im - If) * power(cos(angle), 1 + M) + Cv * (S_s - 1) * sin(angle);
        loss = loss * length;
        L(j,i) = loss;
        
        pumpH = -0.4377 * power(Q, 3) + 1.3402 * power(Q, 2) + 2.7264 * power(Q, 1) + 46.5307;
        H(j,i) = pumpH;
        Q = Q + 0.1;
    end
end
for i=1:1:10
    plot(Q_list(:,i), L(:,i))
    hold on
end

x = [0, 1, 1.8, 2.3, 3.2, 3.7, 4, 4.3, 4.55, 4.8, 5, 5.2, 5.3];
y = [59.2, 58, 55.06, 54.39, 49.19, 43.51, 38.96, 33.46, 26.60, 22.03, 16.59, 10.64, 7.454];

p1 =     -0.5902;
p2 =       1.915;
p3 =       -3.39;
p4 =       59.34;

QQ = 1:0.1:6.9;
HH = zeros(60, 1);
for i=1:1:60
    HH(i) = p1*QQ(i)^3 + p2*QQ(i)^2 + p3*QQ(i) + p4;
end
plot(Q_list(:, 1), HH)