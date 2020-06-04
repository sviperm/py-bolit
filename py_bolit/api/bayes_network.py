from copy import deepcopy
from itertools import product

import numpy as np
from pomegranate import (BayesianNetwork, ConditionalProbabilityTable,
                         DiscreteDistribution, State)


def generate_CPT(event, dependencies):
    deps = deepcopy(dependencies)

    for dep in deps:
        if len(dep) < 2:
            dep['нет'] = [pr for st, pr in event.items()]

    e_states = list(event.keys())
    d_states = [list(dep.keys()) for dep in deps]

    table = list(list(i) for i in product(*d_states, e_states))

    for row in table:
        e_state = row[-1]
        s_i = e_states.index(e_state)
        formula = []

        for i, state in enumerate(row[:-1]):
            formula.append(deps[i][state][s_i])

        formula = 1 - np.prod(1 - np.array(formula))
        row.append(formula)

    states = len(e_states)
    sums = np.array(table)[:, -1].reshape(-1, states).astype(np.float).sum(axis=1)

    for i, row in enumerate(table):
        row[-1] = row[-1] / sums[int(i / states)]
        row[-1] = round(row[-1], 3)
    return table


e_smoking = {
    "да": 0.5,
    "нет": 0.5,
}

e_ater = {
    "да": 0.1,
    "нет": 0.9,
}

e_imt = {
    "да": 0.3,
    "нет": 0.7,
}

e_age_mt_40 = {
    "да": 0.5,
    "нет": 0.5,
}

e_stress = {
    "да": 0.2,
    "нет": 0.8,
}

e_prev_ha = {
    "да": 0.01,
    "нет": 0.99,
}

e_ha = {
    "да": 0.01,
    "нет": 0.99,
}

e_sten = {
    "да": 0.01,
    "нет": 0.99,
}

e_nevralgia = {
    "да": 0.05,
    "нет": 0.95,
}

e_chest_pain = {
    "да": 0.01,
    "нет": 0.99,
}

e_pain_mt_15min = {
    "да": 0.01,
    "нет": 0.99,
}

e_dyspnea = {
    "да": 0.01,
    "нет": 0.99,
}

d_smoke_ater = {"да": [0.9, 0.1]}
d_imt_ater = {"да": [0.8, 0.2]}
d_age_mt_40_ater = {"да": [0.7, 0.3]}

d_prev_ha_ha = {"да": [0.5, 0.5]}
d_stress_ha = {"да": [0.8, 0.2]}
d_ater_ha = {"да": [0.99, 0.01]}
d_age_mt_40_ha = {"да": [0.85, 0.15]}

d_stress_sten = {"да": [0.8, 0.2]}
d_ater_sten = {"да": [0.99, 0.01]}
d_age_mt_40_sten = {"да": [0.65, 0.35]}

d_imt_nevralgia = {"да": [0.05, 0.95], "нет": [0.9, 0.1]}
d_age_mt_40_nevralgia = {"да": [0.1, 0.9], "нет": [0.9, 0.1]}

d_nevralgia_chest_pain = {"да": [0.99, 0.01]}
d_sten_chest_pain = {"да": [0.99, 0.01]}
d_ha_chest_pain = {"да": [0.99, 0.01]}

d_nevralgia_pain_mt_15min = {"да": [0.01, 0.99]}
d_sten_pain_mt_15min = {"да": [0.01, 0.99]}
d_ha_pain_mt_15min = {"да": [0.99, 0.01]}

d_sten_dyspnea = {"да": [0.99, 0.01]}
d_ha_dyspnea = {"да": [0.01, 0.99]}

# Курение
smoking = DiscreteDistribution(e_smoking)

# ИМТ (худой, полный)
imt = DiscreteDistribution(e_imt)

# Старше 40 лет
age_mt_40 = DiscreteDistribution(e_age_mt_40)

# Атеросклероз
ater = ConditionalProbabilityTable(
    generate_CPT(e_ater,
                 [d_smoke_ater, d_imt_ater, d_age_mt_40_ater]),
    [smoking, imt, age_mt_40]
)

# Стресс
stress = DiscreteDistribution(e_stress)

