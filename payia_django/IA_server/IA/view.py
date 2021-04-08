# -*- coding: utf-8 -*-
from django.http import HttpResponse
import numpy as np
import json
from sklearn.externals import joblib
from sklearn import svm
from django.http import JsonResponse
from ast import literal_eval
import time
from . import timefilter
import os
import logging
from . import datafilt 
# from datetime import datetime


dirpath=os.getcwd()+'/data/'
dirpath=dirpath.replace('\\','/')

def hello(request):
	print(dirpath)
	return HttpResponse("welecome to use the django service !")

def checkdir(uid,tag,time):
	print (uid,tag,time)
	
	isExists=os.path.exists(dirpath)
	if not isExists:
		os.makedirs(dirpath) 

	filepath=dirpath+tag+'/'
	if not os.path.exists(filepath):
		os.makedirs(filepath)
		
	filepath=dirpath+uid+'/'
	isExists=os.path.exists(filepath)
	if not isExists:
		os.makedirs(filepath) 
	filepath=filepath+time+'.csv'
	return filepath

def IA(request):

	logger = logging.getLogger('log')

	obj = request.FILES.get("sensor")
	print (obj)
	logger.info(obj)

	str1={}
	if obj:
		data=obj.name
		print(data)
		data=literal_eval(data)
		data['id']=data['id'].replace(' ','')
		print(data['id'],data['apptag'],data['time'])

		filepath=checkdir(data['id'],data['apptag'],data['time'])
		f = open(readpath,'wb')
		for line in obj.chunks():
			f.write(line)
		f.close()
		receivetime=int(round(time.time() * 1000))

		

		str1[data['id']]=['true']
		outtime=int(round(time.time() * 1000))
		output_1=open(os.getcwd().replace('\\','/')+'log.txt','a+')
		filein=str(data['id'])+','+str(data['apptag'])+','+str(receivetime)+','+str(outtime)+','+str((outtime-receivetime))+'\n'

		print (filein)
		logger.info(filein)

		output_1.write(filein)
		output_1.close()
		# print(str)

		return JsonResponse(str1)
	else:
		return HttpResponse("IA")

		# timefilter.timewrap(readpath,writepath,20)
		# upstart,upstop,tempuserdata=datafilt.dataextra(writepath)
		# tempdata=[[] for i in range(6)]
		# for i in range(0,6):
		# 	tempdata[i]=datafilt.kalman(tempuserdata[i])
		# userdata=[[[] for i in range(6)],[[] for i in range(6)]]
		# for i in range(6):
		# 	userdata[0][i]= tempdata[i][upstart:upstop]
		# 	userdata[1][i]= tempdata[i][upstop:upstop+150]

		# i=0
		# tempfeature=[]
		# while i<6:
		# 	filtdata=userdata[0][i]
		# 	feature=datafilt.extrafeature(filtdata)
		# 	for k in feature:
		# 		tempfeature.append(k)
		# 	filtdata=userdata[1][i]
		# 	feature=datafilt.extrafeature(filtdata)
		# 	for k in feature:
		# 		tempfeature.append(k)	
		# 	i=i+1	
		# # # print(len(testdata))
		# indexnum=[42, 44, 2, 22, 24, 43, 1, 23, 112, 45, 40, 25, 21, 54, 52, 32, 34, 20, 0, 46, 111, 66, 94, 99, 98, 70, 72, 102, 77, 62, 113, 63, 118, 61, 114, 93, 33, 65, 64, 35, 119, 41, 31, 95, 115, 36, 82, 30, 60, 80, 10, 97, 71, 27, 81, 11, 51, 100, 58, 50]

		# featurecom=[[]]
		# for i in indexnum:
		# 	featurecom[0].append(tempfeature[i])
		# lda=joblib.load('D:/IA_server/IA/lda.pkl')
		# featurecom=lda.transform(featurecom)
		# # print(featurecom)

		# clf=joblib.load('D:/IA_server/IA/svmmodel.pkl')
		# pretarget=clf.predict_proba(featurecom)
		# print (pretarget)
		# user=['tzh','djb','zzc','ln','ygy']
		# td=0
		# for i in user:
		# 	if data['id']==i:
		# 		break
		# 	else:
		# 		td=td+1
		# print(td)			
		# if pretarget[0][td]>0.1:
		# 	str1[data['id']]=['true']
		# else:
		# 	str1[data['id']]=['false']
