# _*_ coding: utf-8 _*_
from os import listdir

def predatawrite(data,target,path):
	output_1=open(path,"w+")
	for i in range(0,len(target)):
		output_1.write(str(target[i])+",")
		fealen=len(data[i])
		for j in range(0,fealen):
			output_1.write(str(data[i][j])+",")
		output_1.write("\n")
	output_1.close()

def predataread(path):
	target=[]
	dataset=[]
	input_1=open(path,"r+")
	num=0
	for row in input_1:
		dataset.append([])
		row=list(eval(row))
		target.append(row[0])	
		for i in range(1,len(row)):
			dataset[num].append(row[i])
		num=num+1	
	input_1.close()
	return dataset,target


