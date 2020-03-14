data = csvRead('Iris.csv',[],[],'string')

dataNew = data(2:151,2:6)

c1 = dataNew(1:150,5) == 'Iris-setosa'
c2 = dataNew(1:150,5) == 'Iris-versicolor'
c3 = dataNew(1:150,5) == 'Iris-virginica'

temp = csvRead('Iris.csv')
temp = temp(2:151,2:5)
temp(1:150,5) = c1
temp(1:150,6) = c2
temp(1:150,7) = c3

data = temp
X = data(:,1:4)'
y = data(:,5:7)'

[X, y] = ann_pat_shuffle(X, y)

split = size(X)(2)*0.7
X_train = X(:,1:split)
y_train = y(:,1:split)

X_test = X(:,split+1:size(X)(2))
y_test = y(:,split+1:size(X)(2))

N = [4 16 3] // [4 16 3] - 97.77 lp=0.1 epochs-20

W = ann_FF_init(N)

lp = [0.3,0.000001]
T = 100
t = 1

train_losses = []
test_losses = []

train_accuracies = []
test_accuracies = []

while t<=T
    W_updated = ann_FF_Std_online(X_train, y_train, N, W, lp, 1)

    //W_updated = ann_FF_Std_batch(X_train, y_train, N, W, lp, 1)
    W = W_updated
    
    y_train_predicted = ann_FF_run(X_train, N, W)
    y_test_predicted = ann_FF_run(X_test, N, W)
    
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
    
    if test_accuracy >= 0.98
        break
    end
    
    t = t+1
end









