# _*_ coding: utf-8 _*_
from os import listdir
import numpy as np 
from scipy import stats,interp
from datafilt import kalman,meanfilt,savgol,std,minmax,wt,guass,dataextra
import matplotlib.pyplot as plt
from dividepoint import div
from matplotlib.ticker import MultipleLocator, FormatStrFormatter



font1 = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 12,
}



#数据从文件读入内存

# user=['djb','hy','ln','tzh','ygy','yw','zzc','lxy','wql']
# user=['yw','zzc','wql']
# user=['djb']

# user=['djb','hy','tzh','ygy','yw']
user=['djb','hy']



for name in range(0,len(user)):#遍历不同的目录

	# title=listdir('./special2/') 
	title=listdir('./data/'+user[name]+'/') 

	for time in range(0,len(title)):#遍历不同时间的文件
		path='./data/'+user[name]+'/'+title[time]
		print (path)
		# path='./special2/'+title
		userdata=[]
		userdata.append([])
		userdata=[[] for i in range(15)]
		workstart,upstart,upstop,tempuserdata=dataextra(path)

		print (workstart,upstart,upstop)
		for i in range(0,15):
			# userdata[i]=meanfilt(userdata[i])
			userdata[i]=kalman(tempuserdata[i])

		upstartpoint,upstoppoint,downstartpoint,downstoppoint=div(userdata[1],userdata[3],upstart,upstop)
		# upstartpoint,upstoppoint,downstartpoint,downstoppoint=div3(userdata[1],userdata[3],int(workstart),int(upstart),int(upstop))
		# upstartpoint,upstoppoint,downstartpoint,downstoppoint=div5(userdata[1],userdata[3],int(workstart),int(upstart),int(upstop))
		# print (upstartpoint,upstoppoint,downstartpoint,downstoppoint)
		# print (upstart,upstop)

		plt.subplot(3,1,1)
		plt.plot(np.arange(len(userdata[3])),userdata[1] , 'b')
		plt.axvline(upstart,color='black',linestyle='--')
		plt.axvline(upstop,color='black',linestyle='--')
		plt.axvline(upstartpoint,color='green',linestyle='--')
		plt.axvline(upstoppoint,color='green',linestyle='--')
		plt.axvline(downstartpoint,color='g',linestyle='--')
		plt.axvline(downstoppoint,color='g',linestyle='--')
		
		plt.subplot(3,1,2)
		plt.plot(np.arange(len(userdata[4])),userdata[2] , 'b')
		plt.axvline(upstart,color='black',linestyle='--')
		plt.axvline(upstop,color='black',linestyle='--')
		# plt.axvline(upstartpoint,color='green',linestyle='--')
		# plt.axvline(upstoppoint,color='green',linestyle='--')
		# plt.axvline(downstartpoint,color='g',linestyle='--')
		# plt.axvline(downstoppoint,color='g',linestyle='--')
		plt.subplot(3,1,3)
		plt.plot(np.arange(len(userdata[5])),userdata[3] , 'b')
		plt.axvline(upstart,color='black',linestyle='--')
		plt.axvline(upstop,color='black',linestyle='--')
		# plt.axvline(upstartpoint,color='green',linestyle='--')
		# plt.axvline(upstoppoint,color='green',linestyle='--')
		# plt.axvline(downstartpoint,color='g',linestyle='--')
		# plt.axvline(downstoppoint,color='g',linestyle='--')
		# plt.axvline((upstartpoint-330)/50,color='g',linestyle='--')
		# plt.axvline((upstart-330-20)/50,color='g',linestyle='--')
		# plt.axvline((downstoppoint-330)/50,color='g',linestyle='--')
		# plt.axvline((upstop-330-20)/50,color='r',linestyle='--')
		# 
		# plt.show()	
		plt.savefig('./temp/'+title[time].replace('.csv','')+".png")

		plt.close()







			


