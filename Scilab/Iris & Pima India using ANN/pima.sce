data = csvRead('pima-indians-diabetes.csv')

X = data(:,1:8)'
y = data(:,9)'

// Train-Test split
[X, y] = ann_pat_shuffle(X, y)
split = floor(size(X)(2)*0.7)
X_train = X(:,1:split)
y_train = y(:,1:split)

X_test = X(:,split+1:size(X)(2))
y_test = y(:,split+1:size(X)(2))


// Filling missing values
for i=2:6
    temp0 = X_train(i,:)
    if i == 4 || i == 5 then
        temp1 = median(temp0(temp0~=0))
    else
        temp1 = mean(temp0(temp0~=0))
    end       
    temp0(temp0==0) = temp1
    X_train(i,:) = temp0
end

for i=2:6
    temp0 = X_test(i,:)
    if i == 4 || i == 5 then
        temp1 = median(temp0(temp0~=0))
    else
        temp1 = mean(temp0(temp0~=0))
    end
    temp0(temp0==0) = temp1
    X_test(i,:) = temp0
end


// MinMax Normalization
X_train_normalized = (X_train - min(X_train,'c') * ones(1,split) )./((max(X_train,'c')-min(X_train,'c'))*ones(1,split))
X_test_normalized = (X_test - min(X_train,'c') * ones(1,size(X)(2) - split) )./((max(X_train,'c')-min(X_train,'c'))*ones(1,size(X)(2) - split))


// Modeling 
N = [8 8 8 1]

W = ann_FF_init(N)

lp = [0.1,0.00001]
T = 50
t = 1

train_losses = []
test_losses = []

train_accuracies = []
test_accuracies = []

while t<=T
    W_updated = ann_FF_Std_online(X_train_normalized, y_train, N, W, lp, 1)

    //W_updated = ann_FF_Std_batch(X_train, y_train, N, W, lp, 1)
    W = W_updated
    
    y_train_predicted = ann_FF_run(X_train_normalized, N, W)
    y_test_predicted = ann_FF_run(X_test_normalized, N, W)
    
    disp(t,"Epoch: ")
    
    train_loss = ann_sum_of_sqr(y_train_predicted, y_train)/split
    disp(train_loss,'Training Loss: ')
    test_loss = ann_sum_of_sqr(y_test_predicted, y_test)/(size(X)(2) - split)
    disp(test_loss,'Testset Loss: ')
    
    train_accuracy = 1 - ann_sum_of_sqr(y_train_predicted>=0.5,y_train)/split
    test_accuracy = 1 - ann_sum_of_sqr(y_test_predicted>=0.5,y_test)/(size(X)(2) - split)
    disp(train_accuracy,'Training Accuracy: ')
    disp(test_accuracy,'Test Accuracy: ')
    disp("")
    
    train_losses = [train_losses train_loss]
    test_losses = [test_losses test_loss]
    train_accuracies = [train_accuracies train_accuracy]
    test_accuracies = [test_accuracies test_accuracy]
    
    if t>=2 then
        clf(1)
        figure(1)
        plot((1:t)',[train_losses;test_losses]')
        //plot(1:t,test_losses,c='b')
        xlabel('Epochs')
        ylabel('Loss')
        title('Train & Test Losses')
        hl=legend(['train loss';'test loss']');
        
        clf(2)
        figure(2)
        plot((1:t)',[train_accuracies;test_accuracies]')
        //plot(1:t,test_accuracies,c='b')
        xlabel('Epochs')
        ylabel('Accuracy')
        title('Train & Test Accuracy')
        ha=legend(['train accuracy';'test accuracy']');
    end
    
    // Callback
    if test_accuracy >= 0.95
        break
    end
    
    t = t+1
end











