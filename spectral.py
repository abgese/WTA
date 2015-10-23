import numpy as np
import pandas as pd
import scipy as sp
from scipy.stats import pearsonr
from numpy.linalg import eig

def read_data():
	data = pd.read_csv("u.tsv",delimiter='\t')
	return data

def RatingMatrix( data ):
	m = len(data.groupby('User').aggregate('count'))
	n = len(data.groupby('Movie').aggregate('count'))
	R = np.zeros((m,n))
	for i in data.index:
		u = data.User[i]
		m = data.Movie[i]
		R[u-1][m-1]=data.Rating[i]

	return R

def SimilarityMatrix( R ):
	m = len(R)
	S = np.zeros((m,m))
	for i in range(m):
		for j in range(i+1,m):
       			 S[i][j],_ = pearsonr(R[i],R[j])
       			 S[j][i] = S[i][j]
	return S

def Spectral( S , V ):
    values,vectors = eig(S)
    vect = vectors[:,values.argsort()[1]]
    V1=[]
    V2=[]
    for i in range(len(vect)):
        if(vect[i] < 0):
            V1.append(V[i])
        else:
            V2.append(V[i])
    return V1,V2


