# _*_ coding: utf-8 _*_
import math
from os import listdir
import numpy as np 
from scipy import stats
from furier import fft
from kalman import kalman
# from DTWmodel import display
import thread
import time


def midledata(filtdata):
	resdata=[]
	i=0
	while i <len(filtdata)-10:
		resdata.append(np.mean(filtdata[i:i+10]))
		i=i+4
	return resdata	

userdata=[]		#用户原始的数据
classdata=[]	#用于分类的数据
user=['hy','tzh','djb','zzc','ygy','ln','yw']

#数据从文件读入内存
for name in range(0,len(user)):#遍历不同的目录
# for name in range(0,len(user)):#遍历不同的目录
	classdata.append([])
	userdata.append([])
	title=listdir('./'+user[name]+'/') 
	for time in range(0,len(title)):#遍历不同时间的文件
		classdata[name].append([])
		userdata[name].append([])
		for k in range(0,20):#5个3组的，加上一个混合量m，1个1组的
			userdata[name][time].append([])
			# classdata[name][time].append([])
		path='./'+user[name]+'/'+title[time]
		print path
		input_1=open(path,'ab+')
		for row in input_1:
			# if name==5 and time==4:
			# 	print num
			row=list(eval(row))	
			if row[0]==99.0:
				continue
			k=0
			for i in range(0,2):#加入光感器之外的数据
				for j in range(0,3):
					userdata[name][time][i*4+j].append(row[k])
					k=k+1
				userdata[name][time][i*4+3].append((row[k-1]**2+row[k-2]**2+row[k-3]**2)**0.5)
		num=len(userdata[name][time][0])
		input_1.close()
		#数据预处理,滤波
		for i in range(0,2):	#遍历5个传感器
			for j in range(0,4):	#遍历4个数据
				filtdata=userdata[name][time][i*4+j]
				filtdata=midledata(filtdata)
				filtdata=kalman(filtdata[0],filtdata,len(filtdata))
				classdata[name][time].append(filtdata)



target=[]
dataset=[]

#将数据打上标注
for name in range(0,len(user)):
	title=listdir('./'+user[name]+'/') 
	for time in range(0,len(title)):
		target.append(name)
		dataset.append(classdata[name][time])#用户行属性，特征列属性


from dtw import dtw
euclidean_norm = lambda x, y: np.abs(x - y)

aveFAR=[]	
aveFRR=[]
avepre=[]
avefpre=[]
avetnr=[]
aveaccuracy=[]
from sklearn.model_selection import train_test_split,cross_val_score
for rand in range(0,10):
	X_train, X_test, y_train, y_test = train_test_split(dataset, target, test_size=0.2, random_state=rand)
	FAR=[]
	FRR=[]
	PRE=[]
	FPRE=[]
	TNR=[]
	accuracy=[]
	for k in range(0,len(user)):
		comdata=[]
		comscore=[]
		for i in range(0,len(y_train)):
			if y_train[i]==k:
				comdata.append(X_train[i])
		# print len(comdata)		
		# for n1 in range(0,len(comdata)-1):
		for n2 in range(1,len(comdata)):
			# print n1,n2
			total=0
			for i in range(0,2):	#遍历5个传感器，将5个传感器中的数据特征提取出来
				# if i==3:
				# 	break
				for j in range(0,4):	#遍历4个数据
					dis, cost_matrix, acc_cost_matrix, path = dtw(comdata[0][i*4+j].reshape(-1, 1), comdata[n2][i*4+j].reshape(-1, 1), dist=euclidean_norm)
					# print dis,n2,i,j
					total=total+dis
			comscore.append(total)
		comscore=np.percentile(comscore,25)
		print "comscore= ",comscore		
		tp=0
		tn=0
		fp=0
		fn=0
		for n2 in range(0,len(y_test)):
			tempscore=[]
			for n1 in range(0,len(comdata)):
				total=0
				for i in range(0,2):	#遍历5个传感器，将5个传感器中的数据特征提取出来
					for j in range(0,4):	#遍历4个数据
						dis, cost_matrix, acc_cost_matrix, path = dtw(comdata[n1][i*4+j].reshape(-1, 1), X_test[n2][i*4+j].reshape(-1, 1), dist=euclidean_norm)
						total=total+dis
				tempscore.append(total)
			tempscore=np.min(tempscore)
			print "n2=",n2,"tempscore="
			if y_test[n2]==k:
				if tempscore<comscore:
					tp=tp+1
				else:
					fn=fn+1	
			else:
				if tempscore<comscore:
					fp=fp+1
				else:
					tn=tn+1	
		accuracy.append(float(tp+tn)/len(y_test))
		FAR.append(float(fp)/(fp+tn))			
		FRR.append(float(fn)/(tp+fn))
		PRE.append(float(tp)/(tp+fp))
		FPRE.append(float(tn)/(tn+fn))
		TNR.append(float(tn)/(tn+fp))			
	aveFAR.append(np.mean(FAR))  #一次测试中平均每个用户的测试数值
	aveFRR.append(np.mean(FRR))
	avepre.append(np.mean(PRE))
	avefpre.append(np.mean(FPRE))
	avetnr.append(np.mean(TNR))
	aveaccuracy.append(np.mean(accuracy))
	# print "FAR=" ,aveFAR[rand],"FRR=",aveFRR[rand]
print  "FAR=" ,np.mean(aveFAR),"FRR=",np.mean(aveFRR),"accuracy=",np.mean(aveaccuracy),"PRE=",np.mean(avepre),"FPRE=",np.mean(avefpre),"TNR=",np.mean(avetnr)#10次交叉的平均值
