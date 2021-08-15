import pandas as pd

class Instance:

    def __init__(self, df):
        self.df = df
        self.ESTUDIANTES = set()
        self.CURSOS = set()
        self.CURSOS = set()
        self.EST_CURSO = {}
        self.DIAS = set()
        self.PATRONES= {}
        self.PAT_DIA = {}
        self.RELACIONES = {}
        self.curso = {} # curso de cada estudiantes
        self.genero = {} # genero de cada estudiante
        self.n_estu = {} # estudiantes por grado

    def data_process(self):
        # Adiciona consecutivos para nombrar las variables
        self.df["var_id"] = self.df.index

        # Convierte genero en dictomica
        self.df['genero_b'] = self.df['genero'].apply(lambda x: 1 if x == "niña" else 0)

        # Lee la columna de hermanos como lista
        def leer_lista(x):
            if type(x) == str:
                return list(x.split(";"))
            elif type(x) == int:
                lista = []
                lista.append(x)
                return lista
            else:
                return x

        self.df["lista_hermanos"] = pd.DataFrame(self.df["id_hermanos"].apply(leer_lista))
        self.df['lista_hermanos'] = self.df['lista_hermanos'].fillna(-99)
        self.df.apply(lambda row: row['lista_hermanos'].append(row['id']) if row['lista_hermanos'] != -99 else -99, axis=1)

        # Convierte lista de hermanos/relaciones en terminos de var_id
        def hermanos_var_id(val_col, dir_ids):
            if val_col != -99:
                lista = []
                if type(val_col) == int:
                    lista.append(val_col)
                else:
                    lista.extend(val_col)
                lista_varid = [id_to_varid[int(x)] for x in lista]

                return sorted(lista_varid)
            else:
                return -99

        id_to_varid = dict(zip(self.df.id, self.df.var_id))
        self.df['test'] = self.df['lista_hermanos'].apply(hermanos_var_id, args=[id_to_varid])

    def create_elementos(self):
        # Conjunto de estudiantes
        self.ESTUDIANTES = set(self.df["var_id"].to_list())
        # Conjunto de cursos
        self.CURSOS = set(self.df["nivel"].unique())
        # Estudiantes por curso
        # EST_CURSO ={}
        grouped = self.df.groupby('nivel')['var_id']
        # for key in grouped.groups.keys():
        # EST_CURSO[key] = set(grouped.groups[key])
        self.EST_CURSO = {key: set(grouped.groups[key]) for key in grouped.groups.keys()}
        # Conjunto de días
        self.DIAS = {'L', 'Ma', 'Mi', 'J', 'V'}
        # Conjunto de patrones (lista de conjuntos)
        self.PATRONES = {1: {'L', 'Mi'}, 2: {'Ma', 'J'}, 3: {'Mi', 'V'}}
        # Patrones por día
        self.PAT_DIA = {i: set() for i in self.DIAS}
        [self.PAT_DIA[dia].add(key) for key in self.PATRONES.keys() for dia in self.PATRONES[key]]
        # Conjunto de relacion-hermandad
        relacion = self.df['test'][self.df['test'] != -99].to_list()
        relacion = [tuple(lista) for lista in relacion]
        values = list(set(relacion))
        values = [set(tup) for tup in values]
        keys = list(range(len(values)))
        self.RELACIONES = dict(zip(keys, values))

        # Parámetros
        self. curso = dict(zip(self.df.var_id, self.df.nivel))
        # genero de los estudioantes
        self.genero = dict(zip(self.df.var_id, self.df.genero_b))
        # Estudiantes por grado
        conteo = self.df[['id', 'nivel']].groupby(['nivel'], as_index=False).count()
        conteo.rename(columns={'id': 'freq'}, inplace=True)
        self.n_estu = dict(zip(conteo.nivel, conteo.freq))





