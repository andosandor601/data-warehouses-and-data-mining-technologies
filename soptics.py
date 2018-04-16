import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from priority_heap import UpdatablePriorityQueue
from rand_pro_neighs_densities import RandProNeighsAndDensities

undefinedDist = -0.1

class SOptics:
	def run(this, points, minPts):
		if len(points)==0:
			return
		this.points=points	
		this.N = len(points)
		this.reachDist = this.N * [undefinedDist];
	

		algo = RandProNeighsAndDensities(points,minPts)
		this.ptIndex = algo.computeSetsBounds() 	
		this.inverseDensities = algo.computeAverageDistInSet()
		this.neighs = algo.getNeighs()	

		this.iorder=0
		this.processed  = this.N * [False]
		this.order = this.N * [0]
		for ipt in range(0, this.N): 
			if not this.processed[ipt]:
				this.expandClusterOrder(ipt)

		
	def expandClusterOrder(this, ipt) :
		heap = UpdatablePriorityQueue()
		heap.add(ipt, 1e6)
		while(not heap.isEmpty()):
			currPt = heap.pop()
			this.order[this.iorder]=currPt
			this.iorder += 1
			this.processed[currPt]=True	
			coredist=this.inverseDensities[currPt]

			for iNeigh in this.neighs[currPt]:
				if (this.processed[iNeigh]):
					continue
				nrdist = np.linalg.norm(this.points[iNeigh] - this.points[currPt])		
				if (coredist>nrdist):	
					nrdist=coredist  	 
				if (this.reachDist[iNeigh]==undefinedDist):
					this.reachDist[iNeigh]=nrdist
				elif (nrdist< this.reachDist[iNeigh]):
					this.reachDist[iNeigh]=nrdist
				heap.add(iNeigh, nrdist)



df=pd.read_csv('magic04.data', sep=',',header=None)
df = df[:100]

soptics = SOptics()
soptics.run(df.values, 5)

plt.plot(soptics.order, soptics.reachDist, lw=2)
plt.show()





