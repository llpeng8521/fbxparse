# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-08-12

"""节点树"""


class CNode(object):
	"""节点"""
	m_ID = ""
	m_Source = None  # FbxNode

	m_Transform = {
		"translation": (0.0, 0.0, 0.0),
		"rotation": (0.0, 0.0, 0.0, 0.0),
		"scale": (0.0, 0.0, 0.0),
	}
	m_Transforms = [0.0] * 16

	def __init__(self, oFbxNode):
		self.m_ID = oFbxNode.GetName()
		self.m_Source = oFbxNode

		self.m_Bones = []  # [(CNode, FbxAMatrix)]
		self.m_Children = []  # CNode

	def GetInfo(self):
		dInfo = {
			"id": self.m_ID,
		}
		lChildInfo = []
		for oNode in self.m_Children:
			lChildInfo.append(oNode.GetInfo())
		if lChildInfo:
			dInfo["children"] = lChildInfo

		if self.m_Bones:
			dInfo["bones"] = []
			for oNode, fbxmat in self.m_Bones:
				dInfo["bones"].append({"node": oNode.m_ID})
		return dInfo
