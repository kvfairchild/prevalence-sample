import numpy as np
import subprocess
from scipy.integrate import odeint

from submodel import SubModel
from model_data.zip_codes import ZIP_CODES
# from model_data.prevalence_samples import DATES, SAMPLES


class PlaceholderZipCodePrevalenceModel(SubModel):

    def __init__(self):
        self.model_name = 'placeholder-zip-code-prevalence-model'
        self.model_type = 'prevalence'
        self.model_id = '953f4a88d1dddf4884810b24ed7c26741e02d59'

        self.zip_codes = ZIP_CODES
        self.local_prevalence = self.prevalence_over_time(365*2)

    def _get_latest_git_hash(self):
        hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
        hash_utf8 = hash.decode("utf-8")
        return str(hash_utf8[1:])

    def prevalence_over_time(self, num_days: int):
        # From: https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/

        # Total population, N.
        N = 1000
        # Initial number of infected and recovered individuals, I0 and R0.
        I0, R0 = 50, 50
        # Everyone else, S0, is susceptible to infection initially.
        S0 = N - I0 - R0
        # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
        beta, gamma = 0.2, 1. / 8
        # A grid of time points (in days)
        t = np.linspace(0, num_days, num_days)

        # The SIR model differential equations.
        def deriv(y, t, N, beta, gamma):
            S, I, R = y
            dSdt = -beta * S * I / N
            dIdt = beta * S * I / N - gamma * I
            dRdt = gamma * I
            return dSdt, dIdt, dRdt

        # Initial conditions vector
        y0 = S0, I0, R0
        # Integrate the SIR equations over the time grid, t.
        ret = odeint(deriv, y0, t, args=(N, beta, gamma))
        S, I, R = ret.T

        return I / N

    def zip_code_prevalence(self, dates: list, inputs_sample: dict) -> list:
        prevalences = []
        for t_i, date in enumerate(dates):
            prevalences.append({})
            for z in self.zip_codes:
                prevalences[-1][z] = round(self.local_prevalence[t_i] * (1.0 + (np.random.rand() * 0.1 - 0.05)), 4)
        return prevalences

    def single_draw_from_model(self, dates: list, inputs_sample: dict) -> list:
        return self.zip_code_prevalence(dates, inputs_sample)


if __name__ == "__main__":

    model = PlaceholderZipCodePrevalenceModel()

    model.read_input_samples_metadata('/input')
    t0 = model.params['t_0']
    n_samples = model.params['n_samples']
    dates = model.params['dates_to_simulate']

    print("\nRunning model: " + str(model))
    samples = model.sample(t0, int(n_samples), dates)
    metadata = model.generate_metadata(t0)

    model.write_output_samples_metadata('/output', samples, metadata)

