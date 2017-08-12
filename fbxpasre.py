# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-08-12

import os
import sys


def FbxParse(sFbxPath):
	from fbxtool import CFBXParse
	from fbxtool import CModel
	sFilePath = os.path.splitext(sFbxPath)[0] + ".json"
	print sFbxPath, sFilePath
	oFBX = CFBXParse(sFbxPath)
	if not oFBX.m_Result:
		print "解析FBX失败: ", sFbxPath
		return
	oModel = CModel()
	oFBX.ParseFBX(oModel)

	import json
	with open(sFilePath, "w") as f:
		json.dump(oModel.GetInfo(), f, indent=4)


if __name__ == '__main__':
	argv = sys.argv
	sPath = argv[1]
	if os.path.isdir(sPath):
		for root, dirs, files in os.walk(sPath):
			for sFile in files:
				sFile = sFile.lower()
				if not sFile.endwith(".fbx"):
					continue
				sPath = os.path.join(root, sFile)
				FbxParse(sPath)
	else:
		FbxParse(sPath)
