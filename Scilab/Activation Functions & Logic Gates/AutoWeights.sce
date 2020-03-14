threshold = input("Enter the value of threshold: ")
bias = input("Enter the value of bias: ")

x1 = [0 0 1 1]
x2 = [0 1 0 1]
x = [x1' x2']
y = x1.*x2

while 1
    w = rand(2,1,"uniform")
    ypred = x*w + bias
    for i=1:4
        if ypred(i)>threshold then
            ypred(i) = 1
        else
            ypred(i) = 0
        end
    end
    
    if sum(ypred==y') == 4 then
        
end
