# _*_ coding: utf-8 _*_
from os import listdir
import numpy as np 
from scipy import stats
from furier import fft
from datafilt import kalman,meanfilt,savgol,std,minmax,wt
from fisherscore import compute_fisher
from mul_information import mulinform,NMI
from math import log

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        if featVec not in labelCounts.keys():
            labelCounts[featVec]=0
        labelCounts[featVec]+=1
    # print labelCounts  
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)
    return shannonEnt

def extrafeature(filtdata):
	feature=[]
	a=np.max(filtdata)
	b=np.min(filtdata)
	datamean=np.mean(filtdata)
	zerocross=0
	meancross=0
	for i in range(0,len(filtdata)-1):
		if filtdata[i]==0:
			zerocross=zerocross+1
			continue
		if filtdata[i]==datamean:
			zerocross=zerocross+1
			continue
		if filtdata[i]>0 and filtdata[i+1]<0:
			zerocross=zerocross+1
			continue
		if filtdata[i]<0 and filtdata[i+1]>0:
			zerocross=zerocross+1	
			continue
		if filtdata[i]>datamean and filtdata[i+1]<datamean:
			meancross=meancross+1	
			continue
		if filtdata[i]<datamean and filtdata[i+1]>datamean:
			meancross=meancross+1	

	# feature.append(round(zerocross,2))#过零率
	# feature.append(round(meancross,2))#过均值率
	# feature.append(round(a,2))
	# feature.append(round(b,2))
	# feature.append(round(a-b,2)) #波动范围
	# feature.append(round(datamean,2))
	# feature.append(round(np.median(filtdata),2)) #中位数
	# feature.append(round(np.mean(np.absolute(filtdata-np.mean(filtdata))),2))#绝对差
	# feature.append(round(np.mean(np.absolute(filtdata)),2))#振幅平均值
	# feature.append(round(np.std(filtdata),2))#标准差
	# feature.append(round(np.percentile(filtdata,75),2)) #上四分位数
	# feature.append(round(np.percentile(filtdata,25),2)) #下四分位数
	# feature.append(round(np.percentile(filtdata,75)-np.percentile(filtdata,25),2)) #四分位距
	# feature.append(round(stats.skew(filtdata),2))	#偏态
	# feature.append(round(stats.kurtosis(filtdata),2)) #峰度
	# feature.append(round(calcShannonEnt(filtdata),2))#序列熵
	fftdata=fft(filtdata,float(len(filtdata)))
	fftdata=fft(filtdata,float(len(filtdata)/50))
	# for l in fftdata:
	# 	feature.append(round(l,2))

	feature.append(zerocross)#过零率
	feature.append(meancross)#过均值率
	feature.append(a)
	feature.append(b)
	feature.append(a-b) #波动范围
	feature.append(datamean)
	feature.append(np.median(filtdata)) #中位数
	feature.append(np.mean(np.absolute(filtdata-np.mean(filtdata))))#绝对差
	feature.append(np.mean(np.absolute(filtdata)))#振幅平均值
	feature.append(np.std(filtdata))#标准差
	feature.append(np.percentile(filtdata,75)) #上四分位数
	feature.append(np.percentile(filtdata,25)) #下四分位数
	feature.append(np.percentile(filtdata,75)-np.percentile(filtdata,25)) #四分位距
	feature.append(stats.skew(filtdata))	#偏态
	feature.append(stats.kurtosis(filtdata)) #峰度
	feature.append(calcShannonEnt(filtdata))#序列熵
	for l in fftdata:
		feature.append(l)

	return feature



def predatawrite(data,target):
	output_1=open("predata.csv","wb")
	fealen=len(data[0])
	for i in range(0,len(target)):
		output_1.write(str(target[i])+",")
		for j in range(0,fealen):
			output_1.write(str(data[i][j])+",")
		output_1.write("\n")
	output_1.close()

def predataread():
	target=[]
	dataset=[]
	input_1=open("predata.csv","ab+")
	num=0
	for row in input_1:
		dataset.append([])
		row=list(eval(row))
		target.append(row[0])	
		for i in range(1,len(row)):
			dataset[num].append(row[i])
		num=num+1	
	input_1.close()
	return target,dataset


userdata=[]		#用户原始的数据
# user=['hy']
user=['djb','hy','ln','tzh','ygy','yw','zzc']
# user=['hy','tzh','djb','zzc','ygy','ln','yw']
target=[]
dataset=[]
fealen=0
filenum=[]  #读取文件数
#数据从文件读入内存

'''
'''


