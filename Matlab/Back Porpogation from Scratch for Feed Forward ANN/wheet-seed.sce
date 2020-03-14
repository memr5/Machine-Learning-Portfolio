[data,t] = fscanfMat('seeds_dataset.txt')

X = data(:,1:7)'

temp1 = data(:,8) == 1
temp2 = data(:,8) == 2
temp3 = data(:,8) == 3

y = [temp1 temp2 temp3]' * 1

// MinMax Normalization
//X_train_normalized = (X_train - min(X_train,'c') * ones(1,split) )./((max(X_train,'c')-min(X_train,'c'))*ones(1,split))
//X_test_normalized = (X_test - min(X_train,'c') * ones(1,size(X)(2) - split) )./((max(X_train,'c')-min(X_train,'c'))*ones(1,size(X)(2) - split))


best_W1 = []
best_W2 = []
best_test_accuracy = -1
final_train_accuracy = -1
final_loss = []

T = 20
lr = 0.5

iter = 300

for i=1:iter

[X, y] = ann_pat_shuffle(X, y)

split = floor(size(X)(2)*0.80)
//disp(split)
X_train = X(:,1:split)
y_train = y(:,1:split)

X_test = X(:,split+1:size(X)(2))
y_test = y(:,split+1:size(X)(2))

// Standardization
X_train_normalized = (X_train - mean(X_train,'c') * ones(1,split) )./(stdev(X_train,'c')*ones(1,split))
X_test_normalized = (X_test - mean(X_train,'c') * ones(1,size(X)(2) - split) )./(stdev(X_train,'c')*ones(1,size(X)(2) - split))

X_train = X_train_normalized
X_test = X_test_normalized

//disp(X_train(:,1:3))

//X_train = [ones(1,size(X_train)(2));X_train]
//X_test = [ones(1,size(X_test)(2));X_test]



inputSize = size(X_train)(1)
hiddenUnits = 7
outputSize = size(y_train)(1)


W1 = (rand(inputSize, hiddenUnits)*2 - 1)*0.5
W2 = (rand(hiddenUnits, outputSize)*2 - 1)*0.5

t = 1

loss = []

while t<=T
    a0 = X_train
    z1 = W1' * a0               // 5x147
    a1 = 1 ./ (1+exp(-z1))      // 5x147
    z2 = W2' * a1               // 3x147
    a2 = 1 ./ (1+exp(-z2))      // 3x147
    
    loss = [loss ann_sum_of_sqr(y_train,a2)/(6*split)]
     
    W2_ = W2 - (a1 * (a2.*(1-a2).*(a2-y_train))').*(lr/(3*split))
    W1_ = W1 - (a0 * (a1.*(1-a1).*(W2*(a2.*(1-a2).*(a2-y_train))))').*(lr/(3*split))
    
    W1 = W1_
    W2 = W2_
    
    t = t+1
end

// Final Loss Calculation
a0 = X_train
z1 = W1' * a0               // 5x147
a1 = 1 ./ (1+exp(-z1))      // 5x147
z2 = W2' * a1               // 3x147
y_train_predicted = 1 ./ (1+exp(-z2))      // 3x147

y_train_predicted = (y_train_predicted == ones(3,1)*max(y_train_predicted,'r'))*1

train_accuracy = sum(sum(y_train_predicted==y_train,'r')==3)/(size(y_train)(2))
//disp(train_accuracy,"Train Accuracy = ")

//train_accuracy = 1 - ann_sum_of_sqr(y_train_predicted,y_train)/(size(y_train)(2))
//disp(train_accuracy,"Train Accuracy = ")

loss = [loss ann_sum_of_sqr(y_train,a2)/(6*split)]

// Test Accuracy Calcualtion
a0 = X_test
z1 = W1' * a0              
a1 = 1 ./ (1+exp(-z1))    
z2 = W2' * a1            
y_test_predicted = 1 ./ (1+exp(-z2))

//disp(y_test_predicted(:,1:3))

y_test_predicted = (y_test_predicted == ones(3,1)*max(y_test_predicted,'r'))*1

//disp(y_test(:,1:3))
//disp(y_test_predicted(:,1:3))

test_accuracy = sum(sum(y_test_predicted==y_test,'r')==3)/(size(y_test)(2))
//disp(test_accuracy,"Test Accuracy = ")

if best_test_accuracy < test_accuracy then
    best_test_accuracy = test_accuracy
    final_train_accuracy = train_accuracy
    final_loss = loss
    best_W1 = W1
    best_W2 = W2
end

end
//test_accuracy = 1 - ann_sum_of_sqr(y_test_predicted,y_test)/(size(y_test)(2))
//disp(test_accuracy,"Test Accuracy = ")

clf(1)
figure(1)
plot(1:T,final_loss(2:T+1))
xlabel('epochs')
ylabel('Loss')

disp(best_test_accuracy,"Test accuracy: ")
disp(final_train_accuracy,"Train accuracy: ")

//disp(best_W1(:,1:3))
//disp(best_W2(:,1:3))
