import math

import numpy as np

import xml.etree.ElementTree as ET

from model.camera_calibration import CameraCalibration


def _extract_geometry(geometry_node: ET.Element) -> CameraCalibration.GeometryCalibration:
	geometry_calibration = CameraCalibration.GeometryCalibration()

	geometry_calibration.width = int(geometry_node.attrib["width"])
	geometry_calibration.height = int(geometry_node.attrib["height"])

	geometry_calibration.ncx = float(geometry_node.attrib["ncx"])
	geometry_calibration.nfx = float(geometry_node.attrib["nfx"])
	geometry_calibration.dx = float(geometry_node.attrib["dx"])
	geometry_calibration.dy = float(geometry_node.attrib["dy"])
	geometry_calibration.dpx = float(geometry_node.attrib["dpx"])
	geometry_calibration.dpy = float(geometry_node.attrib["dpy"])

	return geometry_calibration


def _extract_intrinsic(intrinsic_node: ET.Element) -> CameraCalibration.IntrinsicCalibration:
	intrinsic_calibration = CameraCalibration.IntrinsicCalibration()

	intrinsic_calibration.focal = float(intrinsic_node.attrib["focal"])
	intrinsic_calibration.kappa1 = float(intrinsic_node.attrib["kappa1"])
	intrinsic_calibration.cx = float(intrinsic_node.attrib["cx"])
	intrinsic_calibration.cy = float(intrinsic_node.attrib["cy"])
	intrinsic_calibration.sx = float(intrinsic_node.attrib["sx"])

	return intrinsic_calibration


def _extract_extrinsic(extrinsic_node: ET.Element) -> CameraCalibration.ExtrinsicCalibration:
	extrinsic_calibration = CameraCalibration.ExtrinsicCalibration()

	extrinsic_calibration.tx = float(extrinsic_node.attrib["tx"])
	extrinsic_calibration.ty = float(extrinsic_node.attrib["ty"])
	extrinsic_calibration.tz = float(extrinsic_node.attrib["tz"])
	extrinsic_calibration.rx = float(extrinsic_node.attrib["rx"])
	extrinsic_calibration.ry = float(extrinsic_node.attrib["ry"])
	extrinsic_calibration.rz = float(extrinsic_node.attrib["rz"])

	return extrinsic_calibration


def recalculate_matrices(calibration: CameraCalibration):
	#https://github.com/tmandel/fish-detrac/blob/3cc57b2a372015186b07447ca0f204cbb9f164bc/fishtrac/trackers/GOG/getRotTrans.m
	calibration.transform_mat = np.array(
		[
			calibration.extrinsic_calibration.tx,
			calibration.extrinsic_calibration.ty,
			calibration.extrinsic_calibration.tz
		],
		np.float64
	)

	sa = math.sin(calibration.extrinsic_calibration.rx)
	ca = math.cos(calibration.extrinsic_calibration.rx)
	sb = math.sin(calibration.extrinsic_calibration.ry)
	cb = math.cos(calibration.extrinsic_calibration.ry)
	sg = math.sin(calibration.extrinsic_calibration.rz)
	cg = math.cos(calibration.extrinsic_calibration.rz)

	r_11 = cb * cg
	r_12 = cg * sa * sb - ca * sg
	r_13 = sa * sg + ca * cg * sb
	r_21 = cb * sg
	r_22 = sa * sb * sg + ca * cg
	r_23 = ca * sb * sg - cg * sa
	r_31 = -sb
	r_32 = cb * sa
	r_33 = ca * cb

	calibration.rotation_mat = np.array(
		[
			[r_11, r_12, r_13],
			[r_21, r_22, r_23],
			[r_31, r_32, r_33]
		],
		np.float64
	)


def load_calibration_file(file_path: str) -> CameraCalibration:
	calibration = CameraCalibration()

	root = ET.parse(file_path).getroot()

	geometry_node = root.find("Geometry")
	calibration.geometry_calibration = _extract_geometry(geometry_node)

	intrinsic_node = root.find("Intrinsic")
	calibration.intrinsic_calibration = _extract_intrinsic(intrinsic_node)

	extrinsic_node = root.find("Extrinsic")
	calibration.extrinsic_calibration = _extract_extrinsic(extrinsic_node)

	recalculate_matrices(calibration)
	
	return calibration
