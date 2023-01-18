import math
from typing import List

from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.Qt3DRender import Qt3DRender
from PySide6.QtGui import QVector3D, QFont
from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DCore import Qt3DCore


class SkeletonView(QWidget):
	_window: Qt3DExtras.Qt3DWindow
	_container: QWidget
	_camera: Qt3DRender.QCamera
	_controller: Qt3DExtras.QOrbitCameraController
	_root: Qt3DCore.QEntity
	_keypoints: List[Qt3DCore.QEntity]

	def __init__(self, *args, **kwargs):
		super(SkeletonView, self).__init__(*args, **kwargs)

		self._window = Qt3DExtras.Qt3DWindow()
		self._window.defaultFrameGraph().setClearColor(QtGui.QColor("#a5bde8"))

		self._container = QtWidgets.QWidget.createWindowContainer(self._window)

		screen_size = self._window.size()
		self._container.setMinimumSize(QtCore.QSize(200, 100))
		self._container.setMaximumSize(screen_size)

		self._camera = self._window.camera()

		self._camera.lens().setPerspectiveProjection(45.0, 1.0, 0.1, 10000.0)
		self._camera.setPosition(QtGui.QVector3D(20.0, 0.0, 0.0))
		self._camera.setUpVector(QtGui.QVector3D(0, 1, 0))
		self._camera.setViewCenter(QtGui.QVector3D(0, 0, 0))

		self._root = Qt3DCore.QEntity()
		self._controller = Qt3DExtras.QOrbitCameraController(self._root)
		self._controller.setLinearSpeed(150.0)
		self._controller.setLookSpeed(180.0)
		self._controller.setCamera(self._camera)

		self._window.setRootEntity(self._root)

		layout = QHBoxLayout()
		layout.addWidget(self._container)
		self.setLayout(layout)

		self._keypoints = []

	def draw_line(self, start, end):
		vec = end[0] - start[0], end[1] - start[1], end[2] - start[2]
		length = math.hypot(*vec)
		edge = Qt3DCore.QEntity(self._root)

		cylinder = Qt3DExtras.QCylinderMesh(edge)
		cylinder.setLength(length)
		cylinder.setRadius(0.3)

		x_angle = math.atan(math.sqrt(math.pow(vec[2], 2) + math.pow(vec[0], 2)) / vec[1]) / math.pi * 180
		y_angle = 0 if vec[0] == 0 and vec[2] == 0 else math.atan(vec[0] / vec[2]) / math.pi * 180

		transform = Qt3DCore.QTransform(edge)
		transform.setRotationX(x_angle)
		transform.setRotationY(y_angle)
		transform.setTranslation(
			QVector3D(
				(end[0] + start[0]) / 2,
				(end[1] + start[1]) / 2,
				(end[2] + start[2]) / 2
			)
		)

		material = Qt3DExtras.QPhongMaterial(edge)
		material.setDiffuse("#ffff00")

		edge.addComponent(cylinder)
		edge.addComponent(transform)
		edge.addComponent(material)

	def clear(self):
		for keypoint in self._keypoints:
			keypoint.setParent(None)
		self._keypoints = []

	def draw_keypoint(self, x, y, z, color):
		keypoint = Qt3DCore.QEntity(self._root)

		sphere = Qt3DExtras.QSphereMesh(keypoint)
		sphere.setRadius(10)

		transform = Qt3DCore.QTransform(keypoint)
		transform.setTranslation(QVector3D(x, y, z))

		material = Qt3DExtras.QPhongMaterial(keypoint)
		material.setDiffuse("#ff0000")
		if color:
			material.setDiffuse(color)

		keypoint.addComponent(sphere)
		keypoint.addComponent(transform)
		keypoint.addComponent(material)

		self._keypoints.append(keypoint)


	def set_camera(self, x, y, z, cam_pos_x, cam_pos_y, cam_pos_z):
		self._camera.setViewCenter(QVector3D(x, y, z))
		self._camera.setPosition(QVector3D(cam_pos_x, cam_pos_y, cam_pos_z))
