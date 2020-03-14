x = -10:10;
alpha = [0.1 0.33 0.5]
sigmoid = 1./(1+exp(-x))
figure(1)
subplot(4,1,1)
plot(x,sigmoid)

sigmoid = 1./(1+0.1*exp(-x))
subplot(4,1,2)
plot(x,sigmoid)

sigmoid = 1./(1+0.33*exp(-x))
subplot(4,1,3)
plot(x,sigmoid)

sigmoid = 1./(1+0.5*exp(-x))
subplot(4,1,4)
plot(x,sigmoid)
