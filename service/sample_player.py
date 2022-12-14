import logging
from typing import List

import os
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

import time
from PySide6.QtGui import QImage, QPixmap


def map_image(image_pose):
	image, pose = image_pose
	height, width, channel = image.shape
	bytes_per_line = 3 * width
	q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
	q_pixmap = QPixmap(q_img)
	return q_pixmap, pose


def map_keypoints(model):
	def processor(image):
		pose = model.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
		if pose.pose_landmarks:
			mp_drawing.draw_landmarks(
				image,
				pose.pose_landmarks,
				mp_pose.POSE_CONNECTIONS,
				landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
			)

		return image, pose.pose_landmarks

	return lambda image: processor(image)


class SamplePlayer:
	sample_dir: str
	frame: int

	max_frame: int

	captures: List[cv2.VideoCapture]

	def get_specific_frame(self, index):
		for capture in self.captures:
			capture.set(cv2.CAP_PROP_POS_FRAMES, index)

		return [capture.read()[1] for capture in self.captures]

	def next_frame(self):
		self.frame = min(self.frame + 1, self.max_frame - 1)

	def prev_frame(self):
		self.frame = min(self.frame + 1, self.max_frame - 1)

	def set_frame_index(self, index):
		self.frame = index

	def get_frame_index(self):
		return self.frame

	def get_max_frame(self):
		return self.max_frame

	def get_frame(self):
		start = time.time()

		images = map(map_keypoints(self.model),  self.get_specific_frame(self.frame))
		images_with_pos = map(map_image, images)

		logging.info(f"Frame conversion: {time.time() - start}")

		return list(images_with_pos)

	def __init__(self, images_path: str):
		self.sample_dir = images_path
		self.captures = []
		for file in os.listdir(images_path):
			self.captures.append(cv2.VideoCapture(os.path.join(images_path, file)))

		self.frame = 0
		self.max_frame = self.captures[0].get(cv2.CAP_PROP_FRAME_COUNT)

		self.model = mp_pose.Pose(
			static_image_mode=True,
			model_complexity=2,
			enable_segmentation=True,
			min_detection_confidence=0.5
		)


