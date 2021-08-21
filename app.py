import pandas as pd
from dash import no_update

import optimiser as opt
from utilities import Instance
import plotly.express as px
import dash
import dash_table
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
import os




# Define the stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP,
    #'https://codepen.io/chriddyp/pen/bWLwgP.css'
    'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap',
    #'https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet'
]

# Creates the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML',],
                title="Alternancia",
                suppress_callback_exceptions=True)


# need to run it in heroku
server = app.server



# Read data
# Get a dataframe from data
#df = pd.read_csv(r'data\Estudiantes.csv')
df = pd.read_csv(r'https://raw.githubusercontent.com/endorgobio/alternancia/master/data/Estudiantes.csv')

# Create instance
instance = Instance(df)
# Preprocess dataframe
instance.data_process()
instance.create_elementos()

# narratives narratives
filepath = os.path.split(os.path.realpath(__file__))[0]
# narrative tab 1
historia_text = open(os.path.join(filepath, "laHistoria.md"), "r").read()


#narrative tab2
detalles_text = open(os.path.join(filepath, "losDetalles.md"), "r").read()

tab1_content = dbc.Row([
        dbc.Col(dcc.Markdown(historia_text, dangerously_allow_html=True), md=8),
        dbc.Col(html.Div([
            html.Img(src="/assets/images/banner_blue_text.png", className='banner_subsection'),
            #html.H4(children="Los retos", className="header-subtitle"),
            dbc.Card([
                # dbc.CardImg(src="https://source.unsplash.com/daily", top=True),
                #dbc.CardImg(src="/assets/images/banner_blue.png", top=True),
                dbc.CardBody([
                    #html.H6("Reto 1", className="card-title"),
                    html.P(
                        "Expresar la programación de las jornadas de "
                        "alternancia como un modelo matemático y resololverlo "
                        "sin adquirir licencias o software de optimización",
                        style={'textAlign': 'justify'},
                        className="card-text",
                    ),
                ])
            ]),
            dbc.Card([
                # dbc.CardImg(src="https://source.unsplash.com/daily", top=True),
                # dbc.CardImg(src="/assets/images/banner_blue.png", top=True),
                dbc.CardBody([
                    #html.H6("Reto 1", className="card-title"),
                    html.P(
                        "Diseñar una interfaz que permita al tomador de "
                        " decisiones visualizar la solución.",
                        style={'textAlign': 'justify'},
                        className="card-text",
                    ),
                ])
            ]),
            #reto_text
        ]),
            md=4),
    ]
)

# Define content for tab2

controlsmap_text = ''' aaaaaa '''
PAGE_SIZE = 8
# Table of students

# Define controls for the solver
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
                            html.P("Diferencia máxima de genero por curso"),
                            dbc.InputGroup(
                                [
                                    dbc.Input(id="bal_gen", type="number", min=0, max=100, step=1, value=50, placeholder="balance"),
                                    dbc.InputGroupAddon("%", addon_type="append"),
                                ],
                                className="mb-3",
                            ),
                        ]
                    ),
                    dbc.FormGroup(
                        [
                            html.P("Aforo máximo del colegio"),
                            dbc.Input(id="aforo", type="number", min=0, max=len(instance.df), step=1, value=30),
                        ]
                    ),
                    dbc.Button("Resolver", id="resolver", className="mr-2", n_clicks=0),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Detalle de la solución "),
                            dbc.ModalBody(id='modal_text'),
                            dbc.ModalFooter(
                                # dbc.Button(
                                #     "Close", id="close", className="ml-auto", n_clicks=0
                                # )
                            ),
                        ],
                        id="modal",
                        is_open=False,
                    ),
                ]
            ),
        ),
    ]
)

