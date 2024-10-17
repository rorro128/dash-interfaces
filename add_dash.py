import dash
import os
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASS = os.getenv('MYSQL_PASS')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DB = os.getenv('MYSQL_DB')

db_config = mysql.connector.connect(
        user= MYSQL_USER,
        password= MYSQL_PASS,
        host= MYSQL_HOST,
        database= MYSQL_DB
)

app = dash.Dash(__name__)

# Layout principal con links a diferentes páginas
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Cantidad por producto', href='/tipo-1'),
        html.Br(),
        dcc.Link('Cantidad por evento', href='/tipo-2'),
        html.Br(),
        dcc.Link('Cantidad por categoria', href='/tipo-3'),
        html.Br()
    ], className="navigation"),
    html.Div(id='page-content')
])

# Callbacks para actualizar el contenido de la página según la ruta
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/tipo-1':
        return layout_cantidad_producto()
    elif pathname == '/tipo-2':
        return layout_cantidad_evento()
    elif pathname == '/tipo-3':
        return layout_cantidad_categoria()
    else:
        return html.Div([
            html.H3('Bienvenido al Dashboard del Ecommerce.'),
            html.P('Seleccione una de las opciones en la navegación para visualizar los gráficos.')
        ])
##############################  
def layout_cantidad_producto():
    return html.Div([
        html.H3('Distribución de la Tarifa por Puerto de Embarque'),
        dcc.Graph(id='fare-distribution', figure=data_cantidad_producto()),
        dcc.Graph(id='fare-distribution-bar', figure=data_cantidad_producto_bar()),
        dcc.Graph(id='fare-distribution-monto', figure=data_cantidad_monto_bar())
    ])

def data_cantidad_producto():
    df = pd.read_sql('''SELECT product_id, count(product_id) as cantidad, SUM(price) 
                    FROM ecommerce_events GROUP BY product_id ORDER BY sum(price) DESC LIMIT 5''', con=db_config)
    fig = px.pie(df, values='cantidad', names='product_id', title='Cantidad de productos vendidos')
    
    return fig

def data_cantidad_producto_bar():
    df = pd.read_sql('''SELECT product_id, count(product_id) as cantidad, SUM(price) 
                    FROM ecommerce_events GROUP BY product_id ORDER BY sum(price) DESC LIMIT 5''', con=db_config)
    fig = px.bar(df, y='cantidad', x='product_id')
    return fig

def data_cantidad_monto_bar():
    df = pd.read_sql('''SELECT product_id, count(product_id) as cantidad, SUM(price) as total
                    FROM ecommerce_events GROUP BY product_id ORDER BY sum(price) DESC LIMIT 5''', con=db_config)
    fig = px.bar(df, y='total', x='product_id', color='cantidad')
    return fig

################################
def layout_cantidad_evento():
    return html.Div([
        html.H3('Distribución de la Tarifa por Puerto de Embarque'),
        dcc.Graph(id='cantidad-evento', figure=data_cantidad_evento()),
        dcc.Graph(id='cantidad-hora-remove', figure=data_cantidad_hora_remove()),
        dcc.Graph(id='cantidad-hora-view', figure=data_cantidad_hora_view()),
        dcc.Graph(id='cantidad-hora-cart', figure=data_cantidad_hora_cart()),
        dcc.Graph(id='cantidad-hora-purch', figure=data_cantidad_hora_purchase())
    ])
def data_cantidad_evento():
    df = pd.read_sql('''SELECT COUNT(product_id) as cantidad, SUM(price) as total, event_type FROM ecommerce_events GROUP BY event_type''', con=db_config)
    fig = px.pie(df, values='cantidad', names='event_type', title='Cantidad de productos por evento')
    return fig

def data_cantidad_hora_remove():
    df = pd.read_sql('''SELECT HOUR(event_time) as hora, COUNT(product_id) as cantidad FROM ecommerce_events where event_type = 'remove_from_cart' GROUP BY HOUR(event_time)''', con=db_config)
    fig = fig = px.line(df, x='hora', y='cantidad', title='Cantidad de removidos por hora')
    return fig

def data_cantidad_hora_view():
    df = pd.read_sql('''SELECT HOUR(event_time) as hora, COUNT(product_id) as cantidad FROM ecommerce_events where event_type = 'view' GROUP BY HOUR(event_time)''', con=db_config)
    fig = fig = px.line(df, x='hora', y='cantidad', title='Cantidad de vistos por hora')
    return fig

def data_cantidad_hora_cart():
    df = pd.read_sql('''SELECT HOUR(event_time) as hora, COUNT(product_id) as cantidad FROM ecommerce_events where event_type = 'cart' GROUP BY HOUR(event_time)''', con=db_config)
    fig = fig = px.line(df, x='hora', y='cantidad', title='Cantidad de seleccionados por hora')
    return fig

def data_cantidad_hora_purchase():
    df = pd.read_sql('''SELECT HOUR(event_time) as hora, COUNT(product_id) as cantidad FROM ecommerce_events where event_type = 'purchase' GROUP BY HOUR(event_time)''', con=db_config)
    fig = fig = px.line(df, x='hora', y='cantidad', title='Cantidad de productos por comprados')
    return fig

################################

def layout_cantidad_categoria():
    return html.Div([
        html.H3('Distribución de la Tarifa por Puerto de Embarque'),
        dcc.Graph(id='cantidad-evento', figure=data_cantidad_categoria())
    ])
def data_cantidad_categoria():
    df = pd.read_sql('''SELECT category_id, count(category_id) as cantidad, SUM(price) FROM ecommerce_events GROUP BY category_id ORDER BY sum(price) DESC LIMIT 5''', con=db_config)
    fig = px.pie(df, values='cantidad', names='category_id', title='Cantidad de productos por evento')
    return fig


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)