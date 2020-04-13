import marchuk.synergetic_stochastic_control as ssc
import marchuk.synergetic_control as sc
import marchuk.marchuk_model_states as states
import matplotlib.pyplot as plt
import random as rand

if __name__ == '__main__':
    plt.rc('font', size=14)
    plt.rc('axes', titlesize=14)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-1, 1), useMathText=True, useOffset=False)

    plt.ylabel('V[k]', rotation='horizontal', Y=1.0)
    plt.xlabel('k,days', X=1.0)

    seed = 42
    epoches = 15
    noise_standard_deviation = 0.7

    rand.seed(seed)
    eq0 = sc.EquationSystem(states.fatal_state)
    eq0.train(epoches)

    rand.seed(seed)
    eq1 = sc.EquationSystem(states.fatal_state)
    eq1.enable_noise(noise_standard_deviation)
    eq1.train(epoches)

    rand.seed(seed)
    eq2 = ssc.EquationSystem(states.fatal_state, is_filter_enabled=False,
                             noise_standard_deviation=noise_standard_deviation)
    eq2.train(epoches)

    rand.seed(seed)
    eq3 = ssc.EquationSystem(states.fatal_state, is_filter_enabled=True,
                             noise_standard_deviation=noise_standard_deviation)
    eq3.train(epoches)

    plt.plot(eq0.vv, c='green', label='СТУ без шума')
    plt.plot(eq1.vv, c='b', label='СТУ + шум')
    plt.plot(eq2.vv, c='red', label='СТУ + стохастика')
    plt.plot(eq3.vv, c='black', label='СТУ + стохастика + фильтр')

    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()
