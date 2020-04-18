class State:
    a1: float
    a2: float
    a3: float
    a4: float
    a5: float
    a6: float

    x0: float
    y0: float
    z0: float

    t0: float
    u_max: float
    c: float
    T: float
    p: float

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


state1_params = {
    "a1": 5,
    "a2": 8,
    "a3": 1,
    "a4": 0.6,
    "a5": 2.46,
    "a6": 2.1,

    "x0": 2,
    "y0": 5,
    "z0": 1,

    "t0": 0.01,
    "u_max": 1000,
    "c": 0.1,
    "T": 0.05,  # 0.001
    "p": 0.01,
}
state1 = State(**state1_params)

state3_params = {
    "a1": 5,
    "a2": 8,
    "a3": 0.8,
    "a4": 0.6,
    "a5": 2.46,
    "a6": 2.1,

    "x0": 1,
    "y0": 1,
    "z0": 1,

    "t0": 0.01,
    "u_max": 1e100,
    "c": 0.1,
    "T": 0.05,  # 0.001
    "p": 0.01,
}
state3 = State(**state3_params)

state10_params = {
    "a1": 5,
    "a2": 8,
    "a3": 0.5,
    "a4": 2.5,
    "a5": 3.9,
    "a6": 2.1,

    "x0": 2,
    "y0": 5,
    "z0": 1,

    "t0": 0.01,
    "u_max": 1000,
    "c": 0.1,
    "T": 0.05,  # 0.001
    "p": 0.01,
}
state10 = State(**state10_params)
