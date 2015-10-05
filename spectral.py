import numpy as np
import pandas as pd
import scipy as sp

def read_data():
	data = pd.read_csv("u.tsv",delimiter='\t')
	return data

def RatingMatrix( data ):
	R = np.zeros((943,1682))
	for i in data.index:
		u = data.User[i]
		m = data.Movie[i]
		R[u-1][m-1]=data.Rating[i]

	return R

def SimilarityMatrix( R ):
	return S


