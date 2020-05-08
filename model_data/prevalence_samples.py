import json

f = open('model_data/prevalence-0_samples.json', )
data = json.load(f)

DATES = data['dates']
SAMPLES = data['samples'][0][0]