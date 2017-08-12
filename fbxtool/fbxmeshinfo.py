# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-08-12

"""FBX网格信息"""

import fbx
from attribute import CAttribute


class CFBXMeshInfo(object):
	m_ID = ""
	m_FbxMesh = None
	m_PointCount = 0  # 顶点数
	m_PolyCount = 0  # 多边形数(面数)

	# 顶点属性
	m_UsePackedColors = False  # Whether to ues packed colors
	m_VertexBlendWeightCount = 4  # 每个顶点的Blend weights数量(最大是4)
	m_UVCount = 0
	m_Attribute = None

	# 骨骼属性
	m_Skin = 0  # FbxSkin
	m_SourceBone = []  # [FbxCluster]

	def __init__(self, FbxMesh):
		self.m_FbxMesh = FbxMesh
		self.m_ID = FbxMesh.GetName()
		self.m_PointCount = FbxMesh.GetControlPointsCount()
		self.m_PolyCount = FbxMesh.GetPolygonCount()

		# 顶点属性
		self.m_Attribute = CAttribute()
		self.m_UVCount = min(8, FbxMesh.GetElementUVCount())
		self.FetchAttributes()

		# 骨骼属性
		if FbxMesh.GetDeformerCount(fbx.FbxDeformer.eSkin) > 0:
			self.m_Skin = FbxMesh.GetDeformer(0, fbx.FbxDeformer.eSkin)
			self.FetchClusters()

	def FetchAttributes(self):
		"""获取顶点属性"""
		self.m_Attribute.SetHasPosition(True)
		self.m_Attribute.SetHasNormal(self.m_FbxMesh.GetElementNormalCount() > 0)
		self.m_Attribute.SetHasColor((not self.m_UsePackedColors) and (self.m_FbxMesh.GetElementVertexColorCount() > 0))
		self.m_Attribute.SetHasColorPacked(self.m_UsePackedColors and (self.m_FbxMesh.GetElementVertexColorCount() > 0))
		self.m_Attribute.SetHasTangent(self.m_FbxMesh.GetElementTangentCount() > 0)
		self.m_Attribute.SetHasBinormal(self.m_FbxMesh.GetElementBinormalCount() > 0)
		for i in xrange(8):
			self.m_Attribute.SetHasUV(i, i < self.m_UVCount)
		for i in xrange(8):
			self.m_Attribute.SetHasBlendWeight(i, i < self.m_VertexBlendWeightCount)

	def FetchClusters(self):
		self.m_SourceBone = []
		clusterCount = self.m_Skin.GetClusterCount()
		for i in xrange(clusterCount):
			self.m_SourceBone.append(self.m_Skin.GetCluster(i))
