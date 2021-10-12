import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(
	__name__,
	external_stylesheets=[]
)
server = app.server

app.layout = html.Div(
	children=[
    	html.H2('Hello World'),
	]
)

if __name__ == '__main__':
    app.run_server(debug=True)
