# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-08-12

"""模型"""


class CModel(object):
	m_Animations = []  # anim.CAnimation对象
	m_Materials = []  # material.CMaterial对象
	m_Meshes = []  # mesh.CMesh对象
	m_Nodes = []  # node.CNode对象

	def GetInfo(self):
		dInfo = {
			"meshes": [],
			"materials": [],
			"nodes": [],
			"animations": [],
		}
		for oAnim in self.m_Animations:
			dInfo["animations"].append(oAnim.GetInfo())
		for oMaterial in self.m_Materials:
			dInfo["materials"].append(oMaterial.GetInfo())
		for oMesh in self.m_Meshes:
			dInfo["meshes"].append(oMesh.GetInfo())
		for oNode in self.m_Nodes:
			dInfo["nodes"].append(oNode.GetInfo())
		return dInfo