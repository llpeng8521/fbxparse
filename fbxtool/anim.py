# -*- coding:utf-8-*-
# Created by Li Lepeng on 2017-08-12

"""FBX动画"""


class CAnimation(object):
	"""动画"""
	m_ID = ""
	m_Length = 0  # 时间秒

	def GetInfo(self):
		dInfo = {
			"id": self.m_ID,
			"length": self.m_Length
		}
		return dInfo
