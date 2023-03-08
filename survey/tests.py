from main import item

item.set_categories(['verano','invierno'])

p1 = item({'q':'Te gusta el invierno?','r':['si','no']},[1],[],1)
p2 = item({'q':'Te gusta el vernao?','r':['si','no']},[0],[],-1)

print(p1,p2)

p1.answer(2)
p1.answer(2)

p2.answer(2)
p2.answer(1)

p1.calculate_statistics()
p2.calculate_statistics()

print(p1.get_feauture_vector())
print(p2.get_feauture_vector())

p1.print_values()
