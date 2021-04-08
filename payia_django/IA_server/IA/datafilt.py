# -*- coding=utf-8 -*-
import numpy as np
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from skfeature.function.similarity_based import fisher_score
import pywt
from scipy import stats
from scipy.ndimage import filters
from scipy.sparse import *
from minepy import MINE
from math import log
from os import listdir
from skfeature.utility.construct_W import construct_W
from skfeature.utility.util import reverse_argsort


def extrafeature(filtdata):
	feature=[]
	a=np.max(filtdata)
	b=np.min(filtdata)
	datamean=np.mean(filtdata)
	feature.append(a)
	feature.append(b)
	feature.append(datamean)
	feature.append(np.mean(np.absolute(filtdata-np.mean(filtdata))))#绝对差
	feature.append(np.mean(np.absolute(filtdata)))#振幅平均值
	feature.append(np.std(filtdata))#标准差
	tempfiltdata=[]
	for i in range(1,len(filtdata)):
		tempfiltdata.append(filtdata[i]-filtdata[i-1])
	feature.append(np.max(tempfiltdata))	
	feature.append(np.min(tempfiltdata))	
	feature.append(np.mean(np.absolute(tempfiltdata-np.mean(tempfiltdata))))	
	feature.append(np.mean(np.absolute(tempfiltdata)))	
	# feature.append(np.std(tempfiltdata))	
	return feature


#数据滤波

	#滤波函数  
def guass(data):
	return filters.gaussian_filter(data,2)


#标准化
def std(data):
	filtdata=[]
	data=np.array(data).reshape(-1,1)
	stdard = StandardScaler()
	data= stdard.fit_transform(data)
	for knum in data:
		filtdata.append(knum[0])
	return filtdata

#0-1化
def minmax(data):
	filtdata=[]
	data=np.array(data).reshape(-1,1)
	minMax = MinMaxScaler()
	data= minMax.fit_transform(data)
	for knum in data:
		filtdata.append(knum[0])
	return filtdata


#中值滤波
def meanfilt(data):
	filtdata=[]
	i=0
	while i <len(data)-10:
		filtdata.append(np.mean(data[i:i+10]))
		i=i+5
	return filtdata


#卡尔曼滤波	
def kalman(y):	#开头，线段，窗口
	winsize=len(y)
	sz = (winsize,)
	xhat=np.zeros(sz)	  # a posteri estimate of x
	P=np.zeros(sz)		 # a posteri error estimate
	xhatminus=np.zeros(sz) # a priori estimate of x
	Pminus=np.zeros(sz)	# a priori error estimate
	K=np.zeros(sz)		 # gain or blending factor
	R = 5 # estimate of measuremet variance, change to see effect
	Q = 0.1 # process variance
	# intial guesses
	xhat[0] = y[0]
	P[0] = 1.0
	for k in range(1,winsize):
		# time update
		xhatminus[k] = xhat[k-1]  #X(k|k-1) = AX(k-1|k-1) + BU(k) + W(k),A=1,BU(k) = 0
		Pminus[k] = P[k-1]+Q	  #P(k|k-1) = AP(k-1|k-1)A' + Q(k) ,A=1
		# measurement update
		K[k] = Pminus[k]/( Pminus[k]+R ) #Kg(k)=P(k|k-1)H'/[HP(k|k-1)H' + R],H=1
		xhat[k] = xhatminus[k]+K[k]*(y[k]-xhatminus[k]) #X(k|k) = X(k|k-1) + Kg(k)[Z(k) - HX(k|k-1)], H=1
		P[k] = (1-K[k])*Pminus[k] #P(k|k) = (1 - Kg(k)H)P(k|k-1), H=1
	return xhat

"""
* 创建系数矩阵X
* size - 2×size+1 = window_size
* rank - 拟合多项式阶次
* x - 创建的系数矩阵
"""
def create_x(size, rank):
	x = []
	for i in range(2 * size + 1):
		m = i - size
		row = [m**j for j in range(rank)]
		x.append(row) 
	x = np.mat(x)
	return x

"""
 * Savitzky-Golay平滑滤波函数
 * data - list格式的1×n纬数据
 * window_size - 拟合的窗口大小	窗口越大越平滑
 * rank - 拟合多项式阶次 阶次越高，越贴和原来图像
 * ndata - 修正后的值
"""
def savgol(data, window_size, rank):
	m = int((window_size - 1) / 2)
	odata = data[:]
	# 处理边缘数据，首尾增加m个首尾项
	for i in range(m):
		odata.insert(0,odata[0])
		odata.insert(len(odata),odata[len(odata)-1])
	# 创建X矩阵
	x = create_x(m, rank)
	# 计算加权系数矩阵B
	b = (x * (x.T * x).I) * x.T
	a0 = b[m]
	a0 = a0.T
	# 计算平滑修正后的值
	ndata = []
	for i in range(len(data)):
		y = [odata[i + j] for j in range(window_size)]
		y1 = np.mat(y) * a0
		y1 = float(y1)
		ndata.append(y1)
	return ndata

