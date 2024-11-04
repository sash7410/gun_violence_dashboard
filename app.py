from dash import Dash
from src.layouts import create_layout
from src.callbacks import register_callbacks

# Initialize the Dash app
app = Dash(__name__)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Gun Violence Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            .stats-card {
                padding: 20px;
                border-radius: 10px;
                background-color: white;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            body {
                background-color: #f5f6fa;
                margin: 20px;
                font-family: Arial, sans-serif;
            }
            .map-controls {
                margin-left: 15px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Set app layout
app.layout = create_layout(app)

# Register callbacks
register_callbacks(app)

# Expose the underlying Flask server for deployment
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
