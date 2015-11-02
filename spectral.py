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
		for j in range( i , m ) :
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
	print "Reading data..."
	data = read_data()
	print "Creating Rating matrix...."
	R = RatingMatrix( data )
	print "Creating Similarity matrix....."
	S = SimilarityMatrix( R )
	V = np.array( [ i for i in range( len( R ) ) ] )
	maxsim = []
	maxsimi = []
	print "Spectral clustering......"
	for n in range( 2 , len( R ) - 1 ):
		print n
		sim = 0
		Stack = []
		maxV = []
		Stack.append( V )
		while( len( Stack ) > 0 ) :
			Vnew = Stack.pop()
			V1 , V2 = Spectral( S , Vnew )
			if( len(V1) > 0 ) :
				if( len( V1 ) < n ) :
					avg1 = AvgSim( S , V1 )
					if( sim < avg1 ):
						maxV = V1
						sim = avg1
				else :
					Stack.append( V1 )
			if( len( V2 ) > 0 ) :
				if( len( V2 ) < n ) :
					avg2 = AvgSim( S , V2 )
					if( sim < avg2 ):
						maxV = V2
						sim = avg2
				else :
					Stack.append( V2 ) 
		if( n > 4 ) :
			maxVi = iterative_refinement( S , maxV , len(R) , int(0.75*len(maxV))  )
			maxsimi.append( AvgSim( S , maxVi ) )
		else:
			maxVi = maxV
			maxsimi.append( sim )
		maxsim.append( sim )
	Final = pd.DataFrame( data = {"GroupSize" : [ i for i in range( 2 , len( R ) - 1 ) ] , "Maximal Similarity" : maxsim , "Maximal Similarity(Refined) " : maxsimi } )	
	Final.to_csv("RealUsers_Spectral.csv")
if __name__ == "__main__" : main()
