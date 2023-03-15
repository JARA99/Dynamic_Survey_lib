from pydyn_surv import survey, item
from pydyn_surv import basic_linear_classifier as blc

categories = ['Invierno','Primavera','Verano','Otoño']

Questions = [
    {
    'question':'Me siento agusto con un clima frío.',
    'answers':['Muy en desacuerdo','En desacuerdo','Neutral','De acuerdo','Muy de acuerdo'],
    'principal_cat_list':[1],
    'expert_extra':0
    },
    {
    'question':'Me siento agusto con un clima caluroso.',
    'answers':['Muy en desacuerdo','En desacuerdo','Neutral','De acuerdo','Muy de acuerdo'],
    'principal_cat_list':[3],
    'expert_extra':0
    },
    {
    'question':'Me agrada cuando los árboles tienen hojas verdes.',
    'answers':['Muy en desacuerdo','En desacuerdo','Neutral','De acuerdo','Muy de acuerdo'],
    'principal_cat_list':[2],
    'expert_extra':0
    },
    {
    'question':'Me agrada cuando los suelos se llenan de hojas secas.',
    'answers':['Muy en desacuerdo','En desacuerdo','Neutral','De acuerdo','Muy de acuerdo'],
    'principal_cat_list':[4],
    'expert_extra':0
    },
    {
    'question':'Prefiero un clima frío a uno caluroso.',
    'answers':['Muy en desacuerdo','En desacuerdo','Neutral','De acuerdo','Muy de acuerdo'],
    'principal_cat_list':[1,-3],
    'expert_extra':0
    },
    {
    'question':'Prefiero un clima caluroso a uno frío.',
    'answers':['Muy en desacuerdo','En desacuerdo','Neutral','De acuerdo','Muy de acuerdo'],
    'principal_cat_list':[-1,3],
    'expert_extra':0
    },
    {
    'question':'Prefiero ver las hojas verdes en los árboles a que estén secas y tiradas.',
    'answers':['Muy en desacuerdo','En desacuerdo','Neutral','De acuerdo','Muy de acuerdo'],
    'principal_cat_list':[2,-4],
    'expert_extra':0
    },
    {
    'question':'Prefiero ver las hojas secas y tiradas a verdes y en los árboles',
    'answers':['Muy en desacuerdo','En desacuerdo','Neutral','De acuerdo','Muy de acuerdo'],
    'principal_cat_list':[-2,4],
    'expert_extra':0
    },
]

item.item.set_categories(categories)

survey1 = survey.survey(Questions,'Cuestionario sobre estaciones del año')

a = item.item()

# print(survey1.get_feature_vectors())

print(survey1.get_training_dataset())

survey1.items[0].answer(2)

print(survey1.items[0].answer_history)

print(survey1.get_feature_vectors())

print(survey1.get_training_dataset())

survey1.print_items()
survey1.print_item_info(3)

survey1.launch_item(3)

survey1.print_item_info(3)