for name in range(0,len(user)):#遍历不同的目录
	# classdata.append([])
	userdata.append([])
	title=listdir('./'+user[name]+'/') 
	filenum.append(len(title))
	for time in range(0,len(title)):#遍历不同时间的文件
		userdata[name].append([])
		for k in range(0,20):#5个3组的，加上一个混合量m，1个1组的
			userdata[name][time].append([])
		path='./'+user[name]+'/'+title[time]
		print (path)
		input_1=open(path,'r')
		flag=0
		#可用于分段
		for row in input_1:
			# if name==5 and time==4:
			# 	print num
			row=list(eval(row))	
			print(row)
			# if row[0]!=99.0 and flag==0:
			# 	continue
			if row[0]==99.0:
				flag=flag+1
				continue
			k=0
			# if row[1]>6:
			for i in range(0,5):
				for j in range(0,3):
					userdata[name][time][i*4+j].append(row[k])
					# userdata[name][time][i*4+j].append(round( row[k] , 5 ))
					k=k+1
				userdata[name][time][i*4+3].append((row[k-1]**2+row[k-2]**2+row[k-3]**2)**0.5)
				# userdata[name][time][i*4+3].append(round((row[k-1]**2+row[k-2]**2+row[k-3]**2)**0.5, 5 ))
		input_1.close()
		# print len(userdata[name][time][0])/4
		print(flag)
		userdata=np.array(userdata)
		print(userdata.shape)
		for i in range(0,5):
			for j in range(0,4):
				userdata[name][time][i*4+j]=meanfilt(userdata[name][time][i*4+j])
				userdata[name][time][i*4+j]=kalman(userdata[name][time][i*4+j][0],userdata[name][time][i*4+j],len(userdata[name][time][i*4+j]))
				# kf = KalmanFilter(initial_state_mean = userdata[name][time][i*4+j][0])
				# userdata[name][time][i*4+j]=userdata[name][time][i*4+j].reshape(-1)
				# userdata[name][time][i*4+j]=wt(userdata[name][time][i*4+j],'db4',5,4,5)
		knum=len(userdata[name][time][0])
		# if knum>100:
		# 	kin=0
		# 	while kin<knum-100:
		# 		target.append(name)
		# 		dataset.append([])
		# 		# classdata[name].append([])
		# 		for i in range(0,5):
		# 			for j in range(0,4):
		# 				filtdata=userdata[name][time][i*4+j][kin:kin+100]
		# 				feature=extrafeature(filtdata)
		# 				for k in feature:
		# 					dataset[fealen].append(k)
		# 		fealen=fealen+1
		# 		kin=kin+10	
		# else:
		target.append(name)
		dataset.append([])
		for i in range(0,5):
			for j in range(0,4):
				filtdata=userdata[name][time][i*4+j]
				feature=extrafeature(filtdata)
				for k in feature:
					dataset[fealen].append(k)
		fealen=fealen+1			



# predatawrite(dataset,target)
# target,dataset=predataread()



#主成分分析，提取最相关的30个特征
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn import tree,preprocessing,svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
# import matplotlib.pyplot as plt
userfn=[]
userfp=[]
for i in range(0,len(user)):
	userfn.append(0)
	userfp.append(0)

# knum=50
# while knum< 1000:
	# knum=knum+20
aveFAR=[]	
aveFRR=[]
avepre=[]
avefpre=[]
avetnr=[]
aveaccuracy=[]

