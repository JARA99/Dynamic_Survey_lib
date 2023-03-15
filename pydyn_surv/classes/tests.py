from item import item
from survey import survey

item.set_categories(['verano','invierno'])
item.set_statistics_weights(0,0,0,0)

# p1 = item({'q':'Te gusta el invierno?','a':['si','no']},[2],[],1)
# p2 = item({'q':'Te gusta el verano?','a':['si','no']},[1],[],-1)
# p3 = item({'q':'Te gusta el verano más que el invierno?','a':['si','no']},[1,-2],[],1.5)
# p4 = item({'q':'Te gusta el invierno más que el verano?','a':['si','no']},[-1,2],[],2)

p1t = {
    'question':'Te gusta el invierno?',
    'answers':['si','no'],
    'answers_values':[2,-2],
    'principal_cat_list':[2],
    'secondary_cat_list':[],
    'principal_value':1,
    'secondary_value':0.5,
    'answer_range':(-2,2),
    'expert_extra':0.5
}

p2t = {
    'question':'Te gusta el verano?',
    'answers':['si','no'],
    'answers_values':[2,-2],
    'principal_cat_list':[1],
    'secondary_cat_list':[],
    'principal_value':1,
    'secondary_value':0.5,
    'answer_range':(-2,2),
    'expert_extra':0
}

p3t = {
    'question':'Te gusta el verano más que el invierno?',
    'answers':['si','no'],
    'answers_values':[2,-2],
    'principal_cat_list':[1,-2],
    'secondary_cat_list':[],
    'principal_value':1,
    'secondary_value':0.5,
    'answer_range':(-2,2),
    'expert_extra':0
}

p4t = {
    'question':'Te gusta el invierno más que el verano?',
    'answers':['si','no'],
    'answers_values':[2,-2],
    'principal_cat_list':[-1,2],
    'secondary_cat_list':[],
    'principal_value':1,
    'secondary_value':0.5,
    'answer_range':(-2,2),
    'expert_extra':1
}

p1 = item(p1t)
p2 = item(p2t)
p3 = item(p3t)
p4 = item(p4t)


# print(p1,p2)

p1.answer(2)
p1.answer(-2)
p1.answer(2)
p1.answer(-2)
p1.answer(2)
p1.answer(-2)
p1.answer(2)

p2.answer(2)
p2.answer(1)

p3.answer(-1)

# p1.update_statistics()
# p2.update_statistics()

# print(p1.get_feauture_vector())
# print(p2.get_feauture_vector())
# p1.update_label()
# p1.print_values()
print(p1.get_dataset_pair())
print(p4.get_dataset_pair())

if p1.get_dataset_pair() != None:
    print(p1.get_dataset_pair())

if p4.get_dataset_pair() != None:
    print(p4.get_dataset_pair())

# print()
# p2.print_values()
# # print()
# p3.print_values()
