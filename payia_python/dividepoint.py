# -*- coding=utf-8 -*-
import numpy as np


def div(acc,gyr,upstart,upstop):
	tol=0
	upsetpoint=0
	upsetpoint=np.argmax(gyr[upstart-50:upstop])+upstart-50
	
	upstopvalue=np.max(acc[upsetpoint:upsetpoint+5])
	upstoppoint=np.argmax(acc[upsetpoint:upsetpoint+5])+upsetpoint

	
	#寻找上升结束点
	for i in range(upsetpoint+5,upstop,5):

		if gyr[i]<0.2:
			upstopvalue=acc[i]
			upstoppoint=i
			if np.std(acc[i:i+5])<0.05 and np.std(gyr[i:i+5])<0.05:
				break	
			if acc[i]>7 and gyr[i]<0.1	and gyr[i]>-0.1:
				break
			if gyr[i]<0.1:
				break
		# if gyr[i]>0.2:
		# 	upstopvalue=acc[i]
		# 	upstoppoint=i
		# else:
		# 	if acc[i]>7 and gyr[i]<0.1	and gyr[i]>-0.1:
		# 		break
		# 	if np.std(acc[i:i+5])>0.05 or np.std(gyr[i:i+5])>0.05:
		# 		upstopvalue=acc[i]
		# 		upstoppoint=i
		# 		# else:
		# 		# 	break
		# 	else:
		# 		if np.std(acc[i:i+5])<0.05 and np.std(gyr[i:i+5])<0.05:
		# 			upstopvalue=acc[i]
		# 			upstoppoint=i
		# 			break			

	# print (upstopvalue,upstoppoint)
	upstartvalue=np.min(acc[upsetpoint-5:upsetpoint])
	upstartpoint=np.argmin(acc[upsetpoint-5:upsetpoint])+upsetpoint-5
	#寻找上升开始点


	for i in range(upsetpoint-5,upstart-100,-5):
		if gyr[i]<0.2:
			upstartvalue=np.min(acc[i-5:i])
			upstartpoint=np.argmin(acc[i-5:i])+i-5
			if acc[i]<5:
				break
			if np.std(acc[i-5:i])<0.05 and np.std(gyr[i-5:i])<0.05:
				break		
			if gyr[i]<-0.2:
				break
		# if gyr[i]>0.2:
		# 	upstartvalue=np.min(acc[i-5:i])
		# 	upstartpoint=np.argmin(acc[i-5:i])+i-5
		# else:
		# 	if acc[i]<5 and gyr[i]<-0.2:
		# 		break
		# 	if np.std(acc[i-5:i])>0.05 or np.std(gyr[i-5:i])>0.05:
		# 		tempupstartvalue=np.min(acc[i-5:i])
		# 		if tempupstartvalue<upstartvalue:
		# 			upstartvalue=tempupstartvalue
		# 			upstartpoint=np.argmin(acc[i-5:i])+i-5
		# 		# else:
		# 		# 	break
		# 	else:
		# 		if np.std(acc[i-5:i])<0.05 and np.std(gyr[i-5:i])<0.05:
		# 			upstartvalue=np.min(acc[i-5:i])
		# 			upstartpoint=np.argmin(acc[i-5:i])+i-5
		# 			break		

	# print (upstartvalue,upstartpoint)
	downsetpoint=0
	downsetpoint=np.argmin(gyr[upstoppoint:upstop+100])+upstoppoint


	downstartvalue=np.max(acc[downsetpoint-5:downsetpoint])
	downstartpoint=np.argmax(acc[downsetpoint-5:downsetpoint])+downsetpoint-5
	#寻找下降开始点
	for i in range(downsetpoint-5,upstoppoint,-5):
		# print(np.std(acc[i-5:i]))
		if gyr[i]>-0.2:
			downstartvalue=acc[i]
			downstartpoint=i
			if acc[i]>7 and gyr[i]<0.1	and gyr[i]>-0.1:
				break
			if np.std(acc[i-5:i])<0.05 and np.std(gyr[i-5:i])<0.05:
				break
			if gyr[i]>0.1:
				break	
		# if gyr[i]<-0.2:
		# 	downstartvalue=acc[i]
		# 	downstartpoint=i
		# else:
		# 	if acc[i]>7 and gyr[i]<0.1	and gyr[i]>-0.1:
		# 		break
		# 	if np.std(acc[i-5:i])>0.05 or np.std(gyr[i-5:i])>0.05:
		# 		downstartvalue=acc[i]
		# 		downstartpoint=i
		# 		# else:
		# 		# 	break
		# 	else:
		# 		if np.std(acc[i-5:i])<0.05 and np.std(gyr[i-5:i])<0.05:
		# 			downstartvalue=acc[i]
		# 			downstartpoint=i
		# 			break		



	# print (downstartvalue,downstartpoint)
	downstopvalue=np.min(acc[max(upstop+30,downsetpoint):max(upstop+30,downsetpoint)+5])
	downstoppoint=np.argmin(acc[max(upstop+30,downsetpoint):max(upstop+30,downsetpoint)+5])+max(upstop+30,downsetpoint)
	#寻找下降结束点
	for i in range(max(upstop+30,downsetpoint)+5,min(upstop+100,len(gyr)-30),5):
		if gyr[i]>-0.2:
			downstopvalue=np.min(acc[i:i+5])
			downstoppoint=np.argmin(acc[i:i+5])+i
			if np.std(acc[i:i+5])<0.05 and np.std(gyr[i:i+5])<0.05:
				break
			if acc[i]<5:
				break
			if gyr[i]>0.2:
				break				

		# if gyr[i]<-0.2:
		# 	downstopvalue=np.min(acc[i:i+5])
		# 	downstoppoint=np.argmin(acc[i:i+5])+i
		# else:
		# 	if acc[i]<5 and gyr[i]>0.2:
		# 		break 
		# 	if np.std(acc[i:i+5])>0.05 or np.std(gyr[i:i+5])>0.05:
		# 		tempdownstopvalue=np.min(acc[i:i+5])
		# 		if tempdownstopvalue<downstopvalue :
		# 			downstopvalue=tempdownstopvalue
		# 			downstoppoint=np.argmin(acc[i:i+5])+i
		# 		# else:
		# 		# 	break
		# 	else:
		# 		if np.std(acc[i:i+5])<0.05 and np.std(gyr[i:i+5])<0.05:
		# 			downstopvalue=np.min(acc[i:i+5])
		# 			downstoppoint=np.argmin(acc[i:i+5])+i
		# 			break


	# print (workstart,upstop,downstartpoint)
	# print (upstartpoint,upstoppoint,downstoppoint,downstoppoint)
	return upstartpoint,upstoppoint,downstartpoint,downstoppoint
