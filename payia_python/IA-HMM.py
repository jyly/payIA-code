# _*_ coding: utf-8 _*_
from os import listdir
import numpy as np 
from furier import fft
from scipy import stats
from kalman import kalman



def extrafeature(filtdata):
	feature=[]
	a=np.max(filtdata)
	b=np.min(filtdata)
	datamean=np.mean(filtdata)
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
	feature.append(zerocross)#过零率
	feature.append(meancross)#过均值率
	fftdata=fft(filtdata,float(num/200))
	for l in fftdata:
		feature.append(l)
	return feature


userdata=[]		#用户原始的数据
classdata=[]	#用于分类的数据
# user=['hy','tzh','djb','zzc','ygy']
user=['hy','tzh','djb','zzc','ygy','ln','yw']

filenum=[]
#数据从文件读入内存
for name in range(0,len(user)):#遍历不同的目录
	classdata.append([])
	userdata.append([])
	# title=os.listdir('./'+user[name]+'/') 
	title=listdir('./'+user[name]+'/') 
	filenum.append(len(title))

	for time in range(0,len(title)):#遍历不同时间的文件
		classdata[name].append([])
		userdata[name].append([])
		for k in range(0,20):#5个3组的，加上一个混合量m，1个1组的
			userdata[name][time].append([])
		path='./'+user[name]+'/'+title[time]
		print path
		input_1=open(path,'ab+')
		flag=0
		for row in input_1:
			# if name==5 and time==4:
			# 	print num
			row=list(eval(row))	

			# if row[0]!=99.0 and flag==0:
			# 	continue
			if row[0]==99.0:
				flag=1
				continue
			k=0
			for i in range(0,5):
				for j in range(0,3):
					userdata[name][time][i*4+j].append(row[k])
					k=k+1
				userdata[name][time][i*4+3].append((row[k-1]**2+row[k-2]**2+row[k-3]**2)**0.5)
		num=len(userdata[name][time][0])
		input_1.close()

		#数据预处理兼提取特征
		for i in range(0,5):	#遍历5个传感器，将5个传感器中的数据特征提取出来
			for j in range(0,4):	#遍历4个数据
				filtdata=[]
				# print userdata[name][time][0][0]
				# if i==2:
				# else:
					# filtdata=savgol(userdata[name][time][i*4+j], 19, 3)
				filtdata=kalman(userdata[name][time][i*4+j][0],userdata[name][time][i*4+j],num)
				feature=extrafeature(filtdata)
				for k in feature:
					classdata[name][time].append(k)
		
#内存中的数据进行训练分类测试
# output_1=open('data/userdata.txt','wb+')
target=[]
dataset=[]

#将数据打上标注
for name in range(0,len(user)):
	title=listdir('./'+user[name]+'/') 
	for time in range(0,len(title)):
		target.append(name)
		dataset.append(classdata[name][time])#用户行属性，特征列属性

#构建对比数据项列
comdata=[]
for i in range(0,len(dataset[0])):
	comdata.append([])
	for j in range(len(dataset)):
		comdata[i].append(dataset[j][i])#特征行属性，用户列属性


micnum=[]
from minepy import MINE#minepy包——基于最大信息的非参数估计
m = MINE()
for i in range(0,len(comdata)):
	m.compute_score(target, comdata[i])
	micnum.append(m.mic())
# print micnum
newdataset=[]
for i in range(len(dataset)):
	newdataset.append([])
for i in range(0,20):
	maxindex=micnum.index(np.max(micnum))
	for j in range(0,len(comdata[0])):	
		newdataset[j].append(comdata[maxindex][j])
	del comdata[maxindex]
	del micnum[maxindex]
dataset=[]
dataset=newdataset



from hmmlearn import hmm
model = hmm.GaussianHMM(n_components=20, n_iter=10000, tol=0.05,covariance_type="full")
from sklearn.model_selection import train_test_split,cross_val_score
aveFAR=[]
aveFRR=[]
aveaccuracy=[]
for rand in range(0,10):
	X_train, X_test, y_train, y_test = train_test_split(dataset, target, test_size=0.2, random_state=rand)
	FAR=[]
	FRR=[]
	accuracy=[]
	for t in range(0,len(user)):
		observer=[]
		observerlen=[]
		for k in range(0,len(y_train)):
			if y_train[k]==t:
				for i in X_train[k]:
					# print i
					observer.append([i])
					# print observer		
				observerlen.append(20)
				# print observerlen	
		print "hmm",rand,t
		# observer=np.array(observer).reshape(-1,1)	
		observer=np.array(observer)	
		# print observer
		checknum=[]
		model.fit(observer,observerlen)
		for i in range(0,len(observerlen)-1):
			num=model.score(observer[i*20:(i+1)*20])
			# print num
			checknum.append(num)
		# print np.percentile(checknum,25)
		checknum=np.percentile(checknum,25)
		# ourscore=[]
		# otherscore=[]
		tp=0
		tn=0
		fp=0
		fn=0
		for k in range(0,len(y_test)):
			observer=[]
			for i in X_test[k]:
				observer.append([i])
			hmmsorce=model.score(observer)
			# print y_test[k],"   hmmscore:",hmmsorce
			if y_test[k]==t:
				# ourscore.append(hmmsorce)
				if hmmsorce>checknum:
					tp=tp+1
				else:
					fn=fn+1	
			else:
				# otherscore.append(hmmsorce)	
				if hmmsorce>checknum:
					fp=fp+1
				else:
					tn=tn+1	
		if tp==0 and fn==0:
			continue				
		tfar=float(fp)/(fp+tn)
		tfrr=float(fn)/(tp+fn)	
		# print tp,tn,fp,fn,tfar,tfrr	
		accuracy.append(float(tp+tn)/len(y_test))
		FAR.append(tfar)			
		FRR.append(tfrr)			
	aveFAR.append(np.mean(FAR))  #一次测试中平均每个用户的测试数值
	aveFRR.append(np.mean(FRR))
	aveaccuracy.append(np.mean(accuracy))
	# print "FAR=" ,aveFAR[rand],"FRR=",aveFRR[rand]
print "FAR=" ,np.mean(aveFAR),"FRR=",np.mean(aveFRR),"accuracy=",np.mean(aveaccuracy)#10次交叉的平均值
	# print ourscore
	# print otherscore
	# print "ourscore:",np.mean(ourscore)," otherscore:",np.mean(otherscore)		