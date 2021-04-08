# _*_ coding: utf-8 _*_
from os import listdir
import numpy as np 


def fisher_criterion(v1, v2, num): #特征列1，目标列2，用户数
	userchardata=[]
	for i in range(0,num):
		userchardata.append([])
	for i in range(0,len(v2)):
		userchardata[v2[i]-1].append(v1[i])
	inter_class=0
	intra_class=0
	ave=np.average(v1)
	for i in range(0,num):
		inter_class=inter_class+len(userchardata[i])*(np.average(userchardata[i])-ave)**2
		intra_class=intra_class+len(userchardata[i])*(np.var(userchardata[i]))**2
		# print 	inter_class,intra_class
	return (inter_class)/(intra_class)

def compute_fisher(data,target,num):
	comdata=[]
	for i in range(0,len(data[0])):
		comdata.append([])
		for j in range(len(data)):
			comdata[i].append(data[j][i])
	fisherscore=[]		
	for i in range(0,len(comdata)):
		fisherscore.append(fisher_criterion(comdata[i],target,num))
	return fisherscore
