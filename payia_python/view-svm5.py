# _*_ coding: utf-8 _*_
from os import listdir
import numpy as np 
from dividepoint import div
from datafilt import kalman,meanfilt,savgol,std,minmax,wt,guass,dataextra,compute_fisher,fisher_score
from datacontrol import predatawrite,predataread
import random
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn import svm
# user=['djb','hy','ln','tzh','ygy','yw','zzc','lxy','wql']
# user=['djb','hy','ln','tzh','ygy','yw','zzc']
# user=['djb','zzc','ln','tzh']

user=['hy','tzh','djb','zzc','ygy','ln','yw','lxy','ys','wql','wc']
# user=['hy','tzh']


def datasplit(dataset,target,rand,feature_size):
	dataset_train, dataset_test, target_train, target_test = train_test_split(dataset, target, test_size=0.2, random_state=rand*3)

	#临时数据准备
	# traindata=[]
	# testdata=[]
	# for i in range(0,len(dataset_train)):
	# 	traindata.append([])
	# for i in range(0,len(dataset_test)):
	# 	testdata.append([])

	# minum=fisher_score(dataset_train,target_train)
	# # print (minum)
	# indexsort = np.argsort(minum)
	# print(indexsort)
	# for i in range(0,20):
	# 	for j in range(0,len(dataset_train)):
	# 		traindata[j].append(dataset_train[j][indexsort[-i-1]])
	# 		# traindata[j].append(dataset_train[j][indexsort[i]])
	# 	for j in range(0,len(dataset_test)):
	# 		testdata[j].append(dataset_test[j][indexsort[-i-1]])
	# 		# testdata[j].append(dataset_test[j][indexsort[i]])
	# dataset_train=traindata
	# dataset_test=testdata

	return dataset_train, dataset_test, target_train, target_test


def pfcal(pretarget,target_test,winsize,weight):
	alltp=0
	alltn=0
	allfp=0
	allfn=0
	for name in range(0,winsize):
		tp=0
		tn=0
		fp=0
		fn=0
		for i in range(0,len(target_test)):
			if target_test[i]==name:
				# if pretarget[i]==name:
				if pretarget[i][name]>weight:
					tp=tp+1
				else:
					fn=fn+1
			else:	
				# if pretarget[i]==name:
				if pretarget[i][name]>weight:
					fp=fp+1
				else:
					tn=tn+1
		if tp==0 and fn==0:
			continue		
		# accuracy=float(tp+tn)/(tp+tn+fp+fn)
		# FAR=float(fp)/(fp+tn)	
		# FRR=float(fn)/(tp+fn)	
		# print ("tFAR=" ,FAR,"FRR=",FRR,"accuracy=",accuracy)
		alltp+=tp
		alltn+=tn
		allfp+=fp
		allfn+=fn
	# print (alltp,alltn,allfp,allfn)	
	accuracy=float(alltp+alltn)/(alltp+alltn+allfp+allfn)
	FAR=float(allfp)/(allfp+alltn)	
	FRR=float(allfn)/(alltp+allfn)
	
	# print ("FAR=" ,FAR,"FRR=",FRR,"accuracy=",accuracy)

	return 	alltp,alltn,allfp,allfn


def Svm(dataset,target,winsize,feature_size=30,c=2,g=0.05,weight=0.2):	
	alltp=0
	alltn=0
	allfp=0
	allfn=0
	for rand in range(0,10):
		dataset_train, dataset_test, target_train, target_test=datasplit(dataset,target,rand,feature_size)
		#实时生成模型
		clf = svm.SVC(C=c,gamma=g,class_weight='balanced',probability=True)
		clf = clf.fit(dataset_train, target_train)

		#使用已生成模型
		# joblib.dump(clf,'model.pkl')
		# clf=joblib.load('model.pkl')
		pretarget=clf.predict_proba(dataset_test)
		# pretarget=clf.predict(dataset_test)
		
		tp,tn,fp,fn=pfcal(pretarget,target_test,winsize,weight)
		alltp+=tp
		alltn+=tn
		allfp+=fp
		allfn+=fn
	aveaccuracy=float(alltp+alltn)/(alltp+alltn+allfp+allfn)
	aveFAR=float(allfp)/(allfp+alltn)	
	aveFRR=float(allfn)/(alltp+allfn)
	print ("aveFAR=" ,aveFAR,"aveFRR=",aveFRR,"aveaccuracy=",aveaccuracy)#10次交叉的平均值
	# return alltp,alltn,allfp,allfn
	return aveaccuracy,aveFAR,aveFRR


