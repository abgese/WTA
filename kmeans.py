import numpy as np
import pandas as pd
import scipy as sp
from scipy.stats import pearsonr
from numpy.linalg import svd
from iterrefin import iterative_refinement
from rationcut import RationCut
from Correlation import cos_cor,pears_cor

def read_data( filename ) :
	data = pd.DataFrame.from_csv( 'Data/'+filename )
	return data


def SimilarityMatrix( R ) :
	m = len( R )
	S = np.zeros( ( m , m ) )
	for i in range( m ) :
		for j in range( i , m ) :
       			 S[ i ][ j ] = pears_cor( R[ i ] , R[ j ] )
       			 S[ j ][ i ] = S[ i ][ j ]
	return S

def Kmeans( R , V ) : 
	k = 2
    	R1 = R[V]
    	centroids = []
    	centroids = np.array(randomize_centroids(R1, centroids, k))  
	old_centroids = [[] for i in range(k)] 
	iterations = 0
	while not (has_converged(centroids, old_centroids, iterations)):
		iterations = iterations + 1
		clusters = [[] for i in range(k)]
		clusters = euclidean_dist(R1, centroids, clusters)
		index = 0
		for cluster in clusters:
            		old_centroids[index] = centroids[index]
            		clusters[index] = np.array(clusters[index])
            		centroids[index] = R[clusters[index]].sum(axis=0)/len(clusters[index])
	            	index = index + 1
	
    	return np.array(clusters[0]) , np.array(clusters[1])

def euclidean_dist(R, centroids, clusters):
    	for i in range(len(R)):  
    		x = np.sum((R[i]-centroids[0])**2)
    	 	y = np.sum((R[i]-centroids[1])**2)
    		if x >= y :
    			clusters[0].append(i)
    		else :
    			clusters[1].append(i)
    	for i in range(len(clusters)):
    		if( not clusters[i] ):
    			clusters[i].append(np.random.randint(0,len(R),size=1)),	
    	return clusters


# randomize initial centroids
def randomize_centroids(R, centroids, k):
    	for cluster in range(0, k):
    	    centroids.append(R[np.random.randint(0, len(R), size=1)])
    	return centroids


# check if clusters have converged    
def has_converged(centroids, old_centroids, iterations):
   	MAX_ITERATIONS = 100000
   	if iterations > MAX_ITERATIONS:
   		return True
   	return np.all( old_centroids == centroids )

def AvgSim( S , V ):
	S1 = S[ V[ : , None] , V ]
	S1 = RationCut( S1 )
	tot = np.sum( S1 )
	avg = tot / np.size( S1 )
	return avg

def main():
	inp = ["Real_Users.csv","RandomAttack.csv","AverageAttack.csv","BandwagonAttack.csv"]
	out = ["RealUsers_Kmeans.csv","RandomAttack_Kmeans.csv","AverageAttack_Kmeans.csv","BandwagonAttack_Kmeans.csv"]
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
			flag = True
			while( len( Stack ) > 0 ) :
				print len(Stack)
				Vnew = Stack.pop()
				V1 , V2 = K( R , Vnew)
				if( len(V1) < n ):
					if( AvgSim(V1) > sim and len(V1) > 1):
						maxV = V1
						sim = AvgSim( V1 ) 
				elif(len(V1) != len(Vnew)):
					Stack.append( V1 )
				if( len( V2 ) < n):
					if( AvgSim(V2) > sim and len( V2 ) > 1):
						maxV = V2
						sim = AvgSim( V2 )
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
