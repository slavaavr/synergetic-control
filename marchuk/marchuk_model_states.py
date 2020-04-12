class State:
    a1: float
    a2: float
    a3: float
    a4: float
    a5: float
    a6: float
    a7: float
    a8: float

    v0: float
    s0: float
    f0: float
    m0: float

    t0: float
    v_desirable: float
    u_max: float
    m_threshold: float
    c: float
    w1: float
    w2: float

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


fatal_params = {
    "a1": 1.54,
    "a2": 0.77,
    "a3": 880,
    "a4": 0.15,
    "a5": 0.5,
    "a6": 12,
    "a7": 0.12,
    "a8": 8,

    "v0": 10e-6,
    "s0": 1,
    "f0": 1,
    "m0": 0,

    "t0": 1,
    "v_desirable": 0,
    "u_max": 5,
    "m_threshold": 0.1,
    "c": 0.1,
    "w1": 0.05,  # 0.001
    "w2": 0.1,  # 0.001
}
fatal_state = State(**fatal_params)

chronic_params = {
    "a1": 1,
    "a2": 0.8,
    "a3": 1000,
    "a4": 0.17,
    "a5": 0.5,
    "a6": 10,
    "a7": 0.12,
    "a8": 8,

    "v0": 10e-6,
    "s0": 1,
    "f0": 1,
    "m0": 0,

    "t0": 1,
    "v_desirable": 0,
    "u_max": 5,
    "m_threshold": 0.1,
    "c": 0.1,
    "w1": 0.05,  # 0.001
    "w2": 0.1,  # 0.001
}
chronic_state = State(**chronic_params)

acute_params = {
    "a1": 2,
    "a2": 0.8,
    "a3": 10000,
    "a4": 0.17,
    "a5": 0.5,
    "a6": 10,
    "a7": 0.12,
    "a8": 8,

    "v0": 10e-6,
    "s0": 1,
    "f0": 1,
    "m0": 0,

    "t0": 1,
    "v_desirable": 0,
    "u_max": 5,
    "m_threshold": 0.1,
    "c": 0.1,
    "w1": 0.05,  # 0.001
    "w2": 0.1,  # 0.001

}
acute_state = State(**acute_params
                    )
sub_clinical_params = {
    "a1": 8,
    "a2": 10,
    "a3": 10000,
    "a4": 0.17,
    "a5": 0.5,
    "a6": 10,
    "a7": 0.12,
    "a8": 8,

    "v0": 10e-6,
    "s0": 1,
    "f0": 1,
    "m0": 0,

    "t0": 1,
    "v_desirable": 0,
    "u_max": 5,
    "m_threshold": 0.1,
    "c": 0.1,
    "w1": 0.05,  # 0.001
    "w2": 0.1,  # 0.001

}
sub_clinical_state = State(**sub_clinical_params)