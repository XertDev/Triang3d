import numpy as np
import numpy.typing as npt


class CameraCalibration:
	class GeometryCalibration:
		width: int
		height: int

		ncx: float
		nfx: float
		dx: float
		dy: float
		dpx: float
		dpy: float

	class IntrinsicCalibration:
		focal: float
		kappa1: float
		cx: float
		cy: float
		sx: float

	class ExtrinsicCalibration:
		tx: float
		ty: float
		tz: float

		rx: float
		ry: float
		rz: float

	geometry_calibration: GeometryCalibration
	intrinsic_calibration: IntrinsicCalibration
	extrinsic_calibration: ExtrinsicCalibration

	rotation_mat: npt.NDArray[np.float64]
	transform_mat: npt.NDArray[np.float64]

	intrinsic_mat: npt.NDArray[np.float64]