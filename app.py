import pandas as pd
import optimiser as opt
from utilities import Instance
import plotly.express as px
import dash
import dash_table
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
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





controlmodel_text = '''
    * Seleccione en el menú desplegable el producto de interes
    * En el gráfico active o desactive las ciudades que desea comparar
    '''
controls_model = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.FormGroup(
                        [
                            html.P("Mínimo de estudiantes por curso"),
                            dbc.Input(id="g_minimo", type="number", min=1, max=len(instance.df), step=1, value=2),
                        ]
                    ),
                    dbc.FormGroup(
                        [
                            html.P("Máximo de estudiantes por curso"),
                            dbc.Input(id="g_maximo", type="number", min=1, max=len(instance.df), step=1, value=20),
                        ]
                    ),
                    dbc.FormGroup(
                        [
                            html.P("Diferencia máxima de genero por curso (%)"),
                            dbc.Input(id="bal_gen", type="number", min=0, max=100, step=1, value=50),
                        ]
                    ),
                    # dbc.FormGroup(
                    #     [
                    #         html.P("Diferencia máxima de genero por curso"),
                    #         dbc.InputGroup(
                    #             [
                    #                 dbc.Input(id="bal_gen", type="number", min=0, max=100, step=1, value=50, placeholder="balance"),
                    #                 dbc.InputGroupAddon("%", addon_type="append"),
                    #             ],
                    #             className="mb-3",
                    #         ),
                    #     ]
                    # ),
                    dbc.FormGroup(
                        [
                            html.P("Aforo máximo del colegio"),
                            dbc.Input(id="aforo", type="number", min=0, max=len(instance.df), step=1, value=30),
                        ]
                    ),
                    dbc.Button(
                        "Resolver", id="resolver", className="mr-2", n_clicks=0
                    ),
                ]
            ),
        ),
    ]
)


# # Número de estudiantes
# print("número de estudiantes: ", df.shape[0] )
# # Obtener función objetivo
# obj_val = model.total_value.expr()
# print("número de asignados: ", int(obj_val))


# initial text
tab1_text = dcc.Markdown('''
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis et sapien eu purus malesuada rutrum non sed tortor. 
Phasellus iaculis, ipsum id vulputate euismod, ex purus varius justo, in sollicitudin risus purus sodales diam. 
Mauris sed commodo neque. Aliquam at urna scelerisque ante ornare rutrum. Vestibulum in dui at arcu fringilla 
molestie. Phasellus sollicitudin porta massa, blandit suscipit velit aliquet id. Integer efficitur, libero ut 
consectetur fermentum, est massa feugiat ligula, sed facilisis urna arcu sit amet turpis. Maecenas malesuada 
neque eu felis eleifend accumsan. Nulla posuere cursus nunc eget dictum.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis et sapien eu purus malesuada rutrum non sed tortor. 
Phasellus iaculis, ipsum id vulputate euismod, ex purus varius justo, in sollicitudin risus purus sodales diam. 
Mauris sed commodo neque. Aliquam at urna scelerisque ante ornare rutrum. Vestibulum in dui at arcu fringilla 
molestie. Phasellus sollicitudin porta massa, blandit suscipit velit aliquet id. Integer efficitur, libero ut 
consectetur fermentum, est massa feugiat ligula, sed facilisis urna arcu sit amet turpis. Maecenas malesuada 
neque eu felis eleifend accumsan. Nulla posuere cursus nunc eget dictum.
''')

reto_text = dcc.Markdown('''
* ** Reto 1**: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis et sapien eu purus malesuada rutrum non sed tortor. 
Phasellus iaculis
* **Reto 2**:  est massa feugiat ligula, sed facilisis urna arcu sit amet turpis. Maecenas malesuada 
neque eu felis eleifend accumsan. Nulla posuere cur
''')


tab1_content = dbc.Row([
        dbc.Col(tab1_text, md=8),
        dbc.Col(html.Div([
            html.H4(
                    children="Los retos", className="header-subtitle"
                ),
            reto_text]
        ),
            md=4),
    ]
)

