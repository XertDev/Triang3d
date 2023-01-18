import os
from typing import List

import numpy as np
import mediapipe as mp

from config import CAMERA_COUNT

from service.calibration_utils import load_calibration_file
from model.camera_calibration import CameraCalibration
from service.triangulation_utils import imageToWorld


def intersect(starts, ends):
	n = (starts - ends) / np.linalg.norm(starts - ends, axis=1)[:, np.newaxis]

	projs = np.eye(n.shape[1]) - n[:, :, np.newaxis] * n[:, np.newaxis]

	R = projs.sum(axis=0)
	q = (projs @ starts[:, :, np.newaxis]).sum(axis=0)

	p = np.linalg.lstsq(R, q, rcond=None)[0]
	return p


class SkeletalReconstructor:
	_calibrations: List[CameraCalibration]

	def __init__(self, calibration_dir):
		self._calibrations = []
		for i in range(1, CAMERA_COUNT+1):
			calibration_file = os.path.join(calibration_dir, f"c{i}.xml")
			self._calibrations.append(load_calibration_file(calibration_file))

	def guide_lines_from_landmarks(self, landmarks_per_subframes):
		grouped_landmarks = {}
		for pose_landmark in mp.solutions.pose.PoseLandmark:
			for cam_idx, subframe_landmarks in enumerate(landmarks_per_subframes):

				if pose_landmark not in grouped_landmarks:
					grouped_landmarks[pose_landmark] = []

				if not subframe_landmarks:
					grouped_landmarks[pose_landmark].append(None)
					continue

				landmark = subframe_landmarks.landmark[pose_landmark]
				x = landmark.x
				# x = landmark.x * self._calibrations[cam_idx].geometry_calibration.width
				y = landmark.y
				# y = landmark.y * self._calibrations[cam_idx].geometry_calibration.height
				# x = (1 - landmark.x) * self._calibrations[cam_idx].geometry_calibration.width
				# y = (1 - landmark.y) * self._calibrations[cam_idx].geometry_calibration.height

				if landmark.visibility < 0.7:
					grouped_landmarks[pose_landmark].append(None)
					continue

				grouped_landmarks[pose_landmark].append((x, y))

		guide_lines_per_landmark = dict()
		for landmark_key in grouped_landmarks.keys():
			if grouped_landmarks[landmark_key].count(None) > 1:
				continue

			guide_lines_per_landmark[landmark_key] = self.map_image_point_to_camera_lines(grouped_landmarks[landmark_key])

		return guide_lines_per_landmark

	def keypoint_from_guide_lines_for_landmarks(self, guide_lines_per_landmark):
		landmarks_3d = dict()
		for landmark_key in guide_lines_per_landmark.keys():
			lines = guide_lines_per_landmark[landmark_key]

			starts = np.array([points[0] for points in lines], np.float64)
			ends = np.array([points[1] for points in lines], np.float64)

			landmarks_3d[landmark_key] = intersect(starts, ends)
		return landmarks_3d


	def map_image_point_to_camera_lines(self, points):
		assert(len(self._calibrations) == len(points))

		lines = []
		for idx, point in enumerate(points):
			if point:
				calib = self._calibrations[idx]
				start = [
					calib.extrinsic_calibration.tx,
					calib.extrinsic_calibration.ty,
					calib.extrinsic_calibration.tz
				]
				end = imageToWorld(point[0], point[1], calib)

				lines.append((start, end))

		return lines

	# Based on https://github.com/smidm/camera.py/blob/master/camera.py
	def linear_triangulation(self, points):
		assert(len(self._calibrations) == len(points))

		D = np.zeros((len(self._calibrations) * 2, 4))
