import urllib.request
import json
import dash
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
		html.Div(
            className='metric',
            children=[
                html.Div(className='metric',
                    children=[
                        html.Div(className='metric-inner',
                            children=[
                                html.Header(className='metric-header',
                                    children=[
                                        html.H1('Safe Gas Price', className='metric-title'),
                                    ],	
                                ),
                                html.Div(className='metric-body',
                                    children=[
                                        html.Div(className='value',
                                            children=[
                                                html.H1(id='live-update-safe'),
                                                html.H2('GWEI'),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(className='metric',
                    children=[
                        html.Div(className='metric-inner',
                            children=[
                                html.Header(className='metric-header',
                                    children=[
                                        html.H1('Propose Gas Price', className='metric-title'),
                                    ],	
                                ),
                                html.Div(className='metric-body',
                                    children=[
                                        html.Div(className='value',
                                            children=[
                                                html.H1(id='live-update-propose'),
                                                html.H2('GWEI'),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(className='metric',
                    children=[
                        html.Div(className='metric-inner',
                            children=[
                                html.Header(className='metric-header',
                                    children=[
                                        html.H1('Fast Gas Price', className='metric-title'),
                                    ],	
                                ),
                                html.Div(className='metric-body',
                                    children=[
                                        html.Div(className='value',
                                            children=[
                                                html.H1(id='live-update-fast'),
                                                html.H2('GWEI'),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
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
	dash.Output('live-update-safe', 'children'),
    dash.Output('live-update-propose', 'children'),
    dash.Output('live-update-fast', 'children'),
	dash.Input('interval-component', 'n_intervals'))
def update_gas(n):
	g = fetch_gas(api_key)
	return g['result']['SafeGasPrice'],g['result']['ProposeGasPrice'],g['result']['FastGasPrice']
	

if __name__ == '__main__':
    app.run_server(debug=True)
