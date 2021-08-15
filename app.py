import pandas as pd
import optimiser as opt
from utilities import Instance
from pyomo.environ import *
from pyomo.opt import *
import plotly.express as px
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from plotly import graph_objs as go


# Define the stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP,
    #'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap',
    #'https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet'
]

# Creates the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                title="Seguridad alimentaria",
                suppress_callback_exceptions=True)
# need to run it in heroku
server = app.server



# Lectura de datos
# Leer archivos en un dataframe
df = pd.read_excel (r'data\Estudiantes.xlsx')
# crea instancia
instance = Instance(df)
# procesa dataframe
instance.data_process()
instance.create_elementos()


model = opt.create_model(instance)
print(type(model))
df_sol, estu_asig = opt.resolver_opt(instance, model)


# # Número de estudiantes
# print("número de estudiantes: ", df.shape[0] )
# # Obtener función objetivo
# obj_val = model.total_value.expr()
# print("número de asignados: ", int(obj_val))

# Difine el layout
app.layout =html.Div(
            children=[estu_asig]
)

# main to run the app
if __name__ == "__main__":
    app.run_server(debug=True)