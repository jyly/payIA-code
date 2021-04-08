# _*_ coding: utf-8 _*_
from os import listdir
from datafilt import dataextra

user=['djb','zzc','tzh','ln']

for filenum in range (10,11,10):
	for name in range(0,len(user)):#遍历不同的目录
		title=listdir('./data/wechat/'+user[name]+'/') 
		# for time in range(0,len(title)):#遍历不同时间的文件
		alllen=0
		for time in range(0,filenum):#遍历不同时间的文件
			path='./data/wechat/'+user[name]+'/'+title[time]
			print(path)
			upstart,upstop,tempuserdata=dataextra(path)
			alllen=alllen+len(tempuserdata[0])
		print(alllen/10*0.02)	