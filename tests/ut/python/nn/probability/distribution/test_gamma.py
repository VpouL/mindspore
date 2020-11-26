# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""
Test nn.probability.distribution.Gamma.
"""
import numpy as np
import pytest

import mindspore.nn as nn
import mindspore.nn.probability.distribution as msd
from mindspore import dtype
from mindspore import Tensor

def test_gamma_shape_errpr():
    """
    Invalid shapes.
    """
    with pytest.raises(ValueError):
        msd.Gamma([[2.], [1.]], [[2.], [3.], [4.]], dtype=dtype.float32)

def test_type():
    with pytest.raises(TypeError):
        msd.Gamma(0., 1., dtype=dtype.int32)

def test_name():
    with pytest.raises(TypeError):
        msd.Gamma(0., 1., name=1.0)

def test_seed():
    with pytest.raises(TypeError):
        msd.Gamma(0., 1., seed='seed')

def test_rate():
    with pytest.raises(ValueError):
        msd.Gamma(0., 0.)
    with pytest.raises(ValueError):
        msd.Gamma(0., -1.)

def test_arguments():
    """
    args passing during initialization.
    """
    g = msd.Gamma()
    assert isinstance(g, msd.Distribution)
    g = msd.Gamma([3.0], [4.0], dtype=dtype.float32)
    assert isinstance(g, msd.Distribution)


class GammaProb(nn.Cell):
    """
    Gamma distribution: initialize with concentration/rate.
    """
    def __init__(self):
        super(GammaProb, self).__init__()
        self.gamma = msd.Gamma([3.0, 4.0], [1.0, 1.0], dtype=dtype.float32)

    def construct(self, value):
        prob = self.gamma.prob(value)
        log_prob = self.gamma.log_prob(value)
        cdf = self.gamma.cdf(value)
        log_cdf = self.gamma.log_cdf(value)
        sf = self.gamma.survival_function(value)
        log_sf = self.gamma.log_survival(value)
        return prob + log_prob + cdf + log_cdf + sf + log_sf

def test_gamma_prob():
    """
    Test probability functions: passing value through construct.
    """
    net = GammaProb()
    value = Tensor([0.5, 1.0], dtype=dtype.float32)
    ans = net(value)
    assert isinstance(ans, Tensor)


class GammaProb1(nn.Cell):
    """
    Gamma distribution: initialize without concentration/rate.
    """
    def __init__(self):
        super(GammaProb1, self).__init__()
        self.gamma = msd.Gamma()

    def construct(self, value, concentration, rate):
        prob = self.gamma.prob(value, concentration, rate)
        log_prob = self.gamma.log_prob(value, concentration, rate)
        cdf = self.gamma.cdf(value, concentration, rate)
        log_cdf = self.gamma.log_cdf(value, concentration, rate)
        sf = self.gamma.survival_function(value, concentration, rate)
        log_sf = self.gamma.log_survival(value, concentration, rate)
        return prob + log_prob + cdf + log_cdf + sf + log_sf

def test_gamma_prob1():
    """
    Test probability functions: passing concentration/rate, value through construct.
    """
    net = GammaProb1()
    value = Tensor([0.5, 1.0], dtype=dtype.float32)
    concentration = Tensor([2.0, 3.0], dtype=dtype.float32)
    rate = Tensor([1.0], dtype=dtype.float32)
    ans = net(value, concentration, rate)
    assert isinstance(ans, Tensor)

class GammaKl(nn.Cell):
    """
    Test class: kl_loss of Gamma distribution.
    """
    def __init__(self):
        super(GammaKl, self).__init__()
        self.g1 = msd.Gamma(np.array([3.0]), np.array([4.0]), dtype=dtype.float32)
        self.g2 = msd.Gamma(dtype=dtype.float32)

    def construct(self, concentration_b, rate_b, concentration_a, rate_a):
        kl1 = self.g1.kl_loss('Gamma', concentration_b, rate_b)
        kl2 = self.g2.kl_loss('Gamma', concentration_b, rate_b, concentration_a, rate_a)
        return kl1 + kl2

def test_kl():
    """
    Test kl_loss.
    """
    net = GammaKl()
    concentration_b = Tensor(np.array([1.0]).astype(np.float32), dtype=dtype.float32)
    rate_b = Tensor(np.array([1.0]).astype(np.float32), dtype=dtype.float32)
    concentration_a = Tensor(np.array([2.0]).astype(np.float32), dtype=dtype.float32)
    rate_a = Tensor(np.array([3.0]).astype(np.float32), dtype=dtype.float32)
    ans = net(concentration_b, rate_b, concentration_a, rate_a)
    assert isinstance(ans, Tensor)

class GammaCrossEntropy(nn.Cell):
    """
    Test class: cross_entropy of Gamma distribution.
    """
    def __init__(self):
        super(GammaCrossEntropy, self).__init__()
        self.g1 = msd.Gamma(np.array([3.0]), np.array([4.0]), dtype=dtype.float32)
        self.g2 = msd.Gamma(dtype=dtype.float32)

    def construct(self, concentration_b, rate_b, concentration_a, rate_a):
        h1 = self.g1.cross_entropy('Gamma', concentration_b, rate_b)
        h2 = self.g2.cross_entropy('Gamma', concentration_b, rate_b, concentration_a, rate_a)
        return h1 + h2

def test_cross_entropy():
    """
    Test cross entropy between Gamma distributions.
    """
    net = GammaCrossEntropy()
    concentration_b = Tensor(np.array([1.0]).astype(np.float32), dtype=dtype.float32)
    rate_b = Tensor(np.array([1.0]).astype(np.float32), dtype=dtype.float32)
    concentration_a = Tensor(np.array([2.0]).astype(np.float32), dtype=dtype.float32)
    rate_a = Tensor(np.array([3.0]).astype(np.float32), dtype=dtype.float32)
    ans = net(concentration_b, rate_b, concentration_a, rate_a)
    assert isinstance(ans, Tensor)

class GammaBasics(nn.Cell):
    """
    Test class: basic mean/sd function.
    """
    def __init__(self):
        super(GammaBasics, self).__init__()
        self.g = msd.Gamma(np.array([3.0, 4.0]), np.array([4.0, 6.0]), dtype=dtype.float32)

    def construct(self):
        mean = self.g.mean()
        sd = self.g.sd()
        mode = self.g.mode()
        return mean + sd + mode

def test_bascis():
    """
    Test mean/sd/mode/entropy functionality of Gamma.
    """
    net = GammaBasics()
    ans = net()
    assert isinstance(ans, Tensor)

class GammaConstruct(nn.Cell):
    """
    Gamma distribution: going through construct.
    """
    def __init__(self):
        super(GammaConstruct, self).__init__()
        self.gamma = msd.Gamma([3.0], [4.0])
        self.gamma1 = msd.Gamma()

    def construct(self, value, concentration, rate):
        prob = self.gamma('prob', value)
        prob1 = self.gamma('prob', value, concentration, rate)
        prob2 = self.gamma1('prob', value, concentration, rate)
        return prob + prob1 + prob2

def test_gamma_construct():
    """
    Test probability function going through construct.
    """
    net = GammaConstruct()
    value = Tensor([0.5, 1.0], dtype=dtype.float32)
    concentration = Tensor([0.0], dtype=dtype.float32)
    rate = Tensor([1.0], dtype=dtype.float32)
    ans = net(value, concentration, rate)
    assert isinstance(ans, Tensor)
