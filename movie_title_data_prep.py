import pandas as pd
import re   # Carga  el paquete de las expresiones regulares
from sklearn.utils import shuffle #Carga función para mezclar lineas de .csv aleatoriamente


csv_terror = pd.read_csv('terror_v2.csv', usecols=['Texto'], index_col=False) #Seeleccionamos el file de peliculas
peliculas_terror = csv_terror['Texto'].to_list() #Asignamos a una lista de python
peliculas_terror = [x.strip().lower() for x in peliculas_terror]# Elimina espacio en blanco al final y principio, convierte todas las mayúsculas en minúsculas
peliculas_terror = [re.sub('[?¿,—:!¡#'']', '', x, flags = re.M) for x in peliculas_terror] #elimina puntuación


csv_comedia = pd.read_csv('comedia_v2.csv', usecols=['Texto1'], index_col=False) #Seleccionamos el file de peliculas
peliculas_comedia = csv_comedia['Texto1'].to_list() #Asignamos a una lista de python
peliculas_comedia = [x.strip().lower() for x in peliculas_comedia]# Elimina espacio en blanco al final y principio y convierte todas las mayúsculas en minúsculas
peliculas_comedia = [re.sub('[?¿,—:!¡#]', '', x, flags = re.M) for x in peliculas_comedia] #elimina puntuación

#Definimos funcion que ayudará a mezclar lineas aleatoriamente
def row_shuffler(Dataframe):
    Dataframe = shuffle(Dataframe)
    Dataframe = Dataframe.reset_index(drop=True)
    return Dataframe

#Funcion para enviar datos a .csv
def send_to_csv(Dataframe, name=''):
    Dataframe.to_csv(name, index=False)

#elimina duplicados en ambos datasets (mismo titulo, diferente genero)
for p in peliculas_comedia:
    if p in peliculas_terror:
        peliculas_terror.remove(p)
        peliculas_comedia.remove(p)

#Asigna los géneros correspondientes
genre_dict = {}
for pelicula in peliculas_terror:
    genre_dict[pelicula] = 'Terror'
peliculas_terror = genre_dict

genre_dict = {}
for pelicula in peliculas_comedia:
    genre_dict[pelicula] = 'Comedia'
peliculas_comedia = genre_dict

#Creamos dataframe
df_terror = pd.DataFrame(peliculas_terror.items(), columns=['Pelicula', 'Genero'])
df_comedia = pd.DataFrame(peliculas_comedia.items(), columns=['Pelicula', 'Genero'])

#Mezclamos
df_terror = row_shuffler(df_terror)
df_comedia = row_shuffler(df_comedia)

#100 títulos para dataset final
df_terror = df_terror[:100]
df_comedia = df_comedia[:100]

#Datos compilados en un solo file (200 títulos)
mis_peliculas = pd.concat([df_terror, df_comedia])
mis_peliculas = row_shuffler(mis_peliculas)

send_to_csv(mis_peliculas, name='dataset_completo.csv')

#Tomamos datos random para el set de testeo ...
df_terror = row_shuffler(df_terror)
df_comedia = row_shuffler(df_comedia)

test_data_comedia = df_comedia[:20]
test_data_terror = df_terror[:20]
test_data = pd.concat([test_data_terror, test_data_comedia])
test_data = row_shuffler(test_data)
send_to_csv(test_data, name='test_data.csv')

#... y el de entrenamiento

train_data_comedia = df_comedia[20:]
train_data_terror = df_terror[20:]
train_data = pd.concat([train_data_terror, train_data_comedia])
train_data = row_shuffler(train_data)
send_to_csv(train_data, name='train_data.csv')




print('Archivos listos!!!') #Todos los archivos enviados a la carpeta!







