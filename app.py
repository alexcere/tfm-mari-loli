# Import required libraries
import base64
import io
import os
import pathlib
from os import listdir
from os.path import join, isfile
from PIL import Image
import matplotlib.image as mpimg
from dash.exceptions import PreventUpdate
from plots import *

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = (PATH.joinpath("data")).resolve()

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

# workpath = os.path.dirname(os.path.abspath(__file__))
# os.chdir(workpath)
onlyfiles = [f for f in listdir(str(DATA_PATH)) if isfile(join(str(DATA_PATH), f))]

message1 = "El desarrollo de este proyecto que nos ocupa se sitúa en lo cotidiano e inadvertido que el ámbito doméstico " \
           "revela tras sus figuras, convirtiendo esta serie de aspectos comunes en un motivo de causa para generar " \
           "espacios de reflexión e investigación. Partiendo de una experiencia personal en un piso compartido cubierto " \
           "de humedades, surge una idea de relación entre dos eventos que, pese a representar una razonable contraposición, " \
           "acogen en su naturaleza comportamientos similares."

message2 = " Lo que a primera vista puede parecer insignificante, como " \
           "una pequeña gota de agua, si su reproducción se repite de forma constante puede llegar a desarrollar el desbordamiento " \
           "de un caudal irrefrenable, desdibujando y construyendo al tiempo la imagen de un nuevo paisaje en tránsito. " \
           "Todo este proceso de transformación puede verse no sólo en la vivienda y su imagen, sino en la corporalidad y " \
           "en los hábitos del individuo que la ocupa."


app.title="Paisajes en zonas de tránsito"
# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="current-gray"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            "Paisajes en zonas de tránsito",
                            style={"margin-bottom": "0px"},
                        ),
                        html.H4(
                            "Orografía emocional de la vivienda", style={"margin-top": "0px"}
                        ),
                    ]
                )
            ],
            id="header",
            style={"margin-bottom": "25px", "text-align" : "center"},),
        # html.Div(
        #     [
        #         html.P(
        #             message1,
        #             className="description-1",
        #             style={"text-align" : "justify"},
        #         ),
        #         html.P(
        #             message2,
        #             className="description-1",
        #             style={"text-align" : "justify"},
        #         ),
        #     ],
        #     id="description_container",
        #     className="pretty_container",
        # ),
        html.Div(
            [
                html.H3("Humedades en relieve: Génesis de paisajes"),
            ],
            style={"margin-top" : "25px", "margin-bottom": "25px", "text-align" : "center"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("personal-text.jpg"),
                            style={"align-items": "center", "width" : "100%"}
                        ),
                    ],
                    className="pretty_container six columns"
                ),
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("INFOGRAFIA.jpg"),
                            style={"align-items": "center", "width" : "100%"}
                        ),
                    ],
                    className="pretty_container six columns"
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.H3("Humedades en relieve: Exploración del paisaje en tránsito"),
            ],
            style={"margin-top" : "25px", "margin-bottom": "25px", "text-align" : "center"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Puedes seleccionar una imagen de la galería de humedades:",
                        ),
                        dcc.Dropdown(
                            id='file-select',
                            options= [{'label': val.rsplit('.',1)[0], 'value': val.rsplit('.',1)[0]} for val in onlyfiles],
                            style={
                                'textAlign': 'center',
                                'margin' : '5px',
                            },
                            value='Humedad I',
                        ),
                        html.P(
                            "o puedes subir una foto en formato PNG de una humedad sobre la que generar el proceso:",
                        ),
                        dcc.Upload(
                            id='upload-image',
                            children=html.Div([
                                'Arrastra o ',
                                html.A('Selecciona un archivo')
                            ]),
                            style={
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            # Allow multiple files to be uploaded
                            # multiple=True,
                            # className=""
                        ),
                        html.P(
                            "Elección de color para las figuras",
                        ),
                        dcc.RadioItems(
                            id='color-select',
                            options= [
                                {'label': "Terreno", 'value': 'terrain'},
                                {'label': "Escala de grises", 'value': 'Greys'}
                            ],
                            # style={
                            #     'textAlign': 'center',
                            # },
                            value='terrain',
                        ),
                    ],
                    className="pretty_container five columns",
                    id="parameter-selection",
                ),
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='original-image'))
                    ],
                    id="imagen-original container",
                    className="pretty_container seven columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [

                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='transformed-image'))
                    ],
                    id="transformed image container",
                    className="pretty_container five columns",
                ),
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='3d-cenital'))
                    ],
                    id="3d cenital container",
                    className="pretty_container seven columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [

                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='contour')),
                    ],
                    id="contour-container",
                    className="pretty_container five columns",
                ),
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id='3d-above')),
                    ],
                    id="3d-above-container",
                    className="pretty_container seven columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.H3("Humedades en relieve: Sibilancia y otras sinfonías"),
            ],
            style={"margin-top" : "25px", "margin-bottom": "25px", "text-align" : "center"},
        ),
        html.Div(
            [
                html.Video(
                    id='movie_player',
                    controls=True,
                    src=app.get_asset_url("output.webm"),
                    className="pretty_container six columns"
                ),
                html.Img(
                    id='waves',
                    src=app.get_asset_url("breather-energy.png"),
                    className="pretty_container six columns"
                )
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


@app.callback([Output('original-image', 'figure'), Output('transformed-image', 'figure'),
               Output('3d-cenital', 'figure'),
               Output('contour', 'figure'), Output('3d-above', 'figure')],
              [Input('current-gray', 'data'), Input('color-select', 'value')])
def update_displayed_graphs(img, colorname):
    if img is None:
        raise PreventUpdate
    img = np.asarray(img)
    gray = generate_process(img)
    return [plotly_imshow_plain_figure(img),
            plotly_imshow_plain_figure_gray(gray), plotly_surface_plot_isometric(gray, colorname),
            plotly_contour_lines(gray, colorname), plotly_surface_plot_from_above(gray,colorname)]


def update_graphs_from_upload(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return np.asarray(Image.open(io.BytesIO(decoded)))


def update_graphs_from_examples(filename):
    return mpimg.imread(str(DATA_PATH) + "/" + str(filename) + '.png')


@app.callback(Output('current-gray', 'data'),
              [Input('file-select', 'value'), Input('upload-image', 'contents')])
def update_graphs(filename, contents):
    ctx = dash.callback_context

    change = ctx.triggered[0]['prop_id'].split('.')[0]
    if change == 'file-select':
        if filename is None:
            raise PreventUpdate
        return update_graphs_from_examples(filename)
    elif change == 'upload-image':
        return update_graphs_from_upload(contents)
    else:
        if filename is None:
            raise PreventUpdate
        return update_graphs_from_examples(filename)

server = app.server

# Main
if __name__ == "__main__":
    app.run_server()
