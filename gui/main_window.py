import enum
import logging
import os
import time
from typing import Optional, List
import mediapipe as mp

from PySide6 import QtCore
from PySide6.QtCore import Slot, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QFileDialog, QGraphicsScene, QGraphicsPixmapItem

from model import Dataset
from service.sample_player import SamplePlayer
from service.skeletal_reconstructor import SkeletalReconstructor
from service.sample_discoverer import discover_samples
from .generated.ui_triangulator import Ui_MainWindow


VIDEO_DIR_SUFFIX = "Images"
CALIBRATION_DIR_SUFFIX = "Calibration"


class AppState(enum.Enum):
	EMPTY = 0
	DISPLAYING = 1


class MainWindow(QMainWindow, Ui_MainWindow):
	dir_path: Optional[str]
	dataset: Optional[Dataset]

	cameras: List[QGraphicsScene]

	state: AppState

	sample_player: Optional[SamplePlayer]
	skeletal_reconstructor: Optional[SkeletalReconstructor]

	pixmaps: List[QGraphicsPixmapItem]

	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)
		self.setWindowTitle("Triang 3d")

		self.state = AppState.EMPTY
		self.cameras = []
		self.pixmaps = []

		scene = QGraphicsScene()
		self.camera_tl.setScene(scene)
		self.cameras.append(scene)

		scene = QGraphicsScene()
		self.camera_tr.setScene(scene)
		self.cameras.append(scene)

		scene = QGraphicsScene()
		self.camera_bl.setScene(scene)
		self.cameras.append(scene)

		scene = QGraphicsScene()
		self.camera_br.setScene(scene)
		self.cameras.append(scene)

	def updateTree(self):
		model = QStandardItemModel()
		self.samples_tree.setModel(model)
		if self.dataset:
			for person in self.dataset.persons:
				person_item = QStandardItem(f"Person {person.id}")
				person_item.setEditable(False)

				for sequence in person.sequences:
					seq_item = QStandardItem(f"Sequence {sequence.seq_id}")
					seq_item.setData(sequence.path)
					seq_item.setEditable(False)

					person_item.appendRow(seq_item)

				model.appendRow(person_item)

	def update_vis(self):
		assert(self.state == AppState.DISPLAYING)

		frame = self.sample_player.get_frame()
		if len(self.pixmaps) > 0:
			for pixmap_item, camera in zip(self.pixmaps, self.cameras):
				camera.removeItem(pixmap_item)
			self.pixmaps = []

		pixmaps = [subframe[0] for subframe in frame]
		landmarks = [subframe[1] for subframe in frame]

		for pixmap, camera in zip(pixmaps, self.cameras):
			camera.setSceneRect(0, 0, pixmap.width(), pixmap.height())
			pixmap_item = camera.addPixmap(pixmap)
			self.pixmaps.append(pixmap_item)

		reconstructed_lines = self.skeletal_reconstructor.guide_lines_from_landmarks(landmarks)
		# for landmark_lines_key in reconstructed_lines.keys():
		# 	for line in reconstructed_lines[landmark_lines_key]:
		# 		self.skeletal.draw_line(line[0], line[1])

		keypoints_3d = self.skeletal_reconstructor.keypoint_from_guide_lines_for_landmarks(reconstructed_lines)

		# center = [0, 0, 0]
		self.skeletal.clear()

		logging.info(f"Drawing {len(keypoints_3d)} points")
		for label, keypoint in keypoints_3d.items():
			self.skeletal.add_keypoint(keypoint[0], keypoint[1], keypoint[2], label)
			# center[0] += keypoint[0]
			# center[1] += keypoint[1]
			# center[2] += keypoint[2]
		for connection in mp.solutions.pose.POSE_CONNECTIONS:
			if connection[0] in keypoints_3d.keys() and connection[1] in keypoints_3d.keys():
				start = keypoints_3d[connection[0]]
				end = keypoints_3d[connection[1]]
				self.skeletal.draw_line(start, end)

		self.skeletal.draw()

		# center[0] /= len(keypoints_3d)
		# center[1] /= len(keypoints_3d)
		# center[2] /= len(keypoints_3d)
		# extr = self.skeletal_reconstructor._calibrations[0].extrinsic_calibration
		# self.skeletal.set_camera(center[0], center[1], center[2], extr.tx * 2, extr.ty * 1.5, extr.tz * 1.5)
		#


	def update_timeline(self):
		self.timeline.blockSignals(True)
		self.timeline.setValue(self.sample_player.get_frame_index())
		self.timeline.blockSignals(False)

	@Slot(QModelIndex)
	def openSequence(self, index: QModelIndex):
		data = index.data(257)
		if data is None:
			return

		self.sample_player = SamplePlayer(os.path.join(data, VIDEO_DIR_SUFFIX))
		self.skeletal_reconstructor = SkeletalReconstructor(os.path.join(data, CALIBRATION_DIR_SUFFIX))
		self.state = AppState.DISPLAYING

		self.timeline.setMaximum(self.sample_player.get_max_frame())

		self.timeline.setEnabled(True)
		self.prev_frame.setEnabled(True)
		self.next_frame.setEnabled(True)

		self.update_vis()

	@Slot()
	def openDirectory(self) -> None:
		logging.debug("Opening directory selector...")
		search_dir = QtCore.QDir.currentPath()
		directory = QFileDialog.getExistingDirectory(self, "Select assets directory", search_dir)
		if directory:
			self.dir_path = str(directory)
			self.dataset = discover_samples(directory)

			self.updateTree()

	@Slot()
	def prevFrame(self) -> None:
		start = time.time()
		assert self.state == AppState.DISPLAYING
		self.sample_player.prev_frame()

		self.update_timeline()
		self.update_vis()
		logging.info(f"Prev frame displayed: {time.time() - start}")

	@Slot()
	def nextFrame(self) -> None:
		start = time.time()
		assert self.state == AppState.DISPLAYING
		self.sample_player.next_frame()

		self.update_timeline()
		self.update_vis()
		logging.info(f"Next frame displayed: {time.time() - start}")

	@Slot(int)
	def setFrame(self, frame_index):
		start = time.time()
		assert self.state == AppState.DISPLAYING
		self.sample_player.set_frame_index(frame_index)
		self.update_vis()
		logging.info(f"Random frame displayed: {time.time() - start}")


	@Slot()
	def exitApp(self) -> None:
		self.close()
