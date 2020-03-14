//EXE 1 Using an in-Built Function
X = 1:5
y = [10 40 50 78 83]

[a, b] = reglin(X,y)

disp(a,"a (reglin) = ")
disp(b,"b (reglin) = ")
disp(ann_sum_of_sqr(y,X.*a + b)/10, 'LOSS = ')

figure(1)
scatter(X,y)
y_pred = X.*a + b
plot(X,y_pred)
xlabel('X')
ylabel('y')


//EXE 2 To Plot Losses at different values of a where h(X) = aX + 0
loss = []

for i=-100:100
    loss = [loss ann_sum_of_sqr(y,X.*i)/10]
end

figure(2)
plot(-100:100,loss)
xlabel('a')
ylabel('Loss')


//EXE 3 Vectorized implementation of Gragient Descent
X = [ones(1,5);X]
W = [0 0]

T = 100
t = 1
lp = 0.1

loss = []

while t<=T
    W_ = W - ((W*X - y)*X').*(lp/5)
    W = W_
    loss = [loss ann_sum_of_sqr(y,W*X)/10]
    t = t + 1
end

disp(W(2),"a = ")
disp(W(1),"b = ")
disp(ann_sum_of_sqr(y,W*X)/10,"Loss = ")

figure(4)
plot(1:T,loss)
xlabel('epochs')
ylabel('Loss')
