import numpy as np

def iterative_refinement( S , V , N , k = 10):
	if k > 10 :
		k = 10
	Vx = np.array([ i for i in range(N) if i not in V ])
	Vf = np.array([ -1 for i in range(len(V)) ] )
	while not np.all(V == Vf ):
		Vf = V
		for i in range(k):
			avg = S[ Vx[ : , None ], V ].sum( axis = 1 )
			Vxsort = Vx[ avg.argsort() ]
			Vx = Vxsort[ : -1 ]
			V = np.append(V,Vx[ -1 : ])
		for i in range(k):
			avg = S[ V[ : , None ] , V ].sum( axis = 1 )
			Vsort =V[ avg.argsort()[ : : -1 ] ]
			V = V[ : -1 ]
			Vx = np.append( Vx , V[ -1 : ])
		V.sort()
		Vx.sort()
	return Vf 



