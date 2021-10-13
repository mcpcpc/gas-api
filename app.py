import urllib.request
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import os

api_key = os.getenv('ETHERSCAN_API_KEY')

def fetch_gas(api_key):
    query = f'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={api_key}'
    with urllib.request.urlopen(query) as url:
        data = json.loads(url.read().decode())
    return data

app = dash.Dash(
	__name__,
	update_title=None,
	meta_tags=[
		{'name':'viewport','content':'width=device-width, initial-scale=1'}
	],
	external_stylesheets=[]
)
server = app.server

app.layout = html.Div(
	children=[
    		html.H2('Etherscan Gas Tracker'),
		html.Hr(),
		html.Div(id='live-update-text'),
		dcc.Interval(
			id='interval-component',
			interval=1*1000,
			n_intervals=0
		)
	]
)

@app.callback(
	dash.Output('live-update-text', 'children'),
	dash.Input('interval-component', 'n_intervals'))
def update_gas(n):
	g = fetch_gas(api_key)
	if g['status'] == '1':
		safe = g['result']['SafeGasPrice']
		propose = g['result']['ProposeGasPrice']
		fast = g['result']['FastGasPrice']
		block = g['result']['LastBlock']
		results = f'Safe Gas Price: {safe} Gwei, Propose Gas Price: {propose} Gwei, Fast Gas Price: {fast} Gwei, Last Block {block}'
	else:
		results = None
	return [
		html.Label('Safe Gas Price'),
		html.P(safe),
		html.Label('Propose Gas Price'),
		html.P(propose),
		html.Label('Fast Gas Price'),
		html.P(fast),
	]
	

if __name__ == '__main__':
    app.run_server(debug=True)
