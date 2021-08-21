import pandas as pd
from pyomo.environ import *
from pyomo.opt import *

def create_model(instance,
                 n_min=2,  # tamaño mínimo de curso
                 n_max=20,  # tamaño máximo de grupo
                 bal_gen=0.68,  # Diferencia en el balanceo por genero
                 aforo=30): # Aforo del colegio):

    # Define el modelo
    # Crea el modelo
    model = ConcreteModel(name="alternancia")

    # Crea conjuntos
    model.E = Set(initialize=instance.ESTUDIANTES, ordered=False)
    model.C = Set(initialize=instance.CURSOS, ordered=False)
    model.Ec = Set(model.C, initialize=instance.EST_CURSO, ordered=False)
    model.D = Set(initialize=instance.DIAS, ordered=False)
    model.P = Set(initialize=set(instance.PATRONES.keys()), ordered=False)
    model.Pi = Set(model.P, initialize=instance.PATRONES, ordered=False)
    model.PD = Set(model.D, initialize=instance.PAT_DIA, ordered=False)
    model.H = Set(initialize=set(instance.RELACIONES.keys()), ordered=False)
    model.Hi = Set(model.H, initialize=instance.RELACIONES, ordered=False)

    # Crea Parámetros
    model.curso_est = Param(model.E, initialize=instance.curso)
    model.genero_est = Param(model.E, initialize=instance.genero)
    model.n_estu = Param(model.C, initialize=instance.n_estu)
    model.bal_gen = Param(initialize=bal_gen)
    model.aforo = Param(initialize=aforo)
    model.nmin = Param(initialize=n_min)
    model.nmax = Param(initialize=n_max)

    # Define variables
    model.x = Var(model.E, model.P, within=Binary)  # Asignacion
    model.y = Var(model.H, model.P, within=Binary)  # Patron para relacion
    model.z = Var(model.C, model.D, within=Binary)  # Abrir curso-dia
    model.w = Var(model.C, model.D, within=NonNegativeReals)  # linealizar balance

    # Define función objetivo
    def value_rule(model):
        return sum(sum(model.x[i, k] for i in model.E) for k in model.P)

    model.total_value = Objective(sense=maximize, rule=value_rule)

    # Define restricciones
    # 1. Restricción cobertura
    def cobertura_rule(model, i):
        return sum(model.x[i, k] for k in model.P) <= 1

    model.cobertura = Constraint(model.E, rule=cobertura_rule)

    # 2. Consistencia en hermandad/relación
    def consistencia_rule(model, l, k):
        return sum(model.x[i, k] for i in model.Hi[l]) == len(model.Hi[l]) * model.y[l, k]

    model.consistencia = Constraint(model.H, model.P, rule=consistencia_rule)

    # 3. Tamaño mínimo y máximo de los grupos
    def tamanoming_rule(model, j, d):
        return sum(sum(model.x[i, k] for i in model.Ec[j]) for k in model.PD[d]) >= model.nmin * model.z[j, d]

    model.tamanoming = Constraint(model.C, model.D, rule=tamanoming_rule)

    def tamanomaxg_rule(model, j, d):
        return sum(sum(model.x[i, k] for i in model.Ec[j]) for k in model.PD[d]) <= model.nmax * model.z[j, d]

    model.tamanomaxg = Constraint(model.C, model.D, rule=tamanomaxg_rule)

    # 4. Balance niñas-niños
    def linear_abs_pos_rule(model, j, d):
        return sum(sum(model.x[i, k] * model.genero_est[i] for i in model.Ec[j]) for k in model.PD[d]) - sum(
            sum(model.x[i, k] * (1 - model.genero_est[i]) for i in model.Ec[j]) for k in model.PD[d]) <= model.w[j, d]

    model.linear_abs_pos = Constraint(model.C, model.D, rule=linear_abs_pos_rule)

    def linear_abs_neg_rule(model, j, d):
        return -(sum(sum(model.x[i, k] * model.genero_est[i] for i in model.Ec[j]) for k in model.PD[d]) - sum(
            sum(model.x[i, k] * (1 - model.genero_est[i]) for i in model.Ec[j]) for k in model.PD[d])) <= model.w[j, d]

    model.linear_abs_neg = Constraint(model.C, model.D, rule=linear_abs_neg_rule)

    def balance_rule(model, j, d):
        return model.w[j, d] <= (sum(sum(model.x[i, k] for i in model.Ec[j]) for k in model.PD[d])) * model.bal_gen

    model.balance = Constraint(model.C, model.D, rule=balance_rule)

    # 5. Aforo colegio
    def aforo_rule(model, d):
        return (sum(sum(model.x[i, k] for i in model.E) for k in model.PD[d])) <= model.aforo

    model.aforocol = Constraint(model.D, rule=aforo_rule)



    return model

def resolver_opt(instance,
                 model,
                 solvername = 'glpk',
                 solverpath_exe = 'D:\\glpk-4.65\\w64\\glpsol'):
    # Configura optimizador
    # solvername = 'glpk'
    # solverpath_exe = 'C:\\glpk-4.65\\w64\\glpsol'
    # solver = SolverFactory(solvername, executable=solverpath_exe)
    solver = SolverFactory(solvername)
    solver.options['tmlim'] = 5

    # Resuelve el modelo
    solver.solve(model, options_string="mipgap=0.02")
    # Obtener variables de decisión
    res = model.x.get_values()

    # Guarda la solución en el dataframe
    column_names = ['var_id', 'Patron', 'L', 'Ma', 'Mi', 'J', 'V']
    DIAS = ['L', 'Ma', 'Mi', 'J', 'V']
    df_sol = pd.DataFrame(columns=column_names)
    for key, value in res.items():
        if value > 0:
            row = [key[0], key[1]]
            for dia in DIAS:
                if dia in instance.PATRONES[key[1]]:
                    row.append(1)
                else:
                    row.append(0)
            df_sol.loc[len(df_sol.index)] = row

    # Une el dataframe de la solucion con el dataframe original
    df_merged = pd.merge(instance.df, df_sol, on='var_id')

    # Número de estudiantes asignados
    assig_estu = model.total_value.expr()
    return df_merged, assig_estu