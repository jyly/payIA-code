# _*_ coding: utf-8 _*_
from minepy import MINE
from math import log
def mulinform(data,target):
	comdata=[]
	for i in range(0,len(data[0])):
		comdata.append([])
		for j in range(len(data)):
			comdata[i].append(data[j][i])
	micnum=[]	
	m = MINE()
	for i in range(0,len(comdata)):
		m.compute_score(comdata[i],target)
		micnum.append(m.mic())   #得出不同特征的互信息值
	return micnum

def NMI(A,B):
	A=np.array(A)
	B=np.array(B)
	# len(A) should be equal to len(B)
	total = len(A)
	A_ids = set(A)
	B_ids = set(B)
	#Mutual information
	MI = 0
	eps = 1.4e-45
	for idA in A_ids:
		for idB in B_ids:
			idAOccur = np.where(A==idA)
			idBOccur = np.where(B==idB)
			idABOccur = np.intersect1d(idAOccur,idBOccur)
			px = 1.0*len(idAOccur[0])/total
			py = 1.0*len(idBOccur[0])/total
			pxy = 1.0*len(idABOccur)/total
			MI = MI + pxy*math.log(pxy/(px*py)+eps,2)
	# Normalized Mutual information
	Hx = 0
	for idA in A_ids:
		idAOccurCount = 1.0*len(np.where(A==idA)[0])
		Hx = Hx - (idAOccurCount/total)*math.log(idAOccurCount/total+eps,2)
	Hy = 0
	for idB in B_ids:
		idBOccurCount = 1.0*len(np.where(B==idB)[0])
		Hy = Hy - (idBOccurCount/total)*math.log(idBOccurCount/total+eps,2)
	# MIhat = 2.0*MI/(Hx+Hy)
	MIhat = (Hx+Hy-MI)
	# print Hx,Hy,MI,MIhat   
	MIhat = MIhat/Hy
	# print MIhat   
	return MIhat