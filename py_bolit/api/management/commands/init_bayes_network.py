from django.core.management.base import BaseCommand
from py_bolit.api.models import NodeType, Node, State, Probability


class Command(BaseCommand):
    help = 'Insert question with answers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='clear database',
        )

    def handle(self, *args, **options):
        if options['reset']:
            Probability.objects.all().delete()
            State.objects.all().delete()
            Node.objects.all().delete()
            NodeType.objects.all().delete()
            print('Database cleared')

        types = ['diagnosis', 'symptom']
        NodeType.objects.bulk_create([
            NodeType(name=t) for t in types
        ])

        nodes = [
            {
                "code": "smoking",
                "name": "курение",
                "description": "",
                "type": "symptom",
                "states": [
                    "да",
                    "нет"
                ]
            },
            {
                "code": "imt",
                "name": "имт",
                "description": "",
                "type": "symptom",
                "states": [
                    "да",
                    "нет"
                ]
            },
            {
                "code": "age_mt_40",
                "name": "старше 40",
                "description": "",
                "type": "symptom",
                "states": [
                    "да",
                    "нет"
                ]
            },
            {
                "code": "ater",
                "name": "атеросклероз",
                "description": "",
                "type": "symptom",
                "states": [
                    "да",
                    "нет"
                ]
            },
            {
                "code": "stress",
                "name": "стресс",
                "description": "",
                "type": "symptom",
                "states": [
                    "да",
                    "нет"
                ]
            },
            {
                "code": "prev_ha",
                "name": "инфаркт в анамнезе",
                "description": "",
                "type": "symptom",
                "states": [
                    "да",
                    "нет"
                ]
            },
            {
                "code": "ha",
                "name": "инфаркт",
                "description": "",
                "type": "diagnosis",
                "states": [
                    "да",
                    "нет"
                ]
            },
            {
                "code": "sten",
                "name": "стенокардия",
                "description": "",
                "type": "diagnosis",
                "states": [
                    "да",
                    "нет"
                ]
            },
            {
                "code": "nevralgia",
                "name": "невралгия",
                "description": "",
                "type": "diagnosis",
                "states": [
                    "да",
                    "нет"
                ]
            },
            {
                "code": "chest_pain",
                "name": "загрудинные боли",
                "description": "",
                "type": "symptom",
                "states": [
                    "да",
                    "нет"
                ]
            },
            {
                "code": "pain_mt_15min",
                "name": "боли > 15 мин",
                "description": "",
                "type": "symptom",
                "states": [
                    "да",
                    "нет"
                ]
            },
            {
                "code": "dyspnea",
                "name": "одышка",
                "description": "",
                "type": "symptom",
                "states": [
                    "да",
                    "нет"
                ]
            }
        ]
        dists = {
            "smoking": {
                "да": 0.5,
                "нет": 0.5,
            },
            "ater": {
                "да": 0.1,
                "нет": 0.9,
            },
            "imt": {
                "да": 0.3,
                "нет": 0.7,
            },
            "age_mt_40": {
                "да": 0.5,
                "нет": 0.5,
            },
            "stress": {
                "да": 0.2,
                "нет": 0.8,
            },
            "prev_ha": {
                "да": 0.01,
                "нет": 0.99,
            },
            "ha": {
                "да": 0.01,
                "нет": 0.99,
            },
            "sten": {
                "да": 0.01,
                "нет": 0.99,
            },
            "nevralgia": {
                "да": 0.05,
                "нет": 0.95,
            },
            "chest_pain": {
                "да": 0.01,
                "нет": 0.99,
            },
            "pain_mt_15min": {
                "да": 0.01,
                "нет": 0.99,
            },
            "dyspnea": {
                "да": 0.01,
                "нет": 0.99,
            }
        }
        for node in nodes:
            code = node['code']
            n = Node.objects.create(
                code=code,
                name=node['name'],
                type=NodeType.objects.get(name=node['type'])
            )
            for state in node['states']:
                n.states.create(
                    value=state,
                    distribution=dists[code][state]
                )

        probs = [
            {
                "parent": "smoking",
                "child": "ater",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.9,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.1,
                    },
                ]
            },
            {
                "parent": "imt",
                "child": "ater",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.8,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.2,
                    },
                ]
            },
            {
                "parent": "age_mt_40",
                "child": "ater",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.7,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.3,
                    },
                ]
            },
            {
                "parent": "prev_ha",
                "child": "ha",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.5,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.5,
                    },
                ]
            },
            {
                "parent": "stress",
                "child": "ha",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.8,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.2,
                    },
                ]
            },
            {
                "parent": "ater",
                "child": "ha",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.99,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.01,
                    },
                ]
            },
            {
                "parent": "age_mt_40",
                "child": "ha",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.85,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.15,
                    },
                ]
            },
            {
                "parent": "stress",
                "child": "sten",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.8,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.2,
                    },
                ]
            },
            {
                "parent": "ater",
                "child": "sten",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.99,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.01,
                    },
                ]
            },
            {
                "parent": "age_mt_40",
                "child": "sten",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.65,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.35,
                    },
                ]
            },
            {
                "parent": "imt",
                "child": "nevralgia",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.05,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.95,
                    },
                    {
                        "p_state": "нет",
                        "c_state": "да",
                        "value": 0.9,
                    },
                    {
                        "p_state": "нет",
                        "c_state": "нет",
                        "value": 0.1,
                    },
                ],
            },
            {
                "parent": "age_mt_40",
                "child": "nevralgia",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.1,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.9,
                    },
                    {
                        "p_state": "нет",
                        "c_state": "да",
                        "value": 0.9,
                    },
                    {
                        "p_state": "нет",
                        "c_state": "нет",
                        "value": 0.1,
                    },
                ],
            },
            {
                "parent": "nevralgia",
                "child": "chest_pain",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.99,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.01,
                    },
                ]
            },
            {
                "parent": "sten",
                "child": "chest_pain",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.99,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.01,
                    },
                ]
            },
            {
                "parent": "ha",
                "child": "chest_pain",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.99,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.01,
                    },
                ]
            },
            {
                "parent": "nevralgia",
                "child": "pain_mt_15min",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.01,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.99,
                    },
                ]
            },
            {
                "parent": "sten",
                "child": "pain_mt_15min",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.01,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.99,
                    },
                ]
            },
            {
                "parent": "ha",
                "child": "pain_mt_15min",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.99,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.01,
                    },
                ]
            },
            {
                "parent": "sten",
                "child": "dyspnea",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.99,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.01,
                    },
                ]
            },
            {
                "parent": "ha",
                "child": "dyspnea",
                "dists": [
                    {
                        "p_state": "да",
                        "c_state": "да",
                        "value": 0.01,
                    },
                    {
                        "p_state": "да",
                        "c_state": "нет",
                        "value": 0.99,
                    },
                ]
            },
        ]

        for prob in probs:
            parent = State.objects.filter(node__code=prob['parent'])
            child = State.objects.filter(node__code=prob['child'])
            for dist in prob['dists']:
                Probability.objects.create(
                    parent_state=parent.filter(value=dist['p_state']).first(),
                    child_state=child.filter(value=dist['c_state']).first(),
                    value=dist['value']
                )
