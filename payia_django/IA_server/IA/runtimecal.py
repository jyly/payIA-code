# -*- coding: utf-8 -*-
import time
import timefilter
from os import listdir
import os
import datafilt 
from sklearn.externals import joblib
from sklearn import svm

title=listdir('./tempdata/wechat/tzh/') 
for i in range(0,10):#遍历不同时间的文件
	readpath='./tempdata/wechat/tzh/'+title[i]
	writepath='./final/wechat/tzh/'+title[i]
	print(readpath)
	receivetime=int(round(time.time() * 1000))
	print (receivetime)

	timefilter.timewrap(readpath,writepath,20)


	upstart,upstop,tempuserdata=datafilt.dataextra(writepath)
	tempdata=[[] for i in range(6)]
	for i in range(0,6):
		tempdata[i]=datafilt.kalman(tempuserdata[i])
	userdata=[[[] for i in range(6)],[[] for i in range(6)]]
	for i in range(6):
		userdata[0][i]= tempdata[i][upstart:upstop]
		userdata[1][i]= tempdata[i][upstop:upstop+150]

	i=0
	tempfeature=[]
	while i<6:
		filtdata=userdata[0][i]
		feature=datafilt.extrafeature(filtdata)
		for k in feature:
			tempfeature.append(k)
		filtdata=userdata[1][i]
		feature=datafilt.extrafeature(filtdata)
		for k in feature:
			tempfeature.append(k)	
		i=i+1	
	# # print(len(testdata))
	# 30
	# indexnum=[72, 42, 44, 52, 54, 32, 34, 22, 24, 92, 70, 25, 46, 21, 23, 94, 20, 40, 91, 93, 75, 71, 10, 80, 87, 30, 88, 73, 95, 0]
	# 20
	# indexnum=[72, 42, 44, 52, 54, 32, 34, 22, 24, 92, 70, 25, 46, 21, 23, 94, 20, 40, 91, 93]
	# 58
	indexnum=[72, 42, 44, 52, 54, 32, 34, 22, 24, 92, 70, 25, 46, 21, 23, 94, 20, 40, 91, 93, 75, 71, 10, 80, 87, 30, 88, 73, 95, 0, 43, 89, 27, 12, 82, 112, 7, 13, 102, 14, 101, 45, 38, 5, 41, 66, 37, 86, 77, 50, 31, 98, 99, 57, 8, 60, 96, 74]
	

	featurecom=[[]]
	for i in indexnum:
		featurecom[0].append(tempfeature[i])
	lda=joblib.load('D:/IA_server/IA/lda.pkl')
	featurecom=lda.transform(featurecom)
	# print(featurecom)

	clf=joblib.load('D:/IA_server/IA/svmmodel.pkl')
	pretarget=clf.predict_proba(featurecom)
	print (pretarget)

	outtime=int(round(time.time() * 1000))
	output_1=open('D:/IA_server/IA/log2.txt','a+')
	filein=str('tzh')+','+str('0')+','+str(receivetime)+','+str(outtime)+','+str((outtime-receivetime)/1000)+'\n'
	output_1.write(filein)
	output_1.close()
	print (filein)