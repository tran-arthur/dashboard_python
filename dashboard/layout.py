from data.get_data import get_df
from dashboard.callbacks import register_callbacks
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import numpy as np
import folium



# Import the dataframe from get_data
df_billionaires = get_df()
# print(len(df_billionaires))
# print(df_billionaires.describe())

#a subdataframe that will be display at the top of the site
df_simplified = df_billionaires.loc[:,["rank","finalWorth","personName","country","industries","gender"]]

# Create an histogram that represents the distribution of billionaire's worth
fig_histo = px.histogram(
    df_billionaires, 
    x="finalWorth", 
    color="gender",
    color_discrete_sequence=['#4169E1', 'pink'],
    nbins=35,
    log_y=True,
    labels={"finalWorth": "Fortune en milliards de $"},
    ).update_layout(# Changing the layout of the histogram
    title="Distribution de la richesse des milliardaires (logarithmique)", 
    xaxis_title="Fortune en milliards de $", 
    plot_bgcolor='white',
    yaxis_title="Compte",
    bargap=0.15,
)

# Create a pie chart that represents the proportion of men and women
# Replace all M and F in the column gender by "Homme" and "Femme"
df_billionaires['gender'] = df_billionaires['gender'].map({'M': 'Homme', 'F': 'Femme'})
fig_pie_gender = px.pie(
    df_billionaires,
    values=df_billionaires['gender'].value_counts().values,
    names=df_billionaires['gender'].value_counts().index,
    title="Diagramme représentant la répartition des sexes"
    )

#Create a pie chart that represents the proportion of selfmades
# Replace all True and False in the column selfmade by "selfmade" and "not selfmade"
df_billionaires['selfMade'] = df_billionaires['selfMade'].map({True: 'selfmade', False: 'not selfmade'})
fig_pie_selfmade = px.pie(
    df_billionaires,
    values=df_billionaires['selfMade'].value_counts().values,
    names=df_billionaires['selfMade'].value_counts().index,
    title="Diagramme représentant la répartition des milliardaires \"selfmade\" "
    )


#features related to the customisable histogramm
special_features = ["finalWorth","age","country",
                    "industries","gender","selfMade","total_tax_rate_country"]

# Transformation of the data for the map layout
# The map represents the number of billionaires per country (log)

# Count billionaires for each country
billionaires_country = df_billionaires["country"].value_counts()
billionaires_country = np.log10(billionaires_country) #transformation in logarithm to rescale

# Dataframe of number of billionaires by country
df_billionaires_country = pd.DataFrame(billionaires_country, columns=["country"])
df_billionaires_country = df_billionaires_country.rename(columns={"country":"count"})
df_billionaires_country = df_billionaires_country.rename_axis("country").reset_index()

# Import of the map's url
countries_url = (
    "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
)

# Creation of the map
map = folium.Map(location=(30,10), tiles='OpenStreetMap', zoom_start=2)

folium.Choropleth(
    geo_data=countries_url,
    data=df_billionaires_country,
    columns=["country", "count"],
    key_on="feature.properties.name",
    fill_color="YlOrBr"
).add_to(map)

map.save(outfile='map_number.html')

#Structure of the site
app_layout = html.Div([

    #Top of the site
    html.Header([
        html.H1("Données sur les milliardaires",className="title"),
        html.Img(src="assets/money_icon.png",className="title_logo"),
    ]),

    #Dataframe displayed on the site
    html.Div([
        dash_table.DataTable(data=df_simplified.to_dict('records'),style_as_list_view=True, page_size=10),
        ],className="df"
    ),
    
    #Map section
    html.H1("Nombre de milliardaires par pays en échelle logarithmique",className="title"),

    html.Div([
        html.Iframe(id="map1",srcDoc = open('map_number.html','r').read(),
                     width='75%',height='600',className="map_css")
        ],className="map_container"
    ),
    
    
    #Customisable histogramm section
    html.H1("Histogramme personalisable",style={"padding-top":"2.5%"}),
    #Selection bar of the x axis of the chart code inspired on https://dash.plotly.com/basic-callbacks
        html.Div([
            html.Div("Données à sélectionner: ",style={"margin":"0.4%"},className="selector_x_title"),
            dcc.Dropdown(
                special_features,
                'age',
                clearable=False,
                id='xaxis_column',
                style={"width": '50%'}
            ),
        ],className="selector_x",style={"display": 'flex',"flex-direction": "row","appearance": "none"}),
        
        html.Div([
            html.Div("Nombres de bins: ",style={"margin":"0.4%"},className="selector_x_title"),
            html.Div(dcc.Input(id='input_bin',value=30, type='number'),style={"margin":"0.5%"},className="bin_input"),
        ],style={"display": 'flex',"flex-direction": "row","appearance": "none"}),
    
    #graph that can be changed according to the selection of the user
    dcc.Graph(id="indicator_graphic",className="custom_histo"),

    # other graphs...
    html.H1("Autres graphiques..."),
    dcc.Graph(id="f1",figure=fig_histo),
    html.Div([
        dcc.Graph(id="f2",figure=fig_pie_gender,style={"width":"45%"}),
        dcc.Graph(id="f3",figure=fig_pie_selfmade,style={"width":"50%"})
    ],className="diagram_graphs",style={"display": 'flex',"flex-direction": "row"}),

    
])

register_callbacks(df_billionaires)
