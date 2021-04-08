# -*- coding: utf-8 -*-
from django.http import HttpResponse
import numpy as np
import json
from sklearn.externals import joblib
from . import extra
from sklearn import svm
from django.http import JsonResponse
from ast import literal_eval
from datetime import datetime
def IA(request):
	# print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

	obj = request.FILES.get("csv")
	print (obj)
	str={}
	if obj:
		data=obj.name
		print(data)
		data=literal_eval(data)
		print(data['id'],data['time'])
		filename='D:/IA/IA/tempdata/'+data['time']+'.csv'
		# filename='D:/IA/IA/tempdata/'+data['id']+'-'+data['time']+'.csv'
		

		f = open(filename,'wb')
		for line in obj.chunks():
			f.write(line)
		f.close()
		# filename='D:/IA/IA/tempdata/hy-2019-1-27-13-51-57.csv'
		# print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

 


		# testdata=extra.extrafeature(filename)
		# # print(len(testdata))
		# indexnum=[74, 2, 0, 24, 36, 13, 17, 15, 80, 6, 41, 39, 16, 14, 86, 21, 23, 107, 40, 105, 47, 43, 106, 30, 97, 84, 91, 101, 19, 45, 102, 89, 88, 1, 95, 94, 99, 38, 92, 87, 85, 100, 93, 78, 98, 73, 27, 46, 20, 22]
		# featurecom=[[]]
		# for i in indexnum:
		# 	featurecom[0].append(testdata[i])
		# lda=joblib.load('D:/IA/IA/lda.pkl')
		# featurecom=lda.transform(featurecom)
		# print(featurecom)
		# clf=joblib.load('D:/IA/IA/svm.pkl')
		# pretarget=clf.predict_proba(featurecom)
		# print (pretarget)
		# if pretarget[0][int(data['id'])]>0.2:
		# 	str[data['id']]=['true']
		# else:
		# 	str[data['id']]=['false']
		# print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
		str[data['id']]=['true']
		print(str)
		return JsonResponse(str)

	# return HttpResponse("IA ")


