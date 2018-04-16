import random
import numpy as np
from math import log, sqrt

logOProjectionConst = 20
DefaultRandSeed = 42
sizeTolerance = 2.0/3.0
undefinedDist = -0.1


class RandProNeighsAndDensities:
	def __init__(this, points, minSplitSize):
		this.points = points
		this.minSplitSize = minSplitSize
		this.N = len(points) 
		this.nDimensions = len(points[0])
		this.points = points
		
		this.nPointSetSplits = int(logOProjectionConst*log(this.N*this.nDimensions+1)/log(2)) 
		this.nProject1d = int(logOProjectionConst*log(this.N*this.nDimensions+1)/log(2)) 

		np.random.seed(DefaultRandSeed)


	def computeSetsBounds(this):
		this.splitsets = []
		
		this.projectedPoints = np.zeros([this.nProject1d, this.N])	
	
		for j in range(0, this.nProject1d):
			S =0
			currRp = np.random.rand(this.nDimensions) - 0.5
			S +=sum(currRp * currRp)				

			S = sqrt(S)
			currRp /= S							

			k=0
			for vecPt in this.points:
				this.projectedPoints[j][k] = sum(currRp*vecPt[:this.nDimensions])	
				k += 1

		proind = range(0, this.nProject1d)
		for avgP in range(0, this.nPointSetSplits):
			tmpPro = this.projectedPoints[0:this.nProject1d]		
			random.shuffle(proind)
			this.projectedPoints[proind]=tmpPro
			 
		   	ind = np.array(range(0, this.N))
			this.splitupNoSort(ind,0)


	def splitupNoSort(this, ind, dim):
		nele = len(ind)
		dim = dim % this.nProject1d
		tpro = this.projectedPoints[dim]
	  
		if (nele > this.minSplitSize*(1-sizeTolerance)  and nele < this.minSplitSize*(1+sizeTolerance)):
			cpro =tpro[ind]
			ind = np.argsort(cpro)
			this.splitsets.append(ind)

		if (nele > this.minSplitSize ):
			randInd = random.randint(0, nele - 1)
			rs = tpro[ind[randInd]]
			minInd = 0
			maxInd = nele-1

			while (minInd < maxInd):
				currEle=tpro[ind[minInd]]		  
				if currEle>rs:
					while (minInd<maxInd and tpro[ind[maxInd]]>rs):
						  maxInd -= 1
					if (minInd==maxInd):
						break
					currInd=ind[minInd]
					ind[minInd]=ind[maxInd]
					ind[maxInd]=currInd
					maxInd -= 1			  
				minInd += 1
			if minInd==nele-1:
				minInd=nele/2
			  			  
			splitpos = minInd+1
			ind2=range(0, splitpos)
			ind2 = ind[ind2]
			this.splitupNoSort(ind2, dim+1)
			
			ind2= np.array(range(0, nele - splitpos)) + splitpos
			ind2 = ind[ind2]
			this.splitupNoSort(ind2,dim+1)


	def computeAverageDistInSet(this):
		davg = np.zeros(this.N);
		nDists = np.zeros(this.N);	
		for pinSet in this.splitsets:
			length = len(pinSet)   	
			indoff = int(round(length/2))
			oldind = pinSet[indoff];
			for ind in pinSet:
				if (ind==indoff):
					continue;
				dist = np.linalg.norm(this.points[ind] - this.points[oldind]);
				davg[oldind] += dist;
				nDists[oldind] += 1;
				davg[ind] += dist;
				nDists[ind] += 1;

		for l in range(0, this.N):
			if nDists[l] == 0: 
				davg[l] = undefinedDist;
			else:
				davg[l] /= nDists[l];
		return davg;


	def getNeighs(this):
		neighs = [];
		for l in range(0, this.N):  	
			neighs.append([]);
		
		for pinSet in this.splitsets:
			length = len(pinSet)   	
			indoff = int(round(length/2))
			oldind = pinSet[indoff];
			
			for ind in pinSet:
				cneighs=neighs[ind];
				cnLenght = len(cneighs)
				pos = np.searchsorted(cneighs, oldind);
				if (pos == cnLenght): 
					cneighs.append(oldind)

				if (pos < cnLenght) and (cneighs[pos] != oldind):	
					cneighs.insert(pos-1, oldind);							

				cneighs2=neighs[oldind];	
				cnLenght2 = len(cneighs2)				
				pos = np.searchsorted(cneighs2, ind);
				if (pos == cnLenght2):
					cneighs2.append(ind);

				if (pos < cnLenght2) and (cneighs2[pos] != ind):
					cneighs2.insert(pos-1, ind)	

		return neighs;
