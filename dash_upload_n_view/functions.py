import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_bootstrap_components as dbc

import pandas as pd

import io
import base64
import toml


def read_settings(path_or_filelike):
    try:
        with open(path_or_filelike) as f:
            toml_str = f.read()
    except TypeError:
        toml_str = path_or_filelike.read()
    return toml.loads(toml_str)


def parse_csv(filename, contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # check if user selected a .csv
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return df
        else:
            return "Wrong File"
    except Exception as e:
        print(e)
        return e


# read the style from the toml file
style = read_settings('./setting.toml')


def create_table(ID,
                 df,
                 title='',
                 row_deletable=False,
                 filter_action='none',
                 row_selectable=False,
                 all_rows_selected=False,
                 editable=False,
                 editable_columns=None,
                 page_size=250,
                 ):
    if editable_columns is None:
        editable_columns = []
    if all_rows_selected:
        length = len(df)
        selected_rows = []
        for x in range(length):
            selected_rows.append(x)
    else:
        selected_rows = []

    table = html.Div([
        html.H5(title),
        dash_table.DataTable(
            style_table=style['table_style'],
            style_cell=style['cell_style'],
            style_header=style['header_style'],
            id=ID,
            columns=[{"name": col_name, "id": col_name, "editable": col_name in editable_columns} for col_name in
                     df.columns],
            data=df.to_dict('records'),
            selected_rows=selected_rows,
            row_deletable=row_deletable,
            filter_action=filter_action,
            row_selectable=row_selectable,
            editable=editable,
            page_size=page_size,
        )
    ])
    return table


def create_upload(ID, multiple=False, title=''):
    return html.Div([
        html.H6(title),
        dcc.Upload(
            id=ID+'upload',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style=style['upload'],
            # Allow multiple files to be uploaded
            multiple=multiple
        ),
        dbc.Button("Copy from Clipboard", id=ID+"copy", n_clicks=0, color="primary", outline=True),
        html.Br(),
        html.Br(),
        html.Div(id=ID+'output'),
        html.Br(),
    ])
