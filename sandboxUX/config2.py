from decimal import Decimal
import numpy as np

from SimCAD import Configuration, configs
from SimCAD.utils.configuration import exo_update_per_ts, proc_trigger, bound_norm_random, \
    ep_time_step


seed = {
    'a': np.random.RandomState(1),
}

# Behaviors per Mechanism
def behavior(step, sL, s):
    return {'param1': 1}

# Internal States per Mechanism
def mechanism(step, sL, s, _input):
    y = 's1'
    x = s['s1'] + _input['param1']
    return (y, x)

# Exogenous States
proc_one_coef_A = 0.7
proc_one_coef_B = 1.3
def env_process(step, sL, s, _input):
    y = 's2'
    x = bound_norm_random(seed['a'], proc_one_coef_A, proc_one_coef_B)
    return (y, x)

def time(step, sL, s, _input):
    y = 'timestamp'
    x = ep_time_step(s, s['timestamp'], seconds=1)
    return (y, x)

# Genesis States
state_dict = {
    's1': Decimal(0.0),
    's2': Decimal(0.0),
    'timestamp': '2018-10-01 15:16:24'
}

# remove `exo_update_per_ts` to update every ts
exogenous_states = exo_update_per_ts(
    {
    "s2": env_process,
    "timestamp": time
    }
)

#	make env proc trigger field agnostic
env_processes = {
}

# lambdas
# genesis Sites should always be there
# [1, 2]
# behavior_ops = [ foldr(_ + _), lambda x: x + 0 ]


# [1, 2] = {'b1': ['a'], 'b2', [1]} =
# behavior_ops = [behavior_to_dict, print_fwd, sum_dict_values]
# behavior_ops = [foldr(dict_elemwise_sum())]
# behavior_ops = []

# need at least 1 behaviour and 1 state function for the 1st mech with behaviors
# mechanisms = {}
mechanisms = {
    "mechanism": {
        "behaviors": {
            "behavior": behavior
        },
        "states": {
            "s1": mechanism,
        }
    }
}

sim_config = {
    "N": 3,
    "T": range(10)
}

configs.append(Configuration(sim_config, state_dict, seed, exogenous_states, env_processes, mechanisms))