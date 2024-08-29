import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash

def create_dash_app(file_path):
    # Initialize the DjangoDash app
    app = DjangoDash('MyDashApp')

    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Data processing
    vlrs_per_country = df['Country Name'].value_counts().sort_values(ascending=False)
    subs_per_country = df.groupby('Country Name')['Number of SUBS'].sum().sort_values(ascending=False)
    vlrs_per_operator = df['Operator'].value_counts().sort_values(ascending=False)
    subs_per_operator = df.groupby('Operator')['Number of SUBS'].sum().sort_values(ascending=False)

    # Define the layout of the app
    app.layout = html.Div([
        html.H1(
            "VLR and Subscribers Statistics Dashboard",
            style={
                'fontSize': '40px',
                'fontFamily': 'Arial',
                'fontWeight': 'bold',
                'marginBottom': '30px'
            }
        ),

        # Graph components

        dcc.Graph(id='vlrs-per-operator'),
        dcc.Graph(id='subs-per-operator'),
        dcc.Graph(id='vlrs-per-country'),
        dcc.Graph(id='subs-per-country'),
    ])

    # Define the callback to update graphs
    @app.callback(
        [Output('vlrs-per-operator', 'figure'),
         Output('subs-per-operator', 'figure'),
         Output('vlrs-per-country', 'figure'),
         Output('subs-per-country', 'figure')],
        [Input('vlrs-per-operator', 'id')]  # Use a placeholder input, as the graphs are static after loading
    )
    def update_graphs(_):
        # VLRs per Country (Pie Chart)
        fig_vlrs_country = px.pie(
            vlrs_per_country,
            names=vlrs_per_country.index,
            values=vlrs_per_country.values,
            title='VLRs per Country',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig_vlrs_country.update_traces(textposition='inside')
        fig_vlrs_country.update_layout(
            uniformtext_minsize=12,
            uniformtext_mode='hide',
            title={
                'text': 'VLRs per Country',
                'font': {'size': 30},
                'x': 0.435,
                'xanchor': 'center'
            },
            height=600,
        )

        # Subscribers per Country (Pie Chart)
        fig_subs_country = px.pie(
            subs_per_country,
            names=subs_per_country.index,
            values=subs_per_country.values,
            title='Subscribers per Country',
            color_discrete_sequence=px.colors.sequential.PuBu_r
        )
        fig_subs_country.update_traces(textposition='inside')
        fig_subs_country.update_layout(
            uniformtext_minsize=12,
            uniformtext_mode='hide',
            title={
                'text': 'Subscribers per Country',
                'font': {'size': 30},
                'x': 0.435,
                'xanchor': 'center'
            },
            height=600,
        )

        # VLRs per Operator (Horizontal Bar Chart)
        fig_vlrs_operator = go.Figure(go.Bar(
            x=vlrs_per_operator.tolist(),
            y=vlrs_per_operator.index.tolist(),
            orientation='h',
            marker=dict(color='blue', line=dict(color='black', width=1))
        ))
        fig_vlrs_operator.update_layout(
            title={'text': 'Repartition of VLRs per Operator', 'font': {'size': 30}, 'x': 0.5, 'xanchor': 'center'},
            xaxis_title={'text': 'Number of VLRs', 'font': {'size': 18}},
            yaxis_title={'text': 'Operator', 'font': {'size': 18}},
            yaxis=dict(categoryorder='total ascending'),
            font=dict(size=14),
            height=800
        )

        # Subscribers per Operator (Horizontal Bar Chart)
        fig_subs_operator = go.Figure(go.Bar(
            x=subs_per_operator.tolist(),
            y=subs_per_operator.index.tolist(),
            orientation='h',
            marker=dict(color='blue', line=dict(color='black', width=1))
        ))
        fig_subs_operator.update_layout(
            title={'text': 'Repartition of Subscribers per Operator', 'font': {'size': 30}, 'x': 0.5, 'xanchor': 'center'},
            xaxis_title={'text': 'Number of Subscribers', 'font': {'size': 18}},
            yaxis_title={'text': 'Operator', 'font': {'size': 18}},
            yaxis=dict(categoryorder='total ascending'),
            font=dict(size=14),
            height=800
        )

        return fig_vlrs_country, fig_subs_country, fig_vlrs_operator, fig_subs_operator
