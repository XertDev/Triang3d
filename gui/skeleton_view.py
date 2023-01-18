import math
from typing import List, Any

import numpy as np
from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout
from matplotlib import artist, cbook
from matplotlib.axes import Axes

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure

## dirty fix
import mpl_toolkits.mplot3d.art3d
from mpl_toolkits.mplot3d import proj3d
from matplotlib import (
	artist, cbook, text as mtext)


# Fixed method
def _norm_text_angle(a):
	a = (a + 180) % 180
	if a > 90:
		a = a - 180
	return a


@artist.allow_rasterization
def draw(self, renderer):
	position3d = np.array((self._x, self._y, self._z))
	proj = proj3d.proj_trans_points(
		[position3d, position3d + self._dir_vec], self.axes.M)
	angle = 1
	with cbook._setattr_cm(self, _x=proj[0][0], _y=proj[1][0], _rotation=_norm_text_angle(angle)):
		mtext.Text.draw(self, renderer)
	self.stale = False


mpl_toolkits.mplot3d.art3d.Text3D.draw = draw


class PlotCanvas3D(FigureCanvasQTAgg):
	axes: Axes

	def __init__(self):
		self.fig = Figure()
		self.axes = self.fig.add_subplot(111, projection="3d")

		super(PlotCanvas3D, self).__init__(self.fig)
		FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
		FigureCanvasQTAgg.updateGeometry(self)
		self.axes.mouse_init()

	def clear(self):
		self.axes.cla()

	def update_graph(self):
		self.draw()


class SkeletonView(QWidget):
	_canvas: PlotCanvas3D
	_keypoints_x: List[Any]
	_keypoints_y: List[Any]
	_keypoints_z: List[Any]
	_keypoints_l: List[Any]
	_bones: List[Any]
	_toolbar: NavigationToolbar2QT

	def __init__(self, *args, **kwargs):
		super(SkeletonView, self).__init__(*args, **kwargs)

		self._canvas = PlotCanvas3D()
		# self._toolbar = NavigationToolbar2QT(self._canvas, self)

		layout = QVBoxLayout()
		layout.addWidget(self._canvas)
		# layout.addWidget(self._toolbar)
		self.setLayout(layout)

		self._keypoints_x = []
		self._keypoints_y = []
		self._keypoints_z = []
		self._keypoints_l = []
		self._bones = []

	def draw_line(self, start, end):
		self._bones.append((start[0], start[1], start[2], end[0], end[1], end[2]))

	def clear(self):
		self._canvas.clear()
		self._keypoints_x = []
		self._keypoints_y = []
		self._keypoints_z = []
		self._keypoints_l = []
		self._bones = []

	def add_keypoint(self, x, y, z, label):
		self._keypoints_x.append(x)
		self._keypoints_y.append(y)
		self._keypoints_z.append(z)
		self._keypoints_l.append(label)

	def draw(self):
		self._canvas.axes.scatter(self._keypoints_y, self._keypoints_x, self._keypoints_z, c='b')

		for i, label in enumerate(self._keypoints_l):
			self._canvas.axes.text(self._keypoints_y[i], self._keypoints_x[i], self._keypoints_z[i], label)
		for bone in self._bones:
			self._canvas.axes.plot([bone[1], bone[4]], [bone[0], bone[3]], [bone[2], bone[5]])

		self._canvas.update_graph()
