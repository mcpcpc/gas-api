import urllib.request
import json
import dash
import dash_daq as daq
from dash import dcc
from dash import html
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
        html.P(id='live-update-block'),
        html.Div(
            className='cards',
            children=[
                daq.Gauge(
                    id='live-update-safe',
                    showCurrentValue=True,
                    units="GWEI",
                    label='Safe Gas Price',
                    max=1000,
                    min=0,
                    value=0
                ),
                daq.Gauge(
                    id='live-update-propose',
                    showCurrentValue=True,
                    units="GWEI",
                    label='Suggested Gas Price',
                    max=1000,
                    min=0,
                    value=0
                ),
                daq.Gauge(
                    id='live-update-fast',
                    showCurrentValue=True,
                    units="GWEI",
                    label='Fast Gas Price',
                    max=1000,
                    min=0,
                    value=0
                ),
            ],
        ),
		dcc.Interval(
			id='interval-component',
			interval=1*1000,
			n_intervals=0
		)
	]
)

@app.callback(
    dash.Output('live-update-block', 'children'),
	dash.Output('live-update-safe', 'value'),
    dash.Output('live-update-propose', 'value'),
    dash.Output('live-update-fast', 'value'),
	dash.Input('interval-component', 'n_intervals'))
def update_gas(n):
	g = fetch_gas(api_key)
	block=safe=propose=fast = 0
	if g['status'] == '1':
		block = g['result']['LastBlock']
		safe = int(g['result']['SafeGasPrice'])
		propose = int(g['result']['ProposeGasPrice'])
		fast = int(g['result']['FastGasPrice'])
	return f'Last Block: {block}', safe, propose, fast 
	

if __name__ == '__main__':
    app.run_server(debug=True)