def extrafeature(filtdata):
	feature=[]
	a=np.max(filtdata)
	b=np.min(filtdata)
	datamean=np.mean(filtdata)
	zerocross=0
	for i in range(0,len(filtdata)-1):
		if filtdata[i]==0:
			zerocross=zerocross+1
			continue
		# if filtdata[i]==datamean:
		# 	zerocross=zerocross+1
		# 	continue
		if filtdata[i]>0 and filtdata[i+1]<0:
			zerocross=zerocross+1
			continue
		if filtdata[i]<0 and filtdata[i+1]>0:
			zerocross=zerocross+1	
			continue
	feature.append(a)
	feature.append(b)
	feature.append(datamean)
	feature.append(np.mean(np.absolute(filtdata-np.mean(filtdata))))#绝对差
	feature.append(np.mean(np.absolute(filtdata)))#振幅平均值
	feature.append(np.std(filtdata))#标准差
	feature.append(stats.skew(filtdata))	#偏态
	feature.append(stats.kurtosis(filtdata)) #峰度
	feature.append(zerocross)#过零率
	return feature



# # timewrap('./data2o/','./timewrap/',user,20)

alfar=[]
alfrr=[]
alacc=[]
for filenum in range (40,41,10):

	# userdata=[]		#用户原始的数据
	# target=[]
	# dataset=[]
	# for name in range(0,len(user)):#遍历不同的目录
	# 	userdata.append([])
	# 	title=listdir('./data/wechat/'+user[name]+'/') 
	# 	# for time in range(0,len(title)):#遍历不同时间的文件
	# 	for time in range(0,filenum):#遍历不同时间的文件
	# 		path='./data/wechat/'+user[name]+'/'+title[time]
	# 		print(path)
	# 		userdata[name].append([])
	# 		userdata[name][time]=[[] for i in range(6)]
	# 		upstart,upstop,tempuserdata=dataextra(path)
	# 		# print (tempuserdata)
	# 		for i in range(0,6):
	# 			# userdata[name][time][i]=meanfilt(userdata[name][time][i])
	# 			userdata[name][time][i]=kalman(tempuserdata[i])

	# 		# upstartpoint,upstoppoint,downstartpoint,downstoppoint=div(userdata[name][time][1],userdata[name][time][3],int(upstart),int(upstop))
		
			
	# 		for i in range(0,6):
	# 			userdata[name][time][i]=userdata[name][time][i][upstart:upstop+150]
	# 			# userdata[name][time][i]=userdata[name][time][i][upstart-50:downstoppoint+100]
	# 			# userdata[name][time][i]=userdata[name][time][i][upstartpoint-50:downstoppoint+70]
	# 			# userdata[name][time][i]=userdata[name][time][i][workstart:workstart+200]
		
	# 		# knum=len(userdata[name][time][0])-20
	# 		# kin=0
	# 		# while kin<knum-40:
	# 		# 	target.append(name)
	# 		# 	dataset.append([])
	# 		# 	for i in range(0,6):
	# 		# 		filtdata=userdata[name][time][i][kin:kin+40]
	# 		# 		feature=extrafeature(filtdata)
	# 		# 		for k in feature:
	# 		# 			dataset[fealen].append(k)
	# 		# 	dataset[fealen].append(np.mean(userdata[name][time][6][kin:kin+40]))
	# 		# 	dataset[fealen].append(np.mean(userdata[name][time][7][kin:kin+40]))

	# 		# 	fealen=fealen+1
	# 		# 	kin=kin+20	


	# 		target.append(name)
	# 		tempfeature=[]
	# 		for i in range(0,6):
	# 			filtdata=userdata[name][time][i]
	# 			feature=extrafeature(filtdata)
	# 			for k in feature:
	# 				tempfeature.append(k)
	# 		temp1=[]
	# 		temp2=[]
	# 		for i in range(0,len(userdata[name][time][0])):
	# 			temp1.append((userdata[name][time][0][i]*2+userdata[name][time][1][i]*2+userdata[name][time][2][i]*2)**2)
	# 			temp2.append((userdata[name][time][3][i]*2+userdata[name][time][4][i]*2+userdata[name][time][5][i]*2)**2)
	# 		# tempfeature.append(np.mean(temp1))
	# 		# tempfeature.append(np.mean(temp2))
	# 		dataset.append(tempfeature)


	# dataset 是一个数据项的所有特征为1行， targetr对应的行是对应的对象
		


	# predatawrite(dataset,target,'./svm5-50.csv')  
	dataset,target=predataread('./svm5-50.csv')

	acc,far,frr=Svm(dataset,target,len(user),30,2,0.05,0.096)
	# DecisionTree(dataset,target,len(user),30,8,0.2)
	# RandomForest(dataset,target,len(user),30,100,5,0.2)
	# MLP(dataset,target,len(user),30,40,500,0.2)
	# Gaussian_bayes(dataset,target,len(user),30,0.2)
	alacc.append(acc)
	alfar.append(far)
	alfrr.append(frr)

print(alacc)	
print(alfar)	
print(alfrr)	

