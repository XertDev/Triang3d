from model.camera_calibration import CameraCalibration


def convertFromImageToDistorted(x: float, y: float, calibration: CameraCalibration):
	x_d = calibration.geometry_calibration.dpx * (
				x - calibration.intrinsic_calibration.cx) / calibration.intrinsic_calibration.sx
	y_d = calibration.geometry_calibration.dpy * (y - calibration.intrinsic_calibration.cy)

	return x_d, y_d


def convertDistortedToUndistorted(x: float, y: float, calibration: CameraCalibration):
	factor = 1 + calibration.intrinsic_calibration.kappa1 * (x * x + y * y)
	x_u = x * factor
	y_u = y * factor

	return x_u, y_u


def imageToWorld(x: float, y: float, calibration: CameraCalibration):
	x_d, y_d = convertFromImageToDistorted(x, y, calibration)
	x_u, y_u = convertDistortedToUndistorted(x_d, y_d, calibration)

	z_w = 0
	rot = calibration.rotation_mat
	focal = calibration.intrinsic_calibration.focal
	t_z = calibration.extrinsic_calibration.tz
	t_x = calibration.extrinsic_calibration.tx
	t_y = calibration.extrinsic_calibration.ty

	denom = (rot[0, 0] * rot[2, 1] - rot[0, 1] * rot[2, 0]) * y_u
	denom += (rot[1, 1] * rot[2, 0] - rot[1, 0] * rot[2, 1]) * x_u
	denom -= focal * rot[0, 0] * rot[1, 1]
	denom += focal * rot[0, 1] * rot[1, 0]

	x_w = (
			(
				(
					rot[0, 1] * rot[2, 2] - rot[0, 2] * rot[2, 1]
				) * y_u +
				(
					rot[1, 2] * rot[2, 1] - rot[1, 1] * rot[2, 2]
				) * x_u -
				focal * rot[0, 1] * rot[1, 2] + focal * rot[0, 2] * rot[1, 1]
			) * z_w +
			(
				rot[0, 1] * t_z - rot[2, 1] * t_x
			) * y_u +
			(
				rot[2, 1] * t_y - rot[1, 1] * t_z
			) * x_u -
			focal * rot[0, 1] * t_y + focal * rot[1, 1] * t_x
		) / denom

	y_w = -(
			(
				(
					rot[0, 0] * rot[2, 2] - rot[0, 2] * rot[2, 0]
				) * y_u +
				(
					rot[1, 2] * rot[2, 0] - rot[1, 0] * rot[2, 2]
				) * x_u -
				focal * rot[0, 0] * rot[1, 2] + focal * rot[0, 2] * rot[1, 0]
			) * z_w +
			(
				rot[0, 0] * t_z - rot[2, 0] * t_x
			) * y_u +
			(
				rot[2, 0] * t_y - rot[1, 0] * t_z
			) * x_u -
			focal * rot[0, 0] * t_y + focal * rot[1, 0] * t_x
	) / denom

	return x_w, y_w, z_w
