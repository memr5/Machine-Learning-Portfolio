x1 = [0 0 1 1]
x2 = [0 1 0 1]

yand = x1.*x2

yor = bitor(x1,x2)

x3 = [0 1]
ynot = bitcmp(x3,1)

figure(1)
scatter(x1,x2,500,yand,"fill")
title("AND")

figure(2)
scatter(x1,x2,500,yor,"fill")
title("OR")

figure(3)
scatter(x3,ynot,500,ynot,"fill")
title("NOT")
