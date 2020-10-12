import numpy as np
import math

class Adaline:


    def __init__(self,d,xi,n_muestras,wi,fac_ap,w_ajustado):
            self.d = d
            self.xi = xi
            self.n_muestras = n_muestras
            self.wi = wi
            self.fac_ap = fac_ap
            self.y = 0 # salida de la red
            self.w_ajustado = w_ajustado
    
    def fit (self):
        self.errors = []
        self.cost = []
        output = self.net_input(self.xi)
        errors = self.y - output
        self.wi[1:] += self.fac_ap * self.xi.T.dot(errors)
        self.wi[0] += self.fac_ap * errors.sum()
        cost = (errors**2).sum() / 2.0
        self.cost.append(cost)
        return [cost,self.wi]
    def net_input(self, X):
        return np.dot(X, self.wi[1:]) + self.wi[0]
    def activation(self, X):
        return self.net_input(X)
    def predict(self, X):
        res =  np.where(self.activation(X) >= 0.0, 1, 0)
        return res
    # def Entrenamiento(self, E_total):
    #     E_ac = 0 # error actual
    #     for i in range(self.n_muestras):
    #         self.y = sum(self.xi[i,:] * self.wi) # calculo de la salida de la red
    #         E_ac = (self.d[i] - self.y) # calculo del error
    #         self.wi = self.wi +( self.fac_ap * E_ac * self.sigma(self.y) * (1 - self.sigma(self.y)) * self.xi[i,:])

    #         E_total = E_total + ((E_ac)**2)
        
    #     return E_total, self.wi
    
    # def sigma(self,y):
    #     return 1 / (1 + math.exp(-y))