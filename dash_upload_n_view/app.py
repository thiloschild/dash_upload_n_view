import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_upload_n_view.functions import create_upload, create_table, parse_csv, read_settings


# create the dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
# read settings to the app
app.settings = read_settings('./setting.toml')

# define some id's
upload_component_id = "uci"
table_id = "ti"

# define the layout
layout = html.Div([
    html.H3("Upload or Copy a CSV-File and see the Content in a Table"),
    html.Br(),
    create_upload(upload_component_id),
], style=app.settings["page_style"])


@app.callback(
    Output(upload_component_id+'output', 'children'),
    [Input(upload_component_id+'upload', 'filename'),
     Input(upload_component_id+'upload', 'contents')],
    Input(upload_component_id+'copy', 'n_clicks')
)
def parse_upload(filename, contents, n_clicks):
    """ Returns a Table with the parsed data """
    # check which callback triggered
    ctx = dash.callback_context
    if not ctx.triggered:
        input_id = None
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if filename is not None and contents is not None and 'upload' in input_id:
        df = parse_csv(filename, contents)
        if type(df) == str:
            # wrong file format -> return error message
            return dbc.Alert("You must select a csv!", color="primary")
        else:
            return create_table(table_id, df)
    elif n_clicks != 0 and 'copy' in input_id:
        df = pd.read_clipboard(sep=',')
        return create_table(table_id, df)


# apply the layout to the app
app.layout = layout

if __name__ == '__main__':
    app.run_server(
        debug=app.settings['debug'],
        host=app.settings['host'],
        port=app.settings['port'],
    )