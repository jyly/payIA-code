# -*- coding=utf-8 -*-
from os import listdir,makedirs,path
import numpy as np

# 1加速计，2陀螺仪，3线性加速计，4磁感计，5方向计，7应用开启，8打开摄像头，9摄像头关闭



def timewrap(readpath,writepath,user,winsize):
	for name in range(0,len(user)):#遍历不同的目录
		title=listdir(readpath+user[name]+'/') 
		folder = path.exists(writepath+user[name]+'/')
		if not folder:
			makedirs(writepath+user[name]+'/')

		for time in range(0,len(title)):#遍历不同时间的文件
		# for time in range(0,2):#遍历不同时间的文件
			tempdata=[[] for i in range(5)]

			workstart=-1
			upstart=-1
			upstop=-1

			inpath=readpath+'/'+user[name]+'/'+title[time]
			outpath=writepath+'/'+user[name]+'/'+title[time]
			print (inpath)
			print (outpath)
			input_1=open(inpath,'r+')
			for row in input_1:
				row=list(eval(row))	
				if(row[0]==7):
					workstart=row[4]
					continue 		
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
				continue

			input_1.close()

			userdata=[[] for i in range(16)]

			timerule=0
			lastrow=[0,0,0,0]
			#用于分段
			output_1=open(outpath,'w+')

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

			workstartflag=0	
			upstartflag=0	
			upstopflag=0	
			for i in range(len(userdata[15])):
				if 	0==workstartflag and userdata[15][i]>workstart:
					for j in range(15):
						output_1.write(str(77.0)+',')
						# userdata[j].append(99.0,i)
					output_1.write(str(workstart)+',')
					output_1.write('\n')
					workstartflag=1
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

# user=['hy','tzh','djb','zzc','ygy','ln','yw']
# user=['hy','tzh','djb','ygy','yw']
user=['tzh','djb','zzc','ygy','ln']

readpath='./final/wechat'
writepath='./tempdata/wechat'
timewrap(readpath,writepath,user,20)