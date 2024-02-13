from dash import Dash
from dashboard.layout import app_layout

#create the app
app = Dash(__name__)
app.layout = app_layout
