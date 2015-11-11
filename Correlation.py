import numpy as np


def cos_cor( x , y ):
	x2 = np.sum(x**2)
	y2 = np.sum(y**2)
	ans = np.sum(x*y)
	ans = ans/(x2**(0.5))
	ans = ans/(y2**(0.5))
	return ans

def pears_cor( x , y ):
	x1 = x[ np.logical_and( ( x != 0 ) , ( y != 0 ) ) ]
	y1 = y[ np.logical_and(x!=0,y!=0) ]
	ans = 0
	if( len(x1) > 0 ):
		avgx = np.average( x1 )
		avgy = np.average( y1 )
		if( np.all( x == avgx ) ):
			avgx  = avgx - 0.0001
		if( np.all( y == avgy ) ):
			avgy = avgy - 0.0001
		scale = avgx / float(avgy)
		if( scale > 1 ):
			scale = 1 / scale
		xarr = x1 - avgx
		yarr = y1 - avgy
		numerator = np.sum( xarr*yarr )
		denominator = ( ( np.sum(xarr**2) )**0.5 )*( ( np.sum(yarr**2) )**0.5 )
		if(denominator != 0):
			ans = scale*numerator/denominator

	return ans




