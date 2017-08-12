# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-08-12

"""网格"""


class CMesh(object):
	"""网格"""

	m_Attribute = None  # attribute.CAttribute
	m_Source = None

	def __init__(self, oFbxMeshInfo):
		self.m_Source = oFbxMeshInfo
		self.m_Attribute = oFbxMeshInfo.m_Attribute

	def GetInfo(self):
		dInfo = {
			"attributes": self.m_Attribute.GetInfo(),
			"vertices_count": self.m_Source.m_PointCount,
			"poly_count": self.m_Source.m_PolyCount,
			"indices_count": self.m_Source.m_PolyCount * 3,
		}
		return dInfo
