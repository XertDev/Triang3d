import os
from pathlib import Path


BASE_PATH = os.path.dirname(os.path.realpath(__file__))
RESOURCE_PATH = BASE_PATH + "/../resources"
OUTPUT_PATH = BASE_PATH + "/../gui/generated"

os.makedirs(OUTPUT_PATH, exist_ok=True)

for root, dirs, files in os.walk(RESOURCE_PATH):
	for name in files:
		if name.lower().endswith(".ui"):
			basename = name[0:-3]
			os.system("pyside6-uic {1}/{0}.ui > {2}/ui_{0}.py".format(basename, RESOURCE_PATH, OUTPUT_PATH))

Path(OUTPUT_PATH + "/__init__.py").touch()
