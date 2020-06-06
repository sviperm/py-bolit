from copy import deepcopy
from itertools import product

import numpy as np
from django.db.models import Q
from pomegranate import (BayesianNetwork, ConditionalProbabilityTable,
                         DiscreteDistribution, State)

from .models import Node, Probability


def generate_CPT(event, dependencies):
    deps = deepcopy(dependencies)

    for dep in deps:
        if len(set(d['p_state'] for d in dep)) < 2:
            for state, value in event.items():
                dep.append({
                    'p_state': 'нет',
                    'c_state': state,
                    'value': value,
                })

    e_states = list(event.keys())

    d_states = []
    for dep in deps:
        d_states.append(list(set(d['p_state'] for d in dep)))

    table = [list(i) for i in product(*d_states, e_states)]

    for row in table:
        e_state = row[-1]
        formula = []

        for i, state in enumerate(row[:-1]):
            f = [d['value'] for d in deps[i]
                 if (d['p_state'] == state) and (d['c_state'] == e_state)][0]
            formula.append(f)

        formula = 1 - np.prod(1 - np.array(formula))
        row.append(formula)

    states = len(e_states)
    sums = np.array(table)[:, -1].reshape(-1, states).astype(np.float).sum(axis=1)

    for i, row in enumerate(table):
        row[-1] = row[-1] / sums[int(i / states)]
        row[-1] = round(row[-1], 3)
    return table


discrete_distr = Node.get_discrete_distribution()
probabilities = Probability.get_all()

# Курение
smoking = DiscreteDistribution(discrete_distr['smoking'])

# ИМТ (худой, полный)
imt = DiscreteDistribution(discrete_distr['imt'])

# Старше 40 лет
age_mt_40 = DiscreteDistribution(discrete_distr['age_mt_40'])

# Атеросклероз
ater = ConditionalProbabilityTable(
    generate_CPT(discrete_distr['ater'],
                 [probabilities['smoking__ater'], probabilities['imt__ater'], probabilities['age_mt_40__ater']]),
    [smoking, imt, age_mt_40]
)

# Стресс
stress = DiscreteDistribution(discrete_distr['stress'])

# Инфаркт в анамнезе
prev_ha = DiscreteDistribution(discrete_distr['prev_ha'])

# Инфаркт
ha = ConditionalProbabilityTable(
    generate_CPT(discrete_distr['ha'],
                 [probabilities['prev_ha__ha'], probabilities['stress__ha'], probabilities['ater__ha'], probabilities['age_mt_40__ha']]),
    [prev_ha, stress, ater, age_mt_40]
)

# Стенокардия
sten = ConditionalProbabilityTable(
    generate_CPT(discrete_distr['sten'],
                 [probabilities['stress__sten'], probabilities['ater__sten'], probabilities['age_mt_40__sten']]),
    [stress, ater, age_mt_40]
)

# Межреберная невралгия
nevralgia = ConditionalProbabilityTable(
    generate_CPT(discrete_distr['nevralgia'],
                 [probabilities['imt__nevralgia'], probabilities['age_mt_40__nevralgia']]),
    [imt, age_mt_40]
)

# Загрудинные боли
chest_pain = ConditionalProbabilityTable(
    generate_CPT(discrete_distr['chest_pain'],
                 [probabilities['nevralgia__chest_pain'], probabilities['sten__chest_pain'], probabilities['ha__chest_pain']]),
    [nevralgia, sten, ha]
)

# Боли > 15 мин
pain_mt_15min = ConditionalProbabilityTable(
    generate_CPT(discrete_distr['pain_mt_15min'],
                 [probabilities['nevralgia__pain_mt_15min'], probabilities['sten__pain_mt_15min'], probabilities['ha__pain_mt_15min']]),
    [nevralgia, sten, ha]
)

# Одышка
dyspnea = ConditionalProbabilityTable(
    generate_CPT(discrete_distr['dyspnea'],
                 [probabilities['sten__dyspnea'], probabilities['ha__dyspnea']]),
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
        keys = [key.lower() for key in X]
        nodes = Node.objects.filter(~Q(code__in=keys)).values('code', 'name', 'type__name')
        for i, state in enumerate(self.model.states):
            code = state.name.lower()
            if code in keys:
                continue
            pred = prediction[i].parameters[0]
            node = [n for n in nodes if code == n['code']][0]
            result.append({
                'code': code,
                'name': node['name'],
                'type': node['type__name'],
                'states': pred,
            })
        return result
