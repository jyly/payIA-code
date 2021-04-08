# -*- coding=utf-8 -*-
from os import listdir,makedirs,path
import numpy as np

# 1加速计，2陀螺仪，3线性加速计，4磁感计，5方向计，7应用开启，8打开摄像头，9摄像头关闭



def timewrap(readpath,writepath,winsize):

	tempdata=[[] for i in range(5)]
	upstart=-1
	upstop=-1

	print (readpath)
	print (writepath)
	input_1=open(readpath,'r+')
	for row in input_1:
		row=list(eval(row))	
				
		if(row[0]==8):
			upstart=row[4]
			continue
		if(row[0]==9):
			upstop=row[4]
			continue	
		flag=0		
		for i in range(1,4):
			if row[i]==99.0:
				flag=1	
		# print (int(row[0]))
		if flag==0:
			tempdata[int(row[0])-1].append(row[1:])
	# print (upstart,upstop)
	if (upstart==-1) or (upstop==-1):
		print("文件错误")
		return

	input_1.close()

	userdata=[[] for i in range(16)]

	timerule=0
	lastrow=[0,0,0,0]
	#用于分段
	output_1=open(writepath,'w+')

	for j in range(len(tempdata[0])):
		if timerule==0:
			timerule=tempdata[0][j][3]+50
			for k in range(4):
				lastrow[k]=tempdata[0][j][k]
			continue
		while tempdata[0][j][3]>timerule+winsize:
			timerule=timerule+winsize
			k=float(timerule-lastrow[3])/(tempdata[0][j][3]-lastrow[3])
			for t in range(0,3):
				userdata[t].append(lastrow[t]+k*(tempdata[0][j][t]-lastrow[t]))
			userdata[15].append(timerule)	
		for k in range(0,4):
			lastrow[k]=tempdata[0][j][k]



	for i in range (1,5):
		for j in range(3):
			userdata[i*3+j].append(tempdata[i][0][j])
			lastrow[j]=tempdata[i][0][j]
		timerule=userdata[15][0]
		lastrow[3]=userdata[15][0]	
		for j in range(0,len(tempdata[i])):
			while tempdata[i][j][3]>timerule+winsize:
				timerule=timerule+winsize
				k=float(timerule-lastrow[3])/(tempdata[i][j][3]-lastrow[3])
				for t in range(0,3):
					userdata[i*3+t].append(lastrow[t]+k*(tempdata[i][j][t]-lastrow[t]))
			for k in range(0,4):
				lastrow[k]=tempdata[i][j][k]
		# 若数据长度不足，则以最后一位替补		
		maxnum=len(userdata[15])-len(userdata[i*3])
		while maxnum>0:
			for j in range(3):
				userdata[i*3+j].append(lastrow[j])
			maxnum=maxnum-1


	# for i in range(15):
		# print(len(userdata[i]))

	upstartflag=0	
	upstopflag=0	
	for i in range(len(userdata[15])):
		if 	0==upstartflag and userdata[15][i]>upstart:
			for j in range(15):
				output_1.write(str(88.0)+',')
				# userdata[j].append(99.0,i)
			output_1.write(str(upstart)+',')
			output_1.write('\n')
			upstartflag=1
		if 	0==upstopflag and userdata[15][i]>upstop:
			for j in range(15):
				output_1.write(str(99.0)+',')
				# userdata[j].append(99.0,i)
			output_1.write(str(upstop)+',')
			output_1.write('\n')
			upstopflag=1	
		for j in range(16):
			# print (i,j)
			output_1.write(str(userdata[j][i])+',')
		output_1.write('\n')
		

	output_1.close()



# user=['tzh','djb','zzc','ygy','ln']
# user=['ln']

# for name in range(0,len(user)):#遍历不同的目录
# 	title=listdir('./tempdata/wechat'+'/'+user[name]+'/') 
# 	folder = path.exists('./final/wechat'+'/'+user[name]+'/')
# 	if not folder:
# 		makedirs('./final/wechat'+'/'+user[name]+'/')

# 	for time in range(0,len(title)):#遍历不同时间的文件
# 		readpath='./tempdata/wechat'+'/'+user[name]+'/'+title[time]
# 		writepath='./final/wechat'+'/'+user[name]+'/'+title[time]
# 		timewrap(readpath,writepath,20)


# for name in range(0,len(user)):#遍历不同的目录
# 	title=listdir('./tempdata/alipay'+'/'+user[name]+'/') 
# 	folder = path.exists('./final/alipay'+'/'+user[name]+'/')
# 	if not folder:
# 		makedirs('./final/alipay'+'/'+user[name]+'/')

# 	for time in range(0,len(title)):#遍历不同时间的文件
# 		readpath='./tempdata/alipay'+'/'+user[name]+'/'+title[time]
# 		writepath='./final/alipay'+'/'+user[name]+'/'+title[time]
# 		timewrap(readpath,writepath,20)
