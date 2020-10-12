import numpy as np 
import math 
class AdalineGD(object):
    def __init__(self,n, eta = 0.01, n_iter = 50):
        self.eta = eta
        self.n_iter = n_iter
        self.w_ = np.random.uniform(-1,1,n)
        self.cost_ = []

    def fit2(self,X,y):
        for x,y in zip(X,y):
            output = self.sigmoide(x)
            error = y - output
            cost  =  error**2
            self.w_ +=  self.eta * error* output *(1-output)*x
        return(self.w_,cost)
    def eval(self,datos):
        return sum(dato*weigth for dato,weigth in zip(datos,self.w_))
    def sigmoide(self,X):
        return 1/(1+math.e**(-(self.eval(X))))