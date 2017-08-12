# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-08-12

"""通用工具"""

import fbx
import pprint


def TransValue(values):
	if isinstance(values, (fbx.FbxDouble2, fbx.FbxVector2)):
		return list(values)
	elif isinstance(values, (fbx.FbxDouble3, )):
		return list(values)
	elif isinstance(values, (fbx.FbxDouble4, fbx.FbxVector4)):
		return list(values)
	else:
		return values


def GetGeometryName(oGeometry):
	sName = oGeometry.GetName()
	if sName:
		return sName
	cnt = oGeometry.GetNodeCount()
	for i in xrange(cnt):
		sName = oGeometry.GetNode(i).GetName()
		if sName:
			return "shape(%s)" % sName
	return ""


def NewPrint(info):
	print "*" * 20 + "\n" + pprint.pformat(info)
	print "*" * 20


def WriteFile(path, data):
	f = open(path, "w")
	try:
		f.write("FBXDATA = ")
		f.write(pprint.pformat(data, indent=2))
	except IOError, e:
		print "创建%s失败"， data
		print e
	finally:
		f.close()