tab2_content = html.Div(
    [
        dbc.Row(
            className="row-with-margin",
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [   # table of students
                                dash_table.DataTable(
                                    id='datatable-paging-page-count',
                                    columns=[
                                        {"name": i, "id": i} for i in ['nombre', 'id', 'nivel', 'genero', 'id_hermanos']
                                    ],
                                    style_table={'overflowX': 'auto'},
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
                dbc.Col(children=[
                    dbc.Row(
                        className="row-with-margin",
                        children=[
                            dbc.Col(dcc.Dropdown(id='fileterEstu',multi=True), md=6),
                            dbc.Col(dbc.Button("Filtrar", id="filtrar", className="mr-2", n_clicks=0), md=1),
                            dbc.Col(dbc.Button("Limpiar", id="limpiar", className="mr-2", n_clicks=0), md=1)
                        ],),
                    dcc.Graph(id="scatterplot")
                    ],
                    md=8
                ),
            ],
            align="center",
        ),
    ]
)

tab3_content = dbc.Row([
        html.Div(id='static',children='$$ x=1 $$'),
        dbc.Col(dcc.Markdown(detalles_text, dangerously_allow_html=True),
                 md=8),
        dbc.Col( md=4),
    ]
)

# Define the layout
app.layout = dbc.Container([
        html.Div(
            children=[
                html.H1(
                    children="Alternancia escolar", className="header-title"
                ),
                html.P(
                    children=html.P(["Optimización  de jornadas escolares",
                                     html.Br(),
                                     " Modelo de alternancia"]),
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
    # dcc.Store inside the app that stores the intermediate value
    dcc.Store(id='data_solver'),
    dcc.Store(id='data_solver_filtered'),
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

# Update table with student information
@app.callback(
    Output('datatable-paging-page-count', 'data'),
    Input('datatable-paging-page-count', "page_current"),
    Input('datatable-paging-page-count', "page_size"))
def update_table(page_current, page_size):
    return df.iloc[page_current*page_size:(page_current+ 1)*page_size].to_dict('records')


# Solve the model or apply filter
@app.callback([Output('data_solver', 'data'),
              Output('data_solver_filtered', 'data'),
              Output('fileterEstu', 'value'),
              Output("modal", "is_open"),
              Output("modal_text", "children")],
              Input('resolver', 'n_clicks'),
              Input('filtrar', 'n_clicks'),
              Input('limpiar', 'n_clicks'),
              State('data_solver', 'data'),
              State('g_minimo', 'value'),
              State('g_maximo', 'value'),
              State('bal_gen', 'value'),
              State('aforo', 'value'),
              State('fileterEstu', 'value')
              )
def run_model_fitler_reset(click_resolver, n_filtrar, n_limpiar,
                     data_solver, g_min, g_max, balance, aforoT, filter_value,
                     ):
    # pop up setting
    estado = False # turn to false and activate the next two lines to not showing it at the beginning
    if click_resolver:
        estado = True

    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'resolver':
        model = opt.create_model(instance,
                                  g_min,
                                  g_max,
                                  balance / 100,
                                  aforoT)
        df_sol, estu_asig = opt.resolver_opt(instance, model)
        data = df_sol[['nombre', 'id', 'L', 'Ma', 'Mi', 'J', 'V']]
        data_scatter = pd.DataFrame(columns=['nombre', 'id', 'dia'])
        nombre_dia = {'L': 'Lunes', 'Ma': 'Martes', 'Mi': 'Miércoles', 'J': 'Jueves', 'V': 'Viernes'}
        for i in range(len(data)):
            for col in ['L', 'Ma', 'Mi', 'J', 'V']:
                if data.loc[i, col] == 1:
                    data_scatter = data_scatter.append({'nombre': df.loc[i, 'nombre'],
                                                      'id': df.loc[i, 'id'],
                                                      'dia': nombre_dia[col]},
                                                     ignore_index=True)
        data_returned = data_scatter.to_json(date_format='iso', orient='split')
        text_popup = "Con los parámetros actuales se logran asignar {} de {} estudiantes.".\
                         format(int(estu_asig),len(instance.df)) + "\r\n Intenta con otros parámetros"
        return data_returned, data_returned, None, estado, text_popup
    elif button_id == 'filtrar':
        data_scatter = pd.read_json(data_solver, orient='split')
        if filter_value:
            data_scatter_filtered = data_scatter[data_scatter['nombre'].isin(filter_value)]
        else:
            data_scatter_filtered = data_scatter
        data_returned = data_scatter_filtered.to_json(date_format='iso', orient='split')
        return data_solver, data_returned, None, False, "aaa"
    elif button_id == 'limpiar':
        return data_solver, data_solver, None, False, "aaa"
    else:
        return (no_update, no_update, no_update)



@app.callback(Output('scatterplot', 'figure'),
              Input('data_solver_filtered', 'data')
              )
def update_scatter(jsonified_sol_data):
    data_scater = pd.read_json(jsonified_sol_data, orient='split')
    fig = px.scatter(data_scater, x='dia', y='nombre',
                     category_orders={"dia": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]}
                     )
    fig.update_traces(marker_size=10)
    fig.update_layout(
        xaxis_title="Día de la semana",
        yaxis_title="Estudiante",
        xaxis_type='category'
    )
    return fig

# Populated dropdown for filtering students
@app.callback(
    Output('fileterEstu', 'options'),
    Input('data_solver', 'data')
)
def dropdown_filter_options(jsonified_sol_data):
    data_scater = pd.read_json(jsonified_sol_data, orient='split')
    data_scater = data_scater[['id', 'nombre']]
    data_scater.sort_values("id", inplace=True)
    # dropping ALL duplicate values
    no_repetead = data_scater.drop_duplicates(keep='first')
    no_repetead.reset_index(inplace=True)
    options = [{'label': no_repetead.loc[i, 'nombre'], 'value': no_repetead.loc[i, 'nombre']} for i in range(len(no_repetead))]
    return options

# # Close modal
# @app.callback(
#     Output('modal', 'is_open'),
#     Input('close', 'nclicks')
# )
# def close_modal(nclicks):
#     return False


# main to run the app
if __name__ == "__main__":
    app.run_server(debug=True)