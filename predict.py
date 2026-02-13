#!/usr/bin/env python

# Example sh command for species net
# python -m speciesnet.scripts.run_model --folders deer/ --predictions_json predictions.json

from py_util.time import time_it

def run_species_net(instances_dict: dict, output_path: str|None) -> None|dict:
	from speciesnet import SpeciesNet
	
	model = SpeciesNet(
			'kaggle:google/speciesnet/pyTorch/v4.0.1a', # or v4.0.1b
			components='all',
			geofence=True,
		)

	return model.predict(
		instances_dict=instances_dict,
		run_mode='multi_thread',
		batch_size=8,
		progress_bars=False,
		predictions_json=output_path,
	)

if __name__ == '__main__':
	import sys
	import argparse
	from time import time_ns

	args = sys.argv[1:]

	parser = argparse.ArgumentParser(sys.argv[0], description='Runs SpeciesNet prediction')
	parser.add_argument('output_path', type=str, help='Output path for the JSON predictions')
	parsed = parser.parse_args(args)
		
	def run():
		from speciesnet.utils import prepare_instances_dict

		instances_dict = prepare_instances_dict(
				folders=['images/'],
				country="USA",
				admin1_region="UT",
			)
		
		run_species_net(instances_dict, parsed.output_path)
	
	print(time_it('ms', run)[0])