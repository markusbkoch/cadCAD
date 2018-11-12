from datetime import datetime, timedelta
from decimal import Decimal
from fn.func import curried

flatten = lambda l: [item for sublist in l for item in sublist]

def flatmap(f, items):
        return list(map(f, items))


def datetime_range(start, end, delta, dt_format='%Y-%m-%d %H:%M:%S'):
    reverse_head = end
    [start, end] = [datetime.strptime(x, dt_format) for x in [start, end]]

    def _datetime_range(start, end, delta):
        current = start
        while current < end:
            yield current
            current += delta

    reverse_tail = [dt.strftime(dt_format) for dt in _datetime_range(start, end, delta)]
    return reverse_tail + [reverse_head]

def last_index(l):
    return len(l)-1

def retrieve_state(l, offset):
    return l[last_index(l) + offset + 1]

# shouldn't
def bound_norm_random(rng, low, high):
    # Add RNG Seed
    res = rng.normal((high+low)/2,(high-low)/6)
    if (res<low or res>high):
        res = bound_norm_random(rng, low, high)
    return Decimal(res)

@curried
def proc_trigger(trigger_step, update_f, step):
    if step == trigger_step:
        return update_f
    else:
        return lambda x: x

# accept timedelta instead of timedelta params
def time_step(dt_str, dt_format='%Y-%m-%d %H:%M:%S', days=0, minutes=0, seconds=30):
    dt = datetime.strptime(dt_str, dt_format)
    t = dt + timedelta(days=days, minutes=minutes, seconds=seconds)
    return t.strftime(dt_format)

# accept timedelta instead of timedelta params
def ep_time_step(s, dt_str, fromat_str='%Y-%m-%d %H:%M:%S', days=0, minutes=0, seconds=1):
    if s['mech_step'] == 0:
        return time_step(dt_str, fromat_str, days, minutes, seconds)
    else:
        return dt_str

def exo_update_per_ts(ep):
    @curried
    def ep_decorator(f, y, step, sL, s, _input):
        if s['mech_step'] + 1 == 1:  # inside f body to reduce performance costs
            return f(step, sL, s, _input)
        else:
            return (y, s[y])
    return {es: ep_decorator(f, es) for es, f in ep.items()}

# def create_tensor_field(mechanisms, env_poc, keys=['behaviors', 'states']):
#     dfs = [ create_matrix_field(mechanisms, k) for k in keys ]
#     df = pd.concat(dfs, axis=1)
#     for es, i in zip(env_poc, range(len(env_poc))):
#         df['es'+str(i)] = es
#     df['m'] = df.index + 1
#     return df
#################

# def exo_proc_trigger(mech_step, update_f, y):
#     if mech_step == 1:
#         return update_f
#     else:
#         return lambda step, sL, s, _input: (y, s[y])



# def apply_exo_proc(s, x, y):
#     if s['mech_step'] == 1:
#         return x
#     else:
#         return s[y]

# def es5p2(step, sL, s, _input): # accept timedelta instead of timedelta params
#     y = 'timestamp'
#     x = ep_time_step(s, s['timestamp'], seconds=1)
#     return (y, x)


