import numpy as np
import pandas as pd
import scipy as sp
from scipy.stats import pearsonr
from numpy.linalg import svd
from iterrefin import iterative_refinement
from rationcut import RationCut
from Correlation import cos_cor,pears_cor

def read_data( filename ) :
	data = pd.DataFrame.from_csv('Data/'+filename )
	return data
	
def SimilarityMatrix( R ) :
	m = len( R )
	S = np.zeros( ( m , m ) )
	for i in range( m ) :
		for j in range( i , m ) :
       			 S[ i ][ j ]  = pears_cor( R[ i ] , R[ j ] )
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
	S1 = RationCut( S1 )
	L = Laplacian( S1 )
	vectors , values , _ = svd( L )
	vect = vectors[ : , values.argsort( )[ 1 ] ]
	V1 = []
	V2 = []
	for i in range( len( vect ) ) :
	    if( vect[ i ] < 0 ) : 
	        V1.append( V[ i ] )
	    else:
	        V2.append( V[ i ] )
	return np.array( V1 ),np.array( V2 )

def AvgSim( S , V ):
	avg = 0
	if len( V ) > 0:
		S1 = S[ V[ : , None] , V ]
		avg = np.average( S1 )
	return avg


def main():
	inp = ["Real_Users.csv" , "RandomAttack.csv" , "AverageAttack.csv" , "BandwagonAttack.csv" ]
	out = ["RealUsers_Spectral.csv","RandomAttack_Spectral.csv","AverageAttack_Spectral.csv","BandwagonAttack_Spectral.csv"]
	for ctr in range(4):
		print "Reading data... "+inp[ctr]+" "+out[ctr]
		data = read_data( inp[ctr] )
		print "Creating Rating matrix...."
		R = data.as_matrix()
		print "Creating Similarity matrix....."
		S = SimilarityMatrix( R )
		V = np.array( [ i for i in range( len( R ) ) ] )
		maxsim = []
		maxsimi = []
		print "Spectral clustering......"
		for n in range( 2 , 900 ):
			sim = 0
			Stack = []
			maxV = []
			Stack.append(V)
			flag = False
			while( len( Stack ) > 0 ) :
				Vnew = Stack.pop()
				V1 , V2 = Spectral( S , Vnew)
				if( len(V1) == 0 and len(maxV) == 0):
					maxV = V2
					sim = AvgSim( S , V2 )
					flag = True
				if( len(V1) < n ):
					if( (AvgSim( S , V1 ) > sim and len( V1 ) > n/2) or flag ):
						maxV = V1
						sim = AvgSim( S , V1 )
						flag = False
				elif(len(V1) != len(Vnew)):
					Stack.append( V1 )
				if( len( V2 ) < n):
					if( ( AvgSim(S , V2) > sim and len(V2) > n/2 ) or flag ):
						maxV = V2
						sim = AvgSim( S , V2 )
						flag = False
				elif(len(V2) != len(Vnew)):
					Stack.append( V2 )

			if( n > 4 ) :
				maxVi = iterative_refinement( S , maxV , len(R) , int(0.75*len(maxV))  )
				maxsimi.append( AvgSim( S , maxVi ) )
			else:
				maxVi = maxV
				maxsimi.append( sim )
			maxsim.append( sim )
			print str(n)+" "+str(len(maxVi))
		Final = pd.DataFrame( data = {"GroupSize" : [ i for i in range( 2 , 900 ) ] , "Maximal Similarity" : maxsim , "Maximal Similarity(Refined) " : maxsimi } )	
		Final.to_csv( 'Data/'+out[ ctr ] )
if __name__ == "__main__" : main()
