import os
from abc import ABC, abstractmethod
import pandas as pd
from finlab_crypto.overfitting import CSCV


def generate_cscv(portfolio, cscv_nbins=10, cscv_objective=lambda r: r.mean()):
    cscv = CSCV(n_bins=cscv_nbins, objective=cscv_objective)
    cscv.add_daily_returns(portfolio.daily_returns())
    cscv_result = cscv.estimate_overfitting(plot=False)
    return cscv_result


class GenerateReport(ABC):
    def __init__(self, symbols: list, date: str, res_dir: str):
        self.symbols = symbols
        self.date = date
        self.res_dir = os.path.join(res_dir, date.strip('-'))
        self.generate_report()

    @abstractmethod
    def print_params(self, params):
        pass

    def generate_report(self):
        if os.path.isdir(self.res_dir) and self.symbols:
            files = os.listdir(self.res_dir)
            print(f'{self.date} update')
            for symbol in self.symbols:
                for f in files:
                    if f.startswith(symbol) and f.endswith(self.date + '.pkl'):
                        res = pd.read_pickle(os.path.join(self.res_dir, f))
                        params = f.split('-')
                        self.print_params(params)
                        res = res.reset_index()
                        res.columns = ['', '']
                        print(res.to_markdown(showindex=False), '\n')
                        # display(HTML(rslt.reset_index().to_html(header=False)))