controlsmap_text = ''' aaaaaa '''
PAGE_SIZE = 5
tab2_content = html.Div(
    [
        dbc.Row(
            className="row-with-margin",
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dash_table.DataTable(
                                    id='datatable-paging-page-count',
                                    columns=[
                                        {"name": i, "id": i} for i in ['nombre', 'id', 'nivel', 'genero', 'id_hermanos']
                                        # df.columns
                                    ],
                                    style_table={'overflowX': 'auto'},
                                    #style_cell={'textAlign': 'left', },
                                    style_cell_conditional=[
                                        {'if': {'column_id': 'nombre'},
                                         'width': '35%'},
                                        {'if': {'column_id': 'id'},
                                         'width': '12%'},
                                        {'if': {'column_id': 'nivel'},
                                         'width': '12%'},
                                        {'if': {'column_id': 'genero'},
                                         'width': '12%'},
                                        {'if': {'column_id': 'id_hermanos'},
                                         'width': '27%'},
                                    ],

                                    css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                                    style_cell={
                                        'textAlign': 'left',
                                        'width': '{}%'.format(len(df.columns)),
                                        'textOverflow': 'ellipsis',
                                        'overflow': 'hidden'
                                    },
                                    style_as_list_view=True,
                                    page_current=0,
                                    page_size=PAGE_SIZE,
                                    page_action='custom'
                                ),
                            ]
                        )
                    ),
                    md=12
                ),
            ],
            align="center",

        ),
        # Line graph and controls
        dbc.Row(
            className="row-with-margin",
            children=[
                dbc.Col(controls_model,
                        md=4),
                dbc.Col(
                    dcc.Graph(id="heatmap"),
                    # dbc.Card(
                    #     dbc.CardBody(
                    #         [
                    #             # html.Div(dcc.Graph(id="heatmap"),
                    #             #          style={'overflowY': 'scroll', 'height': 750}
                    #             #          )
                    #             # #html.Div(id='my-output'),
                    #         ]
                    #     )
                    # ),
                    md=8
                ),
            ],
            align="center",
        ),
    ]
)

tab3_content = dbc.Row([
        dbc.Col(html.Div([
            html.H4(
                    children="Los retos3", className="header-subtitle"
                )]
        ),
            md=4),
    ]
)

# Define the layout
app.layout = dbc.Container([
        html.Div(
            children=[
                html.H1(
                    children="Oferta-Demanda", className="header-title"
                ),
                html.P(
                    children="Herramientas de análisis del precio de los productos "
                             " agrícolas en las distintas plazas de mercado",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        dbc.Tabs(
            [
                dbc.Tab(label="La historia", tab_id="historia"),
                dbc.Tab(label="La solución", tab_id="solucion"),
                dbc.Tab(label="Los detalles", tab_id="detalles"),
            ],
            id="tabs",
            active_tab="historia",
        ),
        dbc.Row(id="tab-content", className="p-4"),
    ],
    fluid=True,
)

# Render the tabs depending on the selection
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab == "historia":
        return tab1_content
    elif active_tab == "solucion":
        return tab2_content
    elif active_tab == "detalles":
        return tab3_content


# Solve the model
@app.callback(Output('heatmap', 'figure'),
              Input('resolver', 'n_clicks'),
              State('g_minimo', 'value'),
              State('g_maximo', 'value'),
              State('bal_gen', 'value'),
              State('aforo', 'value')
)
def update_model_run(n_clicks, g_min, g_max, balance, aforoT):
    model = opt.create_model(instance,
                             g_min,
                             g_max,
                             balance/100,
                             aforoT)
    df_sol, estu_asig = opt.resolver_opt(instance, model)
    print(estu_asig)
    data = df_sol[['nombre', 'id', 'L', 'Ma', 'Mi', 'J', 'V']]
    data_scater = pd.DataFrame(columns = ['nombre', 'id', 'dia'])
    for i in range(len(data)):
        for col in ['L', 'Ma', 'Mi', 'J', 'V']:
            if data.loc[i, col] == 1:
                data_scater = data_scater.append({'nombre': df.loc[i, 'nombre'],
                                                  'id': df.loc[i, 'id'],
                                                  'dia': col},
                                                 ignore_index=True)

    #data = df_sol[['L', 'Ma', 'Mi', 'J', 'V']]
    #fig = px.imshow(data)
    # fig = px.imshow(data,
    #                 labels=dict(x="Day of Week", y="Time of Day"),
    #                 x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    #                 y=df_sol.id.astype('str'),
    #                 )
    # fig.update_traces(showscale=False)
    #print(data_scater.head())
    fig = px.scatter(x=data_scater.dia, y=data_scater.nombre)
    return fig

# Update table with student information
@app.callback(
    Output('datatable-paging-page-count', 'data'),
    Input('datatable-paging-page-count', "page_current"),
    Input('datatable-paging-page-count', "page_size"))
def update_table(page_current,page_size):
    return df.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

# main to run the app
if __name__ == "__main__":
    app.run_server(debug=True)