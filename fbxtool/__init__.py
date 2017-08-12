# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-08-12

"""FBX解析类"""

"""
解析FBX工具
1. 面数
2. 顶点数
3. 网格数
4. 骨骼数量
5. 材质
6. 纹理
"""

import fbx
import FbxCommon

from fbxmeshinfo import CFBXMeshInfo

from model import CModel
from mesh import CMesh
from material import CMaterial
from anim import CAnimation
from node import CNode
from tool import TransValue
from tool import GetGeometryName
from tool import NewPrint


class CFBXParse(object):
	def __init__(self, sPath):
		lManager, lScene = FbxCommon.InitializeSdkObjects()
		self.m_Result = FbxCommon.LoadScene(lManager, lScene, sPath)
		if not self.m_Result:
			print "Load FBX Failed!"
			return

		self.m_Manager = lManager
		self.m_Scene = lScene
		# lManager.Destroy()

		# FBXInfo Map
		self.m_FBXMeshInfo = []  # [CFbxMeshInfo]
		self.m_FBXMeshMap = {}  # {FbxGeometry: [CFbxMeshInfo]}
		self.m_MaterialsMap = {}  # {FbxSurfaceMaterial: CMaterial}
		self.m_TextureFiles = {}  # {FileName: TextureFileInfo}
		self.m_NodeMap = {}  # {FbxNode: CNode}

		self.PrefetchMeshes()
		self.FetchMaterials()

	def ParseFBX(self, oModel):
		"""解析FBX"""
		oModel.m_Materials = self.m_MaterialsMap.values()
		self.AddMesh(oModel)
		self.AddNode(oModel)
		for oNode in oModel.m_Nodes:
			self.UpdateNode(oModel, oNode)
		self.AddAnimations(oModel)

	def PrefetchMeshes(self):
		"""预处理网格，保存网格数据{FbxGeometry: [CFbxMeshInfo]}"""
		cnt = self.m_Scene.GetGeometryCount()  # 几何图元数量
		for i in xrange(cnt):
			oGeometry = self.m_Scene.GetGeometry(i) # fbx.FbxGeometry
			if not isinstance(oGeometry, fbx.FbxMesh):
				print "[%s] Skipping geometry, because it can't be triangulated" % oGeometry.GetClassId().GetName()
				continue
			oMesh = oGeometry
			if oMesh.GetElementMaterialCount() <= 0:
				print "[%s] Skipping geometry without material" % GetGeometryName(oMesh)
				continue
			oFbxMeshInfo = CFBXMeshInfo(oMesh)
			self.m_FBXMeshInfo.append(oFbxMeshInfo)
			if oMesh not in self.m_FBXMeshMap:
				self.m_FBXMeshMap[oMesh] = []
			self.m_FBXMeshMap[oMesh].append(oFbxMeshInfo)

	def FetchMaterials(self):
		"""处理材质，保存材质数据{FbxSurfaceMaterial: CMaterial}"""
		cnt = self.m_Scene.GetMaterialCount():
		for i in xrange(cnt):
			oFbxMaterial = self.m_Scene.GetMaterial(i)  # fbx.FbxSurfacePhong/fbx.FbxSurfaceLambert/fbx.FbxSurfaceMaterial
			oMaterial = CMaterial()
			self.m_TextureFiles = oMaterial.InitMaterial(oFbxMaterial)
			oMaterial.m_TextureFiles = []
			self.m_MaterialsMap[oFbxMaterial] = oMaterial

	def AddMesh(self, oModel, oNode=None):
		"""统计网格"""
		if not oNode:
			oNode = self.m_Scene.GetRootNode()
		childCount = oNode.GetChildCount()
		for i in xrange(childCount):
			self.AddMesh(oModel, oNode.GetChild(i))

		oGeometry = oNode.GetGeometry()
		if oGeometry not in self.m_FBXMeshMap:
			return
		for oMeshInfo in self.m_FBXMeshMap[oGeometry]:
			oMesh = CMesh(oMeshInfo)
			oModel.m_Meshes.append(oMesh)

	def AddNode(self, oModel, oParent=None, oFbxNode=None):
		"""统计节点"""
		if not oFbxNode:
			rootNode = self.m_Scene.GetRootNode()
			for i in xrange(rootNode.GetChildCount()):
				self.AddNode(oModel, oParent, rootNode.GetChild(i))
			return
		oNode = CNode(oFbxNode)
		self.m_NodeMap[oFbxNode] = oNode

		if not oParent:
			oModel.m_Nodes.append(oNode)
		else:
			oParent.m_Children.append(oNode)

		for i in xrange(oFbxNode.GetChildCount()):
			self.AddNode(oModel, oNode, oFbxNode.GetChild(i))

	def UpdateNode(self, oModel, oNode):
		mat = oNode.m_Source.EvaluateLocalTransform()
		oNode.m_Transform["translation"] = TransValue(mat.GetT())
		oNode.m_Transform["rotation"] = TransValue(mat.GetQ())
		oNode.m_Transform["scale"] = TransValue(mat.GetS())

		for i in xrange(4):
			for j in xrange(4):
				oNode.m_Transforms[i*4+j] = TransValue(mat.Get(i, j))

		oGeometry = oNode.m_Source.GetGeometry()
		if oGeometry in self.m_FBXMeshMap:
			for oMeshInfo in self.m_FBXMeshMap[oGeometry]:
				for oCluster in oMeshInfo.m_SourceBone:
					oFbxNode = oCluster.GetLink()
					oNode.m_Bones.append((self.m_NodeMap[oFbxNode], oCluster))

		for oChildNode in oNode.m_Children:
			self.UpdateNode(oModel, oChildNode)

	def AddAnimations(self, oModel):
		"""统计动画"""
		animCount = self.m_Scene.GetSrcObjectCount(fbx.FbxCriteria.ObjectType(fbx.FbxAnimStack.ClassId))
		for in xrange(animCount):
			self.AddAnimation(oModel, self.m_Scene.GetSrcObject(fbx.FbxCriteria.ObjectType(fbx.FbxAnimStack.ClassId), i))

	def AddAnimation(self, oModel, oFbxAnimStack):
		oAnimation = CAnimation()
		oModel.m_Animations.append(oAnimation)
		oAnimation.m_ID = oFbxAnimStack.GetName()

		animTimeSpan = oFbxAnimStack.GetLocalTimeSpan()
		oAnimation.m_Length = animTimeSpan.GetStop().GetMilliSeconds() / 1000.0
