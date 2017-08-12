# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-08-12

"""顶点属性"""

ATTRIBUTE_UNKNOWN =      0
ATTRIBUTE_POSITION =     1
ATTRIBUTE_NORMAL =       2
ATTRIBUTE_COLOR =        3
ATTRIBUTE_COLORPACKED =  4
ATTRIBUTE_TANGENT =      5
ATTRIBUTE_BINORMAL =     6
ATTRIBUTE_TEXCOORD0 =    7
ATTRIBUTE_TEXCOORD1 =    8
ATTRIBUTE_TEXCOORD2 =    9
ATTRIBUTE_TEXCOORD3 =    10
ATTRIBUTE_TEXCOORD4 =    11
ATTRIBUTE_TEXCOORD5 =    12
ATTRIBUTE_TEXCOORD6 =    13
ATTRIBUTE_TEXCOORD7 =    14
ATTRIBUTE_BLENDWEIGHT0 = 15
ATTRIBUTE_BLENDWEIGHT1 = 16
ATTRIBUTE_BLENDWEIGHT2 = 17
ATTRIBUTE_BLENDWEIGHT3 = 18
ATTRIBUTE_BLENDWEIGHT4 = 19
ATTRIBUTE_BLENDWEIGHT5 = 20
ATTRIBUTE_BLENDWEIGHT6 = 21
ATTRIBUTE_BLENDWEIGHT7 = 22
ATTRIBUTE_COUNT =        23


AttributeNames = [
	"UNKNOWN",
	"VERTEX_ATTRIB_POSITION",
	"VERTEX_ATTRIB_NORMAL",
	"VERTEX_ATTRIB_COLOR",
	"COLORPACKED",
	"VERTEX_ATTRIB_TANGENT",
	"VERTEX_ATTRIB_BINORMAL",
	"VERTEX_ATTRIB_TEX_COORD",
	"VERTEX_ATTRIB_TEX_COORD1",
	"VERTEX_ATTRIB_TEX_COORD2",
	"VERTEX_ATTRIB_TEX_COORD3",
	"VERTEX_ATTRIB_TEX_COORD4",
	"VERTEX_ATTRIB_TEX_COORD5",
	"VERTEX_ATTRIB_TEX_COORD6",
	"VERTEX_ATTRIB_TEX_COORD7",
	"VERTEX_ATTRIB_BLEND_WEIGHT",
	"VERTEX_ATTRIB_BLEND_INDEX",
	"BLENDWEIGHT2",
	"BLENDWEIGHT3",
	"BLENDWEIGHT4",
	"BLENDWEIGHT5",
	"BLENDWEIGHT6",
	"BLENDWEIGHT7"
]

AttributeMap = {
	"VERTEX_ATTRIB_POSITION":{
		"size": 3,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_POSITION",
	}
	"VERTEX_ATTRIB_NORMAL":{
		"size": 3,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_NORMAL",
	}
	"VERTEX_ATTRIB_TEX_COORD":{
		"size": 2,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_TEX_COORD",
	}
	"VERTEX_ATTRIB_TEX_COORD1":{
		"size": 2,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_TEX_COORD1",
	}
	"VERTEX_ATTRIB_TEX_COORD2":{
		"size": 2,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_TEX_COORD2",
	}
	"VERTEX_ATTRIB_TEX_COORD3":{
		"size": 2,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_TEX_COORD3",
	}
	"VERTEX_ATTRIB_TEX_COORD4":{
		"size": 2,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_TEX_COORD4",
	}
	"VERTEX_ATTRIB_TEX_COORD5":{
		"size": 2,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_TEX_COORD5",
	}
	"VERTEX_ATTRIB_TEX_COORD6":{
		"size": 2,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_TEX_COORD6",
	}
	"VERTEX_ATTRIB_TEX_COORD7":{
		"size": 2,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_TEX_COORD7",
	}
	"VERTEX_ATTRIB_BLEND_WEIGHT":{
		"size": 4,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_BLEND_WEIGHT",
	}
	"VERTEX_ATTRIB_BLEND_INDEX":{
		"size": 4,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_BLEND_INDEX",
	}
	"VERTEX_ATTRIB_COLOR":{
		"size": 4,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_COLOR",
	}
	"VERTEX_ATTRIB_TANGENT":{
		"size": 3,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_TANGENT",
	}
	"VERTEX_ATTRIB_BINORMAL":{
		"size": 3,
		"type": "GL_FLOAT",
		"attribute": "VERTEX_ATTRIB_BINORMAL",
	}
}

class CAttribute(object):
	def __init__(self):
		self.m_Attributes = {}

	def Set(self, nAttribute, bFlag):
		if bFlag:
			self.m_Attributes[nAttribute] = bFlag
		else:
			if nAttribute in self.m_Attributes:
				del self.m_Attributes[nAttribute]

	def GetName(self, nAttribute):
		return AttributeNames[nAttribute]

	def SetHasPosition(self, bFlag):
		self.Set(ATTRIBUTE_POSITION, bFlag)

	def SetHasNormal(self, bFlag):
		self.Set(ATTRIBUTE_NORMAL, bFlag)

	def SetHasColor(self, bFlag):
		self.Set(ATTRIBUTE_COLOR, bFlag)

	def SetHasColorPacked(self, bFlag):
		self.Set(ATTRIBUTE_COLORPACKED, bFlag)

	def SetHasTangent(self, bFlag):
		self.Set(ATTRIBUTE_TANGENT, bFlag)

	def SetHasBinormal(self, bFlag):
		self.Set(ATTRIBUTE_BINORMAL, bFlag)

	def SetHasUV(self, nUV, bFlag):
		self.Set(ATTRIBUTE_TEXCOORD0 + nUV, bFlag)

	def SetHasBlendWeight(self, nIndex, bFlag):
		self.Set(ATTRIBUTE_BLENDWEIGHT0 + nIndex, bFlag)

	def GetInfo(self):
		lAttr = []
		for nAttribute in sorted(self.m_Attributes.keys()):
			sAttrName = self.GetName(nAttribute)
			if sAttrName in AttributeMap:
				lAttr.append(AttributeMap[sAttrName])
		return lAttr