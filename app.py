import urllib.request
import json
import pandas
import collections
import dash
import dash_core_components as dcc
import dash_html_components as html
import os

api_key = os.getenv('ETHERSCAN_API_KEY')

def fetch_gas(api_key):
    prefix = 'https://api.etherscan.io/api'
    query = f'{prefix}?module=gastracker&action=gasoracle&apikey={api_key}'
    with urllib.request.urlopen(query) as url:
        data = json.loads(url.read().decode())
    return data

def fetch_ring_values(buffer, key):
    return [x['result'][key] for x in buffer]


app = dash.Dash(
	__name__,
	external_stylesheets=[]
)
server = app.server

app.layout = html.Div(
	children=[
    		html.H2('Gas Tracker'),
		dcc.Graph(id='live-update-graph'),
		dcc.Interval(
			id='interval-component',
			interval=1*1000,
			n_intervals=0
		)
	]
)
	
if __name__ == '__main__':
    app.run_server(debug=True)
