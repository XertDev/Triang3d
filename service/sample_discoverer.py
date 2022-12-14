import os
import re

from model import Dataset, Sequence
from model.person import Person


def discover_samples(path: str):
	dataset = Dataset()
	dataset.persons = []

	temp_mapping = dict()

	for entry in os.listdir(path):
		samples_path = os.path.join(path, entry)

		desc = re.match(r"p(?P<person>\d+)s(?P<sample>\d+)", entry)
		person = desc["person"]
		sample = desc["sample"]

		if person not in temp_mapping:
			temp_mapping[person] = dict()

		temp_mapping[person][sample] = samples_path

	for person_id in temp_mapping.keys():
		person = Person()
		person.id = person_id
		person.sequences = []

		for sample in temp_mapping[person_id].keys():
			sequence = Sequence()
			sequence.seq_id = sample
			sequence.path = temp_mapping[person_id][sample]

			person.sequences.append(sequence)

		dataset.persons.append(person)

	return dataset

