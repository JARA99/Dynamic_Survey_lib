from pydyn_surv.classes.item import item

# Configuramos todas las categorías a evaluar en el cuestionario
item.set_categories(['invierno','verano'])

# Definimos un diccionario con la información del ítem
item_dict = {
    'question':'El invierno me gusta más que el verano',
    'answers':['Muy en desacuerdo','En desacuerdo','Neutral','De acuerdo','Muy de acuerdo'],
    'answers_values':[-2,-1,0,1,2],
    'principal_cat_list':[1,-1],
    'expert_extra':0
}

# Definimos una instancia de item utilizando los datos del diccionario
item_instance = item(item_dict)

# Contestamos al item con un punteo de -1 que corresponde a 'En desacuerdo'
item_instance.answer(-1)

# Actualizamos los datos estadísticos del item
item_instance.update_statistics()

# Imprimimos información del item
item_instance.print_values()

# Obtenemos el set de entrenamiento y lo imprimimos
print('\nEl set de entrenamiento es:\n{}'.format(item_instance.dataset_history))

