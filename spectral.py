import numpy as np
import pandas as pd
import scipy as sp
from scipy.stats import pearsonr
from numpy.linalg import eig
from iterrefin import iterative_refinement

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

def Laplacian( S ) :
    d = np.sum( S , axis = 1)
    L = S * -1
    for i in range( len( d ) ) :
        L[ i ][ i ] = L[ i ][ i ] + d[ i ]
    return L



def Spectral( S , V ):
	S1 = S[ V[ : , None ] , V ]
	L = Laplacian( S1 )
	values , vectors = eig( L )
	vect = vectors[ : , values.argsort( )[ 1 ] ]
	V1=[]
	V2=[]
	for i in range( len( vect ) ) :
	    if( vect[ i ] < 0 ) : 
	        V1.append( V[ i ] )
	    else:
	        V2.append( V[ i ] )
	return np.array( V1 ),np.array( V2 )

def AvgSim( S , V ):
	S1 = S[ V[ : , None] , V ]
	tot = np.sum( S1 )
	avg = tot / np.size( S1 )
	return avg

def main():
	n = 50
	print "Reading data..."
	data = read_data()
	print "Creating Rating matrix...."
	R = RatingMatrix( data )
	print "Creating Similarity matrix....."
	S = SimilarityMatrix( R )
	V = np.array( [ i for i in range( len( R ) ) ] )
	Stack = []
	maxV = []
	maxsim = 0
	Stack.append(V)
	print "Spectral clustering......"
	while( len( Stack ) > 0 ) :
		Vnew = Stack.pop()
		V1 , V2 = Spectral( S , Vnew)
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
	print "Iterative Refinement..."
	maxVi = iterative_refinement( S , maxV , len(R) )
	maxsimi = AvgSim( S , maxVi )
	print maxsim
	print maxV
	print maxsimi
	print maxVi


if __name__ == "__main__" : main()
