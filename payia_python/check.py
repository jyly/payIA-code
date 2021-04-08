# _*_ coding: utf-8 _*_
from os import listdir
import numpy as np 
from datafilt import kalman,meanfilt,savgol,std,minmax,wt,guass,extrafeature,dataextra
import json
from sklearn.externals import joblib
from sklearn import svm
from django.http import JsonResponse
from ast import literal_eval

user=['djb','zzc','ln','ygy']


alfar=[]
alfrr=[]
alacc=[]

# threshold=0.53
indexnum=[23, 25, 43, 45, 40, 21, 44, 42, 22, 24, 60, 12, 62, 20, 2, 14, 64, 63, 1, 34, 32, 66, 31, 94, 65, 99, 41, 98, 49, 11, 50, 26, 93, 0, 48, 69, 4, 47, 29, 35, 68, 102, 112, 95, 33, 10, 70, 28, 111, 13, 19, 75, 97, 91, 7, 18, 76, 15, 118, 54]
threshold=0.53

# while threshold<1:
alltp=0
alltn=0
allfp=0
allfn=0
for name in range(0,len(user)):#遍历不同的目录
	tp=0
	tn=0
	fp=0
	fn=0

	modeluser=['djb','hy','ln','tzh','ygy','yw','zzc','lxy','wql','ys','wc']	
	td=0
	for i in modeluser:
		if user[name]==i:
			break
		else:
			td=td+1
	print(td)			

	title=listdir('./attack/'+user[name]+'/') 
	for time in range(0,len(title)):#遍历不同时间的文件
		path='./attack/'+user[name]+'/'+title[time]
		# path='./data/alipay/'+user[name]+'/'+title[time]
		print(path)
		# userdata[name].append([])
		userdata=[[] for i in range(12)]

		upstart,upstop,tempuserdata=dataextra(path)
		tempdata=[[] for i in range(6)]
		for i in range(0,6):
			tempdata[i]=kalman(tempuserdata[i])
		userdata=[[[] for i in range(6)],[[] for i in range(6)]]
		for i in range(6):
			userdata[0][i]= tempdata[i][upstart:upstop]
			userdata[1][i]= tempdata[i][upstop:upstop+100]

		i=0
		tempfeature=[]
		while i<6:
			filtdata=userdata[0][i]
			feature=extrafeature(filtdata)
			for k in feature:
				tempfeature.append(k)
			filtdata=userdata[1][i]
			feature=extrafeature(filtdata)
			for k in feature:
				tempfeature.append(k)	
			i=i+1	

		featurecom=[[]]
		for i in indexnum:
			featurecom[0].append(tempfeature[i])
		lda=joblib.load('./lda.pkl')
		featurecom=lda.transform(featurecom)
		# print(featurecom)
		

		clf=joblib.load('./svmmodel.pkl')
		pretarget=clf.predict_proba(featurecom)
		# print (pretarget)

		if pretarget[0][td]>threshold:
			fp=fp+1
		else:
			tn=tn+1


	title=listdir('./origin/'+user[name]+'/') 
	for time in range(0,len(title)):#遍历不同时间的文件
		path='./origin/'+user[name]+'/'+title[time]
		# path='./data/alipay/'+user[name]+'/'+title[time]
		print(path)
		# userdata[name].append([])
		userdata=[[] for i in range(12)]
		upstart,upstop,tempuserdata=dataextra(path)
		tempdata=[[] for i in range(6)]
		for i in range(0,6):
			tempdata[i]=kalman(tempuserdata[i])
		userdata=[[[] for i in range(6)],[[] for i in range(6)]]
		for i in range(6):
			userdata[0][i]= tempdata[i][upstart:upstop]
			userdata[1][i]= tempdata[i][upstop:upstop+100]

		i=0
		tempfeature=[]
		while i<6:
			filtdata=userdata[0][i]
			feature=extrafeature(filtdata)
			for k in feature:
				tempfeature.append(k)
			filtdata=userdata[1][i]
			feature=extrafeature(filtdata)
			for k in feature:
				tempfeature.append(k)	
			i=i+1	



		featurecom=[[]]
		for i in indexnum:
			featurecom[0].append(tempfeature[i])
		lda=joblib.load('./lda.pkl')
		featurecom=lda.transform(featurecom)
		# print(featurecom)
		

		clf=joblib.load('./svmmodel.pkl')
		pretarget=clf.predict_proba(featurecom)
		# print (pretarget)
		
		if pretarget[0][td]>threshold:
			tp=tp+1
		else:
			fn=fn+1
	print (tp,tn,fp,fn)

	accuracy=float(tp+tn)/(tp+tn+fp+fn)
	FAR=float(fp)/(fp+tn)	
	FRR=float(fn)/(tp+fn)

	# alltp=alltp+tp
	# alltn=alltn+tn
	# allfp=allfp+fp
	# allfn=allfn+fn

# accuracy=float(alltp+alltn)/(alltp+alltn+allfp+allfn)
# FAR=float(allfp)/(allfp+alltn)	
# FRR=float(allfn)/(alltp+allfn)

	alacc.append(accuracy)
	alfar.append(FAR)
	alfrr.append(FRR)

threshold=threshold+0.02


print(alacc)	
print(alfar)	
print(alfrr)	
# print(np.mean(alacc),np.std(alacc))	
# print(np.mean(alfar),np.std(alfar))	
# print(np.mean(alfrr),np.std(alfrr))	


# print(alltp,alltn,allfn,allfp)
# print(float(alltp+alltn)/(alltp+alltn+allfp+allfn))
# print(float(allfp)/(allfp+alltn))
# print(float(allfn)/(alltp+allfn))