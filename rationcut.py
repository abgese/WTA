import numpy as np

def RationCut( S ) :
	N = len( S )
	davg =  150
	density = np.empty( N )
	Rank = np.empty( N )
	Degree = np.empty( N )
	for i in range( N ) :
		vec = S[ i ]
		vec.sort()
		vec = vec[ : : -1 ]
		vec = vec[ : 30 ]
		density[ i ] = np.sum( vec )
	
	for i in range( N ) :
		Rank[ i ] = ( np.sum( ( density <= density[ i ] ) ) )/float( N )
		Degree[ i ] = round( davg*( Rank[ i ] + 0.5 ) )
		vec = S[ i ].argsort()[ : : -1]
		vec = vec[ Degree[ i ] : ]
		for j in vec :
			S[ i ][ j ] = 0
	return S