def wt(index_list,wavefunc,lv,m,n):   # 打包为函数，方便调节参数。  lv为分解层数；data为最后保存的dataframe便于作图；index_list为待处理序列；wavefunc为选取的小波函数；m,n则选择了进行阈值处理的小波系数层数
# def wt(index_list,data,wavefunc,lv,m,n):   # 打包为函数，方便调节参数。  lv为分解层数；data为最后保存的dataframe便于作图；index_list为待处理序列；wavefunc为选取的小波函数；m,n则选择了进行阈值处理的小波系数层数
	# 分解
	coeff = pywt.wavedec(index_list,wavefunc,mode='sym',level=lv)   # 按 level 层分解，使用pywt包进行计算， cAn是尺度系数 cDn为小波系数
	sgn = lambda x: 1 if x > 0 else -1 if x < 0 else 0 # sgn函数
	# 去噪过程
	for i in range(m,n+1):   # 选取小波系数层数为 m~n层，尺度系数不需要处理
		cD = coeff[i]
		for j in range(len(cD)):
			Tr = np.sqrt(2*np.log(len(cD)))  # 计算阈值
			if cD[j] >= Tr:
				coeff[i][j] = sgn(cD[j]) - Tr  # 向零收缩
			else:
				coeff[i][j] = 0   # 低于阈值置零

	# 重构
	denoised_data_list = pywt.waverec(coeff,wavefunc)
	abs_denoised_list = list(map(lambda x: abs(x), denoised_data_list))
	# 返回降噪结果
	return abs_denoised_list




def fftshow(ori_func, ft, sampling_period): 
	n = float(len(ori_func)) 
	interval = sampling_period / n 
	frequency = np.arange(int(n / 2)) / (n * interval) 
	nfft = abs(ft[range(int(n / 2))] / n ) 
	return frequency,nfft
	fig1 = plt.figure()
	## 绘制原始函数
	plt.subplot(2, 1, 1) 
	plt.plot(np.arange(0, sampling_period, interval), ori_func, 'black') 
	plt.xlabel('Time'), plt.ylabel('Amplitude') 
	# # 绘制变换后的函数
	plt.subplot(2,1,2) 
	plt.plot(frequency, nfft, 'red') 
	plt.xlabel('Freq (Hz)'), plt.ylabel('Amp. Spectrum') 
	plt.show() 



def fft(x,period):
	y = np.fft.fft(x) 
	frequency,y=fftshow(x,y,period) 
	# return frequency,y
	
	return maxfft(frequency,y)


def maxfft(frequency,y):	
	lens=len(y)
	maxnum1=1
	maxnum2=1
	# maxnum3=1
	# maxnum4=1
	for i in range(2,int(lens/2)):
		if y[maxnum1]<y[i]:
			maxnum1=i
	for i in range(2,int(lens/2)):
		if y[maxnum2]<y[i] and (y[i]<y[maxnum1]):
			maxnum2=i
	# for i in range(2,lens/2):
	# 	if y[maxnum3]<y[i] and (y[i]<y[maxnum]) and (y[i]<y[maxnum2]) :
	# 		maxnum3=i
	# for i in range(2,lens/2):
	# 	if y[maxnum4]<y[i] and (y[i]<y[maxnum]) and (y[i]<y[maxnum2]) and (y[i]<y[maxnum3]):
	# 		maxnum4=i
	peak=y[maxnum1]
	peakf=frequency[maxnum1]
	peak2=y[maxnum2]
	peakf2=frequency[maxnum2]
	date=[]
	date.append(peak)
	# date.append(peakf)
	date.append(peak2)
	# date.append(peakf2)
	return date


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
	# print (Hx,Hy,MI,MIhat)   
	MIhat = MIhat/Hy
	# print MIhat   
	return MIhat
	


def compute_fisher(data,target,num):
	comdata=[]
	for i in range(0,len(data[0])):
		comdata.append([])
		for j in range(len(data)):
			comdata[i].append(data[j][i])
	fisherscore=fisher_score.fisher_score(np.array(data), target)
	return fisherscore

def fisher_score(X, y):
    kwargs = {"neighbor_mode": "supervised", "fisher_score": True, 'y': y}
    W = construct_W(X, **kwargs)
    D = np.array(W.sum(axis=1))
    L = W
    tmp = np.dot(np.transpose(D), X)
    D = diags(np.transpose(D), [0])
    Xt = np.transpose(X)
    t1 = np.transpose(np.dot(Xt, D.todense()))
    t2 = np.transpose(np.dot(Xt, L.todense()))
    D_prime = np.sum(np.multiply(t1, X), 0) - np.multiply(tmp, tmp)/D.sum()
    L_prime = np.sum(np.multiply(t2, X), 0) - np.multiply(tmp, tmp)/D.sum()
    D_prime[D_prime < 1e-12] = 10000
    lap_score = 1 - np.array(np.multiply(L_prime, 1/D_prime))[0, :]
    score = 1.0/lap_score - 1
    return score



def dataextra(filepath):
	#用于分段
	upstart=-1
	upstop=-1
	tol=0
	userdata=[[] for i in range(15)]
	# print (filepath)
	input_1=open(filepath,'r+')
	#可用于分段
	for row in input_1:
		row=list(eval(row))	
		if(row[0]==77.0):
			continue
		if(row[0]==88.0):
			upstart=tol
			continue
		if(row[0]==99.0):
			upstop=tol
			continue	
		for i in range(0,15):
			userdata[i].append(row[i])	
		tol=tol+1	
	input_1.close()
	return upstart,upstop,userdata

