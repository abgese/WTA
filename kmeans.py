import numpy as np
import pandas as pd
import scipy as sp
from scipy.stats import pearsonr
from numpy.linalg import eig
from iterrefin import iterative_refinement

def read_data() :
	data = pd.read_csv( "Real_Users.csv")
	return data

def SimilarityMatrix( R ) :
	m = len( R )
	S = np.zeros( ( m , m ) )
	for i in range( m ) :
		for j in range( i , m ) :
       			 S[ i ][ j ] , _ = pearsonr( R[ i ] , R[ j ] )
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
	tot = np.sum( S1 )
	avg = tot / np.size( S1 )
	return avg

def main():
	print "Reading data..."
	data = read_data()
	print "Creating Rating matrix...."
	R = data.as_matrix()
	print "Creating Similarity matrix....."
	S = SimilarityMatrix( R )
	V = np.array( [ i for i in range( len( R ) ) ] )
	maxsim = []
	maxsimi = []
	print "Kmeans clustering......"
	for n in range( 2 , 900 ) :
		sim = 0
		Stack = []
		maxV = []
		Stack.append(V)
		flag = True
		while( len( Stack ) > 0 ) :
			Vnew = Stack.pop()
			V1 , V2 = Kmeans( R , Vnew)
			if( len( V1 ) > 0 ) :
				if( len(V1) > n - 10 and len( V1 ) < n + 10 )  :
					avg1 = AvgSim( S , V1 )
					if( sim < avg1 or ( len(maxV) <= n - 10 and len(maxV) > 0 ) ):
						maxV = V1
						sim = avg1
						flag = False
				elif( len(V1) >= n):
					Stack.append( V1 )
				else:
					if( len(V1) > len(maxV) ):
						avg1 = AvgSim( S , V1 )
						maxV = V1
						sim = avg1

			if( len( V2 ) > 0 ) :
				if( len( V2 ) > n - 10 and len( V2 ) < n + 10 ) :
					avg2 = AvgSim( S , V2 )
					if( sim < avg2 or (len(maxV) <= n - 10 and len(maxV) > 0) ):
						maxV = V2
						sim = avg2
						flag = False
				elif(len(V2) >= n):
					Stack.append( V2 )
				else :
					if( len( V2 ) >	len( maxV) ):
						avg2 = AvgSim( S , V2 )
						maxV = V2
						sim =avg2


			if( flag ) :
				if( len(V1) < n and len(V1) > 0): 
					avg1 = AvgSim( S , V1 )
					if( sim < avg1 ):
						maxV = V1
						sim = avg1
				if( len(V2) < n and len(V2) > 0 ): 
					avg2 = AvgSim( S , V2 )
					if( sim < avg2 ):
						maxV = V2
						sim = avg2
		if( n > 4 ) :
			maxVi = iterative_refinement( S , maxV , len(R) , int(0.75*len(maxV))  )
			maxsimi.append( AvgSim( S , maxVi ) )
		else:
			maxVi = maxV
			maxsimi.append( sim )
		maxsim.append( sim )
		print str(n)+" "+str(len(maxVi))
	Final = pd.DataFrame( data = {"GroupSize" : [ i for i in range( 2 , 900 ) ] , "Maximal Similarity" : maxsim , "Maximal Similarity(Refined) " : maxsimi } )	
	Final.to_csv("RealUsers_Kmeans.csv")


if __name__ == "__main__" : main()