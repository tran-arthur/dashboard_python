from dash import callback, Input, Output
import plotly.express as px

#function that uses callback to update the customisable histogram
def register_callbacks(df_billionaires):

    #all callback needen
    @callback(
        #change the graph
        Output('indicator_graphic', 'figure'),
        #change the data to plot
        Input('xaxis_column', 'value'),
        #select the bin's number
        Input("input_bin","value")
    )

    #function that changes the graph based on the input 
    def update_graph(xaxis_column_name,bin):

        fig = px.histogram(df_billionaires,
                           x=xaxis_column_name,nbins=bin).update_layout(title="Histogramme de "+str(xaxis_column_name) + " avec "+ str(bin)+ " bins",
                            plot_bgcolor='white',bargap=0.15,yaxis_title="Nombre").update_xaxes(categoryorder='total descending')
        
        return fig