for rand in range(0,10):
	x_train, x_test, y_train, y_test = train_test_split(dataset, target, test_size=0.2, random_state=rand*3)
	traindata=[]
	testdata=[]
	for i in range(0,len(x_train)):
		traindata.append([])
	for i in range(0,len(x_test)):
		testdata.append([])
	# minum=mulinform(x_train,y_train)
	minum=NMI(x_train,y_train)
	indexsort = np.argsort(minum)

	for i in range(0,60):
		for j in range(0,len(x_train)):
			traindata[j].append(x_train[j][indexsort[-i-1]])
		for j in range(0,len(x_test)):
			testdata[j].append(x_test[j][indexsort[-i-1]])

	x_train=traindata
	x_test=testdata
	lda=LinearDiscriminantAnalysis()
	lda.fit(x_train,y_train)
	x_train=lda.transform(x_train)
	x_test=lda.transform(x_test)


	# convert_x=np.dot(x,np.transpose(lda.coef_))+lda.intercept_
	# plot_LDA(convert_x,y)


	# clf = tree.DecisionTreeClassifier(min_samples_split=10)
	# clf = RandomForestClassifier(n_estimators=100,min_samples_split=8)
	clf = svm.SVC(C=1.9,gamma=0.033)
	# clf = KNeighborsClassifier(n_neighbors=13,weights='distance')
	# clf = MLPClassifier(hidden_layer_sizes=(70, ),activation='relu',solver='adam')
	clf = clf.fit(x_train, y_train)
	pretarget=clf.predict(x_test)
	# print y_test
	# print pretarget
	FAR=[]
	FRR=[]
	PRE=[]
	FPRE=[]
	TNR=[]
	accuracy=[]
	for name in range(0,len(user)):
		tp=0
		tn=0
		fp=0
		fn=0
		for  i in range(0,len(y_test)):
			if y_test[i]==name:
				if pretarget[i]==name:
					tp=tp+1
				else:
					fn=fn+1
					userfn[name]=userfn[name]+1
			else:	
				if pretarget[i]==name:
					fp=fp+1
					userfp[name]=userfp[name]+1
				else:
					tn=tn+1
		if tp==0 and fn==0:
			continue		
		# tfar=float(fp)/(fp+tn)
		# tfrr=float(fn)/(tp+fn)	
		# print tp,tn,fp,fn,tfar,tfrr	
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
print  ("FAR=" ,np.mean(aveFAR),"FRR=",np.mean(aveFRR),"accuracy=",np.mean(aveaccuracy),"PRE=",np.mean(avepre),"FPRE=",np.mean(avefpre),"TNR=",np.mean(avetnr))#10次交叉的平均值
# print "knum=",knum,"  FAR=" ,np.mean(aveFAR),"FRR=",np.mean(aveFRR),"accuracy=",np.mean(aveaccuracy),"PRE=",np.mean(avepre),"FPRE=",np.mean(avefpre),"TNR=",np.mean(avetnr)#10次交叉的平均值
# print  "FAR=" ,np.mean(aveFAR),"FRR=",np.mean(aveFRR),"accuracy=",np.mean(aveaccuracy)
# print "knum=",knum,"  FAR=" ,np.mean(aveFAR),"FRR=",np.mean(aveFRR),"accuracy=",np.mean(aveaccuracy)
# print userfn,userfp



# for i in filenum:
# 	print i
# print sum(filenum)	




'''
import pydotplus 
import os 


# clf = RandomForestClassifier()
clf =tree.DecisionTreeClassifier()
clf = clf.fit(dataset, target)
pretarget=clf.predict(dataset)
print pretarget
t=0
f=0
for  i in range(0,len(target)):
	if pretarget[i]==target[i]:
		t=t+1
	else:		
		f=f+1
print 	't=',t,' f=',f		

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
dot_data = tree.export_graphviz(clf, out_file=None) 
graph = pydotplus.graph_from_dot_data(dot_data) 
graph.write_pdf("active.pdf")




'''



#泊松相关系数
# from scipy.stats import pearsonr
# pearsonrscore=[]		
# for i in range(0,len(comdata)):
# 	pearsonrscore.append(np.abs(pearsonr(comdata[i],target)[0]))
# print  pearsonrscore
# for i in range(0,20):
# 	maxindex=pearsonrscore.index(np.max(pearsonrscore))
# 	for j in range(0,len(comdata[0])):	
# 		newdataset[j].append(comdata[maxindex][j])
# 	del comdata[maxindex]
# 	del pearsonrscore[maxindex]


#二者交叉特征

# fisherscore=[]		
# for i in range(0,len(comdata)):
# 	fisherscore.append([i,fisher_criterion(comdata[i],target)])


# micnum=[]
# from minepy import MINE#minepy包——基于最大信息的非参数估计
# m = MINE()
# for i in range(0,len(comdata)):
# 	m.compute_score(target, comdata[i])
# 	micnum.append([i,m.mic()])   #得出不同特征的互信息值

# temptoken=[]
# for i in range(0,len(fisherscore)):
# 	temptoken.append(0)

# for i in range(0,80):
# 	maxindex=0
# 	for j in range(0,len(fisherscore)):
# 		if fisherscore[maxindex][1]<fisherscore[j][1]:
# 			maxindex=j
# 	temptoken[fisherscore[maxindex][0]]=temptoken[fisherscore[maxindex][0]]+1
# 	del fisherscore[maxindex]		

# for i in range(0,80):
# 	maxindex=0
# 	for j in range(0,len(micnum)):
# 		if micnum[maxindex][1]<micnum[j][1]:
# 			maxindex=j
# 	temptoken[micnum[maxindex][0]]=temptoken[micnum[maxindex][0]]+1
# 	del micnum[maxindex]


# feature=[]
# for i in range(0,len(temptoken)):
# 	if temptoken[i]>1:	
# 		feature.append(i)
# 		for j in range(0,len(comdata[0])):	
# 			newdataset[j].append(comdata[i][j])
# print feature,len(feature)
