# (C) Copyright 2023 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.


import logging
import os

import numpy as np
import onnxruntime as ort
from ai_models.model import Model

LOG = logging.getLogger(__name__)


class Debug(Model):
    # Download
    download_url = ""
    download_files = []

    # Input
    area = [90, 0, -90, 360]
    grid = [0.25, 0.25]
    param_sfc = ["msl", "10u", "10v", "2t"]
    param_level_pl = (
        ["z", "q", "t", "u", "v"],
        [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50],
    )

    # Output
    expver = "test"

    def __init__(self, num_threads=1, **kwargs):
        super().__init__(**kwargs)
        self.num_threads = num_threads

    def run(self):
        fields_pl = self.fields_pl

        param, level = self.param_level_pl
        fields_pl = fields_pl.sel(param=param, level=level)
        fields_pl = fields_pl.order_by(param=param, level=level)

        fields_pl_numpy = fields_pl.to_numpy(dtype=np.float32)
        fields_pl_numpy = fields_pl_numpy.reshape((5, 13, 721, 1440))

        fields_sfc = self.fields_sfc
        fields_sfc = fields_sfc.sel(param=self.param_sfc)
        fields_sfc = fields_sfc.order_by(param=self.param_sfc)

        fields_sfc_numpy = fields_sfc.to_numpy(dtype=np.float32)

        # input = fields_pl_numpy
        # input_surface = fields_sfc_numpy



        with self.stepper(6) as stepper:
            for i in range(self.lead_time // 6):
                step = (i + 1) * 6


                stepper(i, step)
