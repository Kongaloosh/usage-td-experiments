'''
Created on May 25, 2015

@author: A. Rupam Mahmood
'''

import numpy as np
from pysrc.problems.offrandommdp import OffRandomMDP
from pysrc.problems.mdp import PerformanceMeasure
from pysrc.experiments import offrndmdpexp
from pysrc.algorithms.tdprediction.offpolicy.gtd import GTD
from pysrc.algorithms.tdprediction.offpolicy.wtd import WTD
from pysrc.algorithms.tdprediction.offpolicy.wislstd import WISLSTD
from pysrc.algorithms.tdprediction.offpolicy.olstd2 import OLSTD2
from pysrc.algorithms.tdprediction.offpolicy.oislstd import OISLSTD
import matplotlib.pyplot as ppl


def onealg(alg, prob, nrunseeds, N, config):
  perf1mean = np.zeros((nrunseeds, N))
  for runseed in range(nrunseeds):
    config['runseed'] = runseed
    alg1 = alg(config)
    perf1 = PerformanceMeasure(config, prob)
    offrndmdpexp.runoneconfig(config, prob, alg1, perf1)
    perf1mean[config['runseed']] = perf1.getNormMSPVE()
  
  return perf1mean

def main():
  ns          = 10
  nrunseeds    = 5
  N           = 500
  gamma   = 0.9
  config     = \
                   {
                   'mdpseed'    : 1000, 
                   'Gamma'      : gamma,
                   'ftype'      : 'binary',
                   'numzerogs'  : 2,
                   'T'          : N,
                   'N'          : N,
                   'ns'         : ns,
                   'na'         : 3,
                   'nf'         : int(np.ceil(np.log(ns+1)/np.log(2))),
                   'b'          : 3,
                   'rtype'      :'uniform', 
                   'rparam'     :1,
                   'Rstd'       : 0.0,
                   'initsdist'  : 'statezero',
                   'bpoltype'   : 'random',
                   'tpoltype'   : 'random',
                   }
  config.update({'alpha':0.05, 'beta':0.0, 'lmbda':0.5})            
  prob = OffRandomMDP(config)
  perf1mean = onealg(GTD, prob, nrunseeds, N, config)         
  config.update({'eta':0.01, 'initd':1.0, 'lmbda':0.5})            
  perf2mean = onealg(WTD, prob, nrunseeds, N, config)         
  config.update({'inita':0.1, 'lmbda':0.8})            
  perf3mean = onealg(WISLSTD, prob, nrunseeds, N, config)         
  config.update({'inita':1., 'lmbda':0.99})            
  perf4mean = onealg(OLSTD2, prob, nrunseeds, N, config)         
  config.update({'inita':10., 'lmbda':0.9})            
  perf5mean = onealg(OISLSTD, prob, nrunseeds, N, config)         
  ppl.plot(np.mean(perf1mean, 0), label='gtd')
  ppl.plot(np.mean(perf2mean, 0), label='wtd')
  ppl.plot(np.mean(perf3mean, 0), label='wislstd')
  ppl.plot(np.mean(perf4mean, 0), label='olstd2')
  ppl.plot(np.mean(perf5mean, 0), label='oislstd')
  ppl.yscale('log')
  ppl.ylim([None, 1])
  ppl.legend()
                   
if __name__ == '__main__':
    main()
    ppl.show()
    