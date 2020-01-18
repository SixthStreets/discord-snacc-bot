import os
import json

from darkness.common.constants import RESOURCES_DIR


def read_json(file_name: str):
	p = os.path.join(RESOURCES_DIR, file_name)

	with open(p, "r") as f:
		data = json.load(f)

	return data


def write_json_keys(file_name: str, **kwargs):
	p = os.path.join(RESOURCES_DIR, file_name)

	data = read_json(file_name)

	for k, w in kwargs.items():
		data[k] = w

	with open(p, "w") as f:
		json.dump(data, f)
