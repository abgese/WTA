import numpy as np
import pandas as pd
import scipy as sp
from scipy.stats import pearsonr
from numpy.linalg import eig

def read_data() :
	data = pd.read_csv( "u.tsv" , delimiter= '\t' )
	return data

def RatingMatrix( data ) :
	m = len( data.groupby( 'User' ).aggregate( 'count' ) )
	n = len( data.groupby( 'Movie' ).aggregate( 'count' ) )
	R = np.zeros( ( m , n ) )
	for i in data.index :
		u = data.User[ i ]
		m = data.Movie[ i ]
		R[ u - 1 ][ m - 1 ]=data.Rating[ i ]

	return R

def SimilarityMatrix( R ) :
	m = len( R )
	S = np.zeros( ( m , m ) )
	for i in range( m ) :
		for j in range( i+1 , m ) :
       			 S[ i ][ j ] , _ = pearsonr( R[ i ] , R[ j ] )
       			 S[ j ][ i ] = S[ i ][ j ]
	return S

def Kmeans( R , V ) : 

def AvgSim( S , V ):
	S1 = S[ V[ : , None] , V ]
	tot = np.sum( S1 )
	avg = tot / np.size( S1 )
	return avg

def main():
	n = 50
	data = read_data()
	R = RatingMatrix( data )
	S = SimilarityMatrix( R )
	V = np.array( [ i for i in range( len( R ) ) ] )
	Stack = []
	maxV = []
	maxsim = 0
	Stack.append(V)
	while( len( Stack ) > 0 ) :
		Vnew = Stack.pop()
		V1 , V2 = Kmeans( R , Vnew)
		if( len( V1 ) < n ) :
			avg1 = AvgSim( S , V1 )
			if( maxsim < avg1 ):
				maxV = V1
				maxsim = avg1
		else :
			Stack.append( V1 )
		if( len( V2 ) < n ) :
			avg2 = AvgSim( S , V2 )
			if( maxsim < avg2 ):
				maxV = V2
				maxsim = avg2
		else :
			Stack.append( V2 )
	print maxsim
	print maxV


if __name__ == "__main__" : main()

