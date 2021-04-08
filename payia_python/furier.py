# _*_ coding: utf-8 _*_
import math
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn
# 原始函数，变换后函数、采样的时间段
def show(ori_func, ft, sampling_period): 
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

''''''

def fft(x,period):
	y = np.fft.fft(x) 
	frequency,y=show(x,y,period) 
	# return frequency,y
	
	return maxfft(frequency,y)


def maxfft(frequency,y):	
	lens=len(y)
	maxnum1=1
	maxnum2=1
	# maxnum3=1
	# maxnum4=1
	for i in range(2,lens/2):
		if y[maxnum1]<y[i]:
			maxnum1=i
	for i in range(2,lens/2):
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
	date.append(peakf)
	date.append(peak2)
	date.append(peakf2)
	return date