# Инфаркт в анамнезе
prev_ha = DiscreteDistribution(e_prev_ha)

# Инфаркт
ha = ConditionalProbabilityTable(
    generate_CPT(e_ha,
                 [d_prev_ha_ha, d_stress_ha, d_ater_ha, d_age_mt_40_ha]),
    [prev_ha, stress, ater, age_mt_40]
)

# Стенокардия
sten = ConditionalProbabilityTable(
    generate_CPT(e_sten,
                 [d_stress_sten, d_ater_sten, d_age_mt_40_sten]),
    [stress, ater, age_mt_40]
)

# Межреберная невралгия
nevralgia = ConditionalProbabilityTable(
    generate_CPT(e_nevralgia,
                 [d_imt_nevralgia, d_age_mt_40_nevralgia]),
    [imt, age_mt_40]
)

# Загрудинные боли
chest_pain = ConditionalProbabilityTable(
    generate_CPT(e_chest_pain,
                 [d_imt_nevralgia, d_sten_chest_pain, d_ha_chest_pain]),
    [nevralgia, sten, ha]
)

# Боли > 15 мин
pain_mt_15min = ConditionalProbabilityTable(
    generate_CPT(e_pain_mt_15min,
                 [d_nevralgia_pain_mt_15min, d_sten_pain_mt_15min, d_ha_pain_mt_15min]),
    [nevralgia, sten, ha]
)

# Одышка
dyspnea = ConditionalProbabilityTable(
    generate_CPT(e_dyspnea,
                 [d_sten_dyspnea, d_ha_dyspnea]),
    [sten, ha]
)

n_smoking = State(smoking, name='smoking')
n_imt = State(imt, name='imt')
n_age_mt_40 = State(age_mt_40, name='age_mt_40')
n_ater = State(ater, name='ater')
n_stress = State(stress, name='stress')
n_prev_ha = State(prev_ha, name='prev_ha')
n_ha = State(ha, name='ha')
n_sten = State(sten, name='sten')
n_nevralgia = State(nevralgia, name='nevralgia')
n_chest_pain = State(chest_pain, name='chest_pain')
n_pain_mt_15min = State(pain_mt_15min, name='pain_mt_15min')
n_dyspnea = State(dyspnea, name='dyspnea')


class BayesNetwork:
    def __init__(self):
        # TODO upload and download destribution from databse

        model = BayesianNetwork('Этиологически-ориентированная СППВР')
        model.add_states(n_smoking, n_imt, n_age_mt_40, n_ater, n_stress,
                         n_prev_ha, n_ha, n_sten, n_nevralgia, n_chest_pain,
                         n_pain_mt_15min, n_dyspnea)

        model.add_edge(n_smoking, n_ater)

        model.add_edge(n_imt, n_ater)
        model.add_edge(n_imt, n_nevralgia)

        model.add_edge(n_ater, n_sten)
        model.add_edge(n_ater, n_ha)

        model.add_edge(n_age_mt_40, n_ater)
        model.add_edge(n_age_mt_40, n_nevralgia)
        model.add_edge(n_age_mt_40, n_sten)
        model.add_edge(n_age_mt_40, n_ha)

        model.add_edge(n_stress, n_ha)
        model.add_edge(n_stress, n_sten)

        model.add_edge(n_prev_ha, n_ha)

        model.add_edge(n_nevralgia, n_chest_pain)
        model.add_edge(n_nevralgia, n_pain_mt_15min)

        model.add_edge(n_sten, n_chest_pain)
        model.add_edge(n_sten, n_pain_mt_15min)
        model.add_edge(n_sten, n_dyspnea)

        model.add_edge(n_ha, n_chest_pain)
        model.add_edge(n_ha, n_pain_mt_15min)
        model.add_edge(n_ha, n_dyspnea)

        model.bake()

        self.model = model

    def predict(self, X):
        prediction = self.model.predict_proba(X)
        result = []
        for i, state in enumerate(self.model.states):
            code = state.name.lower()
            if code in [key.lower() for key in X]:
                continue
            pred = prediction[i].parameters[0]
            result.append({
                'code': code,
                'name': 'TODO',
                'type': 'TODO',
                'states': pred,
            })
        return result
