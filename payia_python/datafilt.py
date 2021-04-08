# -*- coding=utf-8 -*-
import numpy as np
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import pywt

#标准化
def std(data):
	filtdata=[]
	data=np.array(data).reshape(-1,1)
	minMax = MinMaxScaler()
	data= minMax.fit_transform(data)
	for knum in data:
		filtdata.append(knum[0])
	return filtdata

#0-1化
def minmax(data):
	filtdata=[]
	data=np.array(data).reshape(-1,1)
	stdard = StandardScaler()
	data= stdard.fit_transform(data)
	for knum in data:
		filtdata.append(knum[0])
	return filtdata


#中值滤波
def meanfilt(data):
	filtdata=[]
	i=0
	while i <len(data)-10:
		filtdata.append(np.mean(data[i:i+10]))
		i=i+4
	return filtdata

#卡尔曼滤波	
def kalman(ymean,y,winsize):	#开头，线段，窗口
	sz = (winsize,)
	xhat=np.zeros(sz)	  # a posteri estimate of x
	P=np.zeros(sz)		 # a posteri error estimate
	xhatminus=np.zeros(sz) # a priori estimate of x
	Pminus=np.zeros(sz)	# a priori error estimate
	K=np.zeros(sz)		 # gain or blending factor
	R = 1 # estimate of measuremet variance, change to see effect
	Q = 0.1 # process variance
	# intial guesses
	xhat[0] = ymean
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
	# 在原dataframe中添加处理后的列便于画图
	# data['denoised_index']=pd.Series('x',index=data.index)
	# for i in range(len(data)):
	#	 data['denoised_index'][i] = denoised_index[i] 

	# # 画图
	# data = data.set_index(data['tradeDate'])
	# data.plot(figsize=(20,20),subplots=(2,1))
	# data.plot(figsize=(20,10))