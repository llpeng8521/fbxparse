# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-08-12

"""材质"""

import fbx
from FbxCommon import *
from tool import TransValue
from tool import NewPrint


class CMaterial(object):
	"""材质"""
	m_ID = ""
	m_Diffuse = [0.0, 0.0, 0.0]  # 漫反射光照
	m_Ambient = [0.0, 0.0, 0.0]  # 环境光照
	m_Emissive = [0.0, 0.0, 0.0]  # 放射光照
	m_Specular = [0.0, 0.0, 0.0]  # 镜面光照
	m_Shininess = 0  # 高光(的发光值)
	m_Opacity = 0  # 透明度
	m_Textures = []
	m_Source = None  # fbx.FbxSurfacePhong/fbx.FbxSurfaceLambert/fbx.FbxSurfaceMaterial

	m_TextureFiles = {}

	def InitMaterial(self, oFbxMaterial):
		self.m_TextureFiles = {}
		self.m_Source = oFbxMaterial
		self.m_ID = oFbxMaterial.GetName()

		# 1.判断FbxSurfaceMaterial材质
		if not isinstance(oFbxMaterial, fbx.FbxSurfaceLambert):
			self.m_Diffuse = [1.0, 1.0, 1.0]
			return

		# 2.判断FbxSurfaceLambert材质
		# 设置材质属性
		if oFbxMaterial.Ambient.IsValid():
			self.m_Ambient = TransValue(oFbxMaterial.Ambient.Get())
		if oFbxMaterial.Diffuse.IsValid():
			self.m_Diffuse = TransValue(oFbxMaterial.Diffuse.Get())
		if oFbxMaterial.Emissive.IsValid():
			self.m_Emissive = TransValue(oFbxMaterial.Emissive.Get())

		# 设置透明度
		if oFbxMaterial.TransparencyFactor.IsValid() and oFbxMaterial.TransparentColor.IsValid():
			fFactor = 1.0 - TransValue(oFbxMaterial.TransparencyFactor.Get())
			tColor = TransValue(oFbxMaterial.TransparentColor.Get())
			fOpacity = (tColor[0] * fFactor + tColor[1] * fFactor + tColor[2] * fFactor) / 3.0
			self.m_Opacity = fOpacity
		elif oFbxMaterial.TransparencyFactor.IsValid():
			self.m_Opacity = 1.0 - TransValue(oFbxMaterial.TransparentColor.Get())
		elif oFbxMaterial.TransparentColor.IsValid():
			tColor = TransValue(oFbxMaterial.TransparentColor.Get())
			self.m_Opacity = (tColor[0] + tColor[1] + tColor[2]) / 3.0

		dMap = CTexture.m_UsageMap
		self._addTextures(oFbxMaterial.Ambient, dMap["Ambient"])
		self._addTextures(oFbxMaterial.Diffuse, dMap["Diffuse"])
		self._addTextures(oFbxMaterial.Emissive, dMap["Emissive"])
		self._addTextures(oFbxMaterial.Bump, dMap["Bump"])
		self._addTextures(oFbxMaterial.NormalMap, dMap["NormalMap"])
		self._addTextures(oFbxMaterial.TransparentColor, dMap["Transparency"])

		if not isinstance(oFbxMaterial, fbx.FbxSurfacePhong):
			return

		# 3.判断FbxSurfacePhong材质
		# 设置镜像光照和高光
		if oFbxMaterial.Specular.IsValid():
			self.m_Specular = TransValue(oFbxMaterial.Specular.Get())
		if oFbxMaterial.Shininess.IsValid():
			self.m_Shininess = TransValue(oFbxMaterial.Shininess.Get())

		self._addTextures(oFbxMaterial.Specular, dMap["Specular"])
		self._addTextures(oFbxMaterial.Reflection, dMap["Reflection"])
		return self.m_TextureFiles

	def _addTextures(self, oFbxProp, nType):
		def RecursivefindTexture(oFbxTexture, i, nType):
			if isinstance(oFbxTexture, fbx.FbxFileTexture):
				self.m_Textures.append(self._createTexture(oFbxTexture, nType))
			elif isinstance(oFbxTexture, fbx.FbxTexture):
				for i in xrange(oFbxTexture.GetSrcObjectCount()):
					RecursivefindTexture(oFbxTexture, i, nType)

		cnt = oFbxProp.GetSrcObjectCount()
		for i in xrange(cnt):
			oFbxTexture = oFbxProp.GetSrcObject(i)
			if isinstance(oFbxTexture, fbx.FbxFileTexture):
				self.m_Textures.append(self._createTexture(oFbxTexture, nType))
			elif isinstance(oFbxTexture, fbx.FbxTexture):
				for i in xrange(oFbxTexture.GetSrcObjectCount()):
					RecursivefindTexture(oFbxTexture, i, nType)

	def _createTexture(self, oFbxFileTexture, nType=0):
		if not oFbxFileTexture:
			return 0
		oResult = CTexture(oFbxFileTexture, nType)
		self.m_TextureFiles[oResult.m_FileName] = oResult
		return oResult

	def GetInfo(self):
		lTextureInfo = []
		for oTexture in self.m_Textures:
			lTextureInfo.append(oTexture.GetInfo())
		dInfo = {
			"id": self.m_ID,
			"ambient": self.m_Ambient,
			"diffuse": self.m_Diffuse,
			"emissive": self.m_Emissive,
			"opacity": self.m_Opacity,
			"specular": self.m_Specular,
			"shininess": self.m_Shininess,
			"specularFactor": 0.0,
			"textures": lTextureInfo,
		}
		return dInfo

class CTexture(object):
	"""纹理"""
	m_UsageMap = {
		"Unknown": 0,
		"None": 1,
		"Diffuse": 2,
		"Emissive": 3,
		"Ambient": 4,
		"Specular": 5,
		"Shininess": 6,
		"Normal": 7,
		"Bump": 8,
		"Transparency": 9,
		"Reflection": 10,
	}

	m_ID = ""
	m_FileName = ""
	m_Type = ""
	m_WrapModeU = ""
	m_WrapModeV = ""
	m_uvTranslation = (0.0, 0.0)
	m_uvScale = (1.0, 1.0)
	m_Source = None  # fbx.FbxFileTexture

	def __init__(self, oFbxFileTexture, nType):
		self.m_Source = oFbxFileTexture
		self.m_ID = oFbxFileTexture.GetName()
		self.m_FileName = oFbxFileTexture.GetFileName().encode("UTF-8")
		self.m_uvTranslation = TransValue(oFbxFileTexture.GetUVTranslation())
		self.m_uvScale = TransValue(oFbxFileTexture.GetUVScaling())
		self.m_Type = nType
		self.m_WrapModeU = oFbxFileTexture.GetWrapModeU()
		self.m_WrapModeV = oFbxFileTexture.GetWrapModeV()

	def GetInfo(self):
		import os
		dInfo = {
			"id": self.m_ID,
			"filename": os.path.basename(self.m_FileName),
			"type": self._getUsageMapString(self.m_Type),
			"wrapMopeU": self._getWrapModeUseString(self.m_WrapModeU),
			"wrapMopeV": self._getWrapModeUseString(self.m_WrapModeV),
		}
		return dInfo

	def _getUsageMapString(self, nType):
		for sStr, nUsageMap in CTexture.m_UsageMap.items():
			if nUsageMap == nType:
				return sStr.upper()

	def _getWrapModeUseString(self, nEWrapMode):
		if nEWrapMode == fbx.FbxFileTexture.eRepeat:
			return "REPEAT"
		elif nEWrapMode == fbx.FbxFileTexture.eClamp:
			return "CLAMP"
		else:
			return "UNKNOWN"
