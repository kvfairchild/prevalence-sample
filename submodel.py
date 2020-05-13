import argparse
import json
from pathlib import Path

class SubModel:
    model_type = ""
    model_name = ""
    model_id = ""
    is_forecast_model = False
    input_models = []
    model_parameters = {}
    all_inputs_samples_and_metadata = []
    params = {}

    def __str__(self):
        return " | ".join([self.model_type, self.model_name, self.model_id])

    # def parse_arguments(self) -> argparse.Namespace:
    #     parser = argparse.ArgumentParser(description='')
    #     parser.add_argument('--t0', required=True)
    #     parser.add_argument('--n_samples', required=True)
    #     parser.add_argument('--dates', nargs='+', required=True)
    #     args = parser.parse_args()
    #     args.dates = args.dates[0].split(' ')
    #     return args

    def read_input_samples_metadata(self, input_dir):
        for input_model in self.input_models:
            input_prefix = Path(input_dir, input_model['model_name']).as_posix()
            with open(input_prefix + "_samples.json") as f:
                samples = json.load(f)
            with open(input_prefix + "_metadata.json") as f:
                metadata = json.load(f)
            self.all_inputs_samples_and_metadata.append((samples, metadata))
        if not self.input_models:
            input_prefix = Path(input_dir, 'input').as_posix()
            with open(input_prefix + "_params.json") as f:
                params = json.load(f)
            self.params = params

    def write_output_samples_metadata(self, output_dir : str, samples : dict, metadata : dict):
        metadata_fname = Path(output_dir, 'output_metadata.json').as_posix()
        samples_fname = Path(output_dir, 'output_samples.json').as_posix()
        print('Model storing file locally: ' + metadata_fname)
        print('Model storing file locally: ' + samples_fname)
        with open(samples_fname, 'w') as f:
            json.dump(samples, f, indent=4)
        with open(metadata_fname, 'w') as f:
            json.dump(metadata, f, indent=4)

    def single_draw_from_model(self, dates: list, inputs_sample: dict) -> dict:
        raise NotImplementedError

    def needed_input_models(self) -> list:
        return self.input_models

    def generate_metadata(self, t_0: str) -> dict:
        return dict(
            model_type=self.model_type,
            model_name=self.model_name,
            model_id=self.model_id,
            input_models=self.input_models,
            t0_date=t_0,
            model_parameters=self.model_parameters
        )

    def sample(self,  t_0: str, n_samples: int, dates: list) -> dict:
        samples = list()
        for n in range(n_samples):
            inputs_sample = dict()
            for inputs_samples, inputs_metadata in self.all_inputs_samples_and_metadata:
                if inputs_metadata['model_type'] not in inputs_sample:
                    inputs_sample[inputs_metadata['model_type']] = dict()
                inputs_sample[inputs_metadata['model_type']][inputs_metadata['model_name']] = inputs_samples['samples'][n]
            samples.append(self.single_draw_from_model(dates, inputs_sample))
        if self.is_forecast_model:
            return dict(dates=dates, samples=samples)
        return dict(samples=samples)
