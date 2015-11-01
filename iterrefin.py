import numpy as np

def iterative_refinement( S , V , N , k = 10):
	V = V
	Vx = np.array([ i for i in range(N) if i not in V ])
	Vf = np.array([ -1 for i in range(len(V)) ] )
	while not np.all(V == Vf ):
		Vf = V
		avg = S[ V[ : , None ], V ].sum( axis = 1 )
		Vsort = V[ avg.argsort()[ : : -1] ]	
		V = Vsort[ : -k ]
		Vx = np.concatenate( ( Vx , Vsort[ -k : ] ) )
		Vx.sort()
		avg = S[Vx[ : , None ] , V ].sum( axis =1 )
		Vxsort = Vx[ avg.argsort() ]
		Vx = Vxsort[ : -k ]
		V = np.concatenate( ( V , Vx[ -k  : ] ) )
		V.sort()
	return Vf 



