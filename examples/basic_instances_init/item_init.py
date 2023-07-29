from pydyn_surv.item import item

# Definimos un diccionario con la información del ítem
item_dict = {
    'question':'El invierno me gusta más que el verano',
    'answers':['Muy en desacuerdo','En desacuerdo','Neutral','De acuerdo','Muy de acuerdo'],
    'answers_values':[-2,-1,0,1,2],
    'category_vector':[1,-1],
    'expert_extra':0,
    'id':1
}

# Definimos una instancia de item utilizando los datos del diccionario
item_instance = item(item_dict)

# Contestamos al item con un punteo de -1 que corresponde a 'En desacuerdo'
item_instance.answer(-1)

# Imprimimos información del item
item_instance.print_info()

# Obtenemos el set de entrenamiento y lo imprimimos
print('\nEl set de entrenamiento es:\n{}'.format(item_instance.get_dataset_history()))

