				Vnew = Stack.pop()
				V1 , V2 = Spectral( R , Vnew)
				if( len( V1 ) > 0 ) :
					if( len(V1) > n - 10 and len( V1 ) < n + 10 )  :
						avg1 = AvgSim( S , V1 )
						if( sim < avg1 or ( len(maxV) <= n - 10 and len(maxV) > 0 ) ):
							maxV = V1
							sim = avg1
							flag = False
					elif( len(V1) >= n and len(V1) < len(Vnew)):
						Stack.append( V1 )
					else:
						if( len(V1) > len(maxV) and len( V1 ) < n):
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
					elif(len(V2) >= n and len(V2) < len(Vnew) ):
						Stack.append( V2 )
					else :
						if( len( V2 ) >	len( maxV) and len( V2 ) < n ):
							avg2 = AvgSim( S , V2 )
							maxV = V2
							sim = avg2


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