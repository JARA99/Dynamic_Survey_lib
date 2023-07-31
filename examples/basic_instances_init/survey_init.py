from pydyn_surv.survey import survey

# Para definir un cuestionario primero definimos una lista de diccionarios con la información de los ítems en este.
# Se utilizan las siguientes categorias

categories = ['Invierno','Primavera','Verano','Otoño']

# Definimos un diccionario con la información del primer ítem
i1_dict = {
    'question':'El invierno me gusta más que el verano',
    'answers':['Muy en desacuerdo','En desacuerdo','Neutral','De acuerdo','Muy de acuerdo'],
    'answers_values':[-2,-1,0,1,2],
    'category_vector':[1,0,-1,0],
    'expert_extra':0,
    'id':0
}

# Definimos un diccionario con la información del segundo ítem
i2_dict = {
    'question':'Me gusta la primavera más que el otoño o el verano',
    'answers':['Muy en desacuerdo','En desacuerdo','Neutral','De acuerdo','Muy de acuerdo'],
    'answers_values':[-2,-1,0,1,2],
    'category_vector':[0,1,-1,-1],
    'expert_extra':0,
    'id':1
}

# Generamos la lista de diccionarios con la información de los ítems
items_list = [i1_dict,i2_dict]

# Definimos una instancia de survey utilizando la lista de diccionarios
survey_instance = survey(items_list,name='Ejemplo de cuestionario',categories=categories)

# Imprimimos información del survey
survey_instance.print_info()

# Obtenemos el primer item utilizando el diccionario de items del cuestionario
i1 = survey_instance.item_by_id[0]

# Obtenemos el segundo item utilizando la posición en la lista de items del cuestionario
i2 = survey_instance.get_items()[1]

# Contestamos al primer item con un punteo de -1 que corresponde a 'En desacuerdo'
i1.answer(-1)

# Contestamos al segundo item con un punteo de 2 que corresponde a 'Muy de acuerdo'
i2.answer(2)


# Obtenemos el set de entrenamiento del cuestionario y lo imprimimos
print('\nEl set de entrenamiento es:\n{}'.format(survey_instance.get_training_dataset()))

# Obtenemos el historial de respuestas por categoría y lo imporimimos
print('\nEl historial de respuestas por categoría es:\n{}'.format(survey_instance.get_category_answer_history()))

# Contestamos una vez más los items
i1.answer(-2)
i2.answer(1)

# Imprimimos información del survey, ahora el training dataset mostrará el hisotrial de respuestas con vectores de categorías y se tendrán etiquetas predichas y calculadas
survey_instance.print_info()

# También es posible obtener un item de dorma pseudoaleatoria en donde se tome en cuenta la probabilidad calculada de cada item
ir,ir_text,ir_answerstext,ir_answersvals = survey_instance.launch_random()

# Imprimimos el item obtenido
print('\nSe obtuvo el ítem: {},\nCuyo enunciado es: {},\nSus posibles respuestas son: {},\nY los valores asociados son: {}'.format(ir.id,ir_text,ir_answerstext,ir_answersvals))

# Este item puede ser contestado, se podría usar el método answer() utilizado antes, pero se ejemplifica ahora el uso del método launch_on_terminal()
survey_instance.launch_on_terminal(ir)

# Volvemos a imprimir información del survey
survey_instance.print_info()

# Este fue un ejemplo básico del uso de la clas survey
