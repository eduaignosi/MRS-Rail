# Code created to analyze railbam data, considering all failures but for especific vehicules
# Plot graphs for the failures on monthly and daily basis

# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from sklearn.preprocessing import OneHotEncoder
import datetime

# %%
df_ab = pd.read_csv("Anomaly_bam.csv", sep=";", decimal=",",
                    parse_dates=['Data da Medição'])
df_ahb = pd.read_csv("Anomaly_hotbox.csv", sep=";",
                     decimal=",", parse_dates=['Data da Medição'])

df_ab["month"] = df_ab["Data da Medição"].dt.month
# ------------------------------------------------------------------------------
# %%
# Defining functions


def plot_graph(df):
    "Plot failure versus time graphic"
    fig = go.Figure(data=go.Line(x=df.index,
                                 y=df[:],
                                 marker_color='black', text="Quantidade de ocorrências"))
    fig.update_layout({"title": "Total de Ocorrências diárias de Falha no Rolamento tipo '.' ",
                       "xaxis": {"title": "Data"},
                       "yaxis": {"title": "Total de ocorrências por dia"},
                       "showlegend": False},
                      xaxis_range=['2022-01-01', '2023-01-31'])
    fig.show()


def get_x_y(df):
    "Get x and y for plot function"
    x = df.index
    y = df[:]
    return x, y


def plot_main_failures_per_vehicle_per_side_per_rodeiro(df_mult_index_sintax: pd.DataFrame, vehicle: str, side: str, rodeiro: str, range: str) -> None:
    # Plotting multiple trends in the same graph, main failures (monthly basis)
    fig = go.Figure()
    x1, y1 = get_x_y(df_mult_index_sintax['Falha de rolamento_.'])
    x2, y2 = get_x_y(df_mult_index_sintax['Falha de rolamento_RS3'])
    x3, y3 = get_x_y(df_mult_index_sintax['Falha de rolamento_RS2'])
    x4, y4 = get_x_y(df_mult_index_sintax['Falha de rolamento_RS1'])
    fig.add_trace(go.Scatter(x=x1, y=y1,
                             mode='lines+markers',
                             name="Falha de rolamento '.' "))
    fig.add_trace(go.Scatter(x=x2, y=y2,
                             mode='lines+markers',
                             name='Falha de rolamento RS3'))
    fig.add_trace(go.Scatter(x=x3, y=y3,
                             mode='lines+markers', name='Falha de rolamento RS2'))
    fig.add_trace(go.Scatter(x=x4, y=y4,
                             mode='lines+markers+text', name='Falha de rolamento RS1',
                             textposition='top left',
                             textfont=dict(color='#233a77'),
                             text="RS1"))
    vehi = 'xxx'
    fig.update_layout({"title": f"Total de Ocorrências {range} de Falhas Primárias no Rolamento no Veiculo {vehicle}, Lado {side}, Rodeiro {rodeiro}",
                       "xaxis": {"title": "Data"},
                       "yaxis": {"title": "Total de ocorrências"},
                       "showlegend": True},
                      xaxis_range=['2022-01-01', '2023-01-31'])
    fig.show()


def plot_secondary_failures_per_vehicle_per_side_per_rodeiro(df_mult_index_sintax: pd.DataFrame, vehicle: str, side: str, rodeiro: str, range: str) -> None:
    # Plotting multiple trends in the same graph,  secondary failures (monthly basis)
    fig = go.Figure()
    x1, y1 = get_x_y(df_mult_index_sintax['Falha de rolamento_FBS(RS3)'])
    x2, y2 = get_x_y(df_mult_index_sintax['Falha de rolamento_FBS(RS2)'])
    x3, y3 = get_x_y(df_mult_index_sintax['Falha de rolamento_FBS(4)'])
    x4, y4 = get_x_y(df_mult_index_sintax['Falha de rolamento_RS1'])
    fig.add_trace(go.Scatter(x=x1, y=y1,
                             mode='lines+markers',
                             name="Falha de rolamento FBS(RS3) "))
    fig.add_trace(go.Scatter(x=x2, y=y2,
                             mode='lines+markers',
                             name='Falha de rolamento FBS(RS2)'))
    fig.add_trace(go.Scatter(x=x3, y=y3,
                             mode='lines+markers', name='Falha de rolamento FBS(4)'))
    fig.add_trace(go.Scatter(x=x4, y=y4,
                             mode='lines+markers+text', name='Falha de rolamento RS1',
                             textposition='top left',
                             textfont=dict(color='#233a77'),
                             text="RS1"))
    fig.update_layout({"title": f"Total de Ocorrências {range} de Falhas Secundárias no Rolamento no Veiculo {vehicle}, Lado {side}, Rodeiro {rodeiro}",
                       "xaxis": {"title": "Data"},
                       "yaxis": {"title": "Total de ocorrências"},
                       "showlegend": True},
                      xaxis_range=['2022-01-01', '2023-01-31'])
    fig.show()

# ---------------------------------------------------------------------------------
# %%
# One hot encoding of the type of failures - Monthly basis


# creating instance of one-hot-encoder
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
encoder_df = pd.DataFrame(encoder.fit_transform(df_ab[['Falha de rolamento']]))
encoder_df.columns = encoder.get_feature_names_out(['Falha de rolamento'])
# merge one-hot encoded columns back with original DataFrame
final_df = df_ab.join(encoder_df)
final_df.set_index('Data da Medição', inplace=True)

# Groupby to to agregate data, Monthly frequency
final_dff = final_df.groupby(
    [pd.Grouper(freq='M'), "Veículo", "Lateral do veículo", "Número do eixo do veículo"]).sum()
# Changing the order of the multilevel index, making the type of fail being the first level
final_dff = final_dff.swaplevel()
final_dff = final_dff.swaplevel()
# ----------------------------

# %%
plot_main_failures_per_vehicle_per_side_per_rodeiro(
    final_dff.loc[:, 612934, 'L', 1], '612934', 'L', '1', 'Mensal')

plot_secondary_failures_per_vehicle_per_side_per_rodeiro(
    final_dff.loc[:, 612934, 'L', 1], '612934', 'L', '1', 'Mensal')

plot_main_failures_per_vehicle_per_side_per_rodeiro(
    final_dff.loc[:, 612934, 'L', 2], '612934', 'L', '2', 'Mensal')

plot_secondary_failures_per_vehicle_per_side_per_rodeiro(
    final_dff.loc[:, 612934, 'L', 2], '612934', 'L', '2', 'Mensal')

plot_main_failures_per_vehicle_per_side_per_rodeiro(
    final_dff.loc[:, 612934, 'L', 3], '612934', 'L', '3', 'Mensal')

plot_secondary_failures_per_vehicle_per_side_per_rodeiro(
    final_dff.loc[:, 612934, 'L', 3], '612934', 'L', '3', 'Mensal')

plot_main_failures_per_vehicle_per_side_per_rodeiro(
    final_dff.loc[:, 612934, 'L', 4], '612934', 'L', '4', 'Mensal')

plot_secondary_failures_per_vehicle_per_side_per_rodeiro(
    final_dff.loc[:, 612934, 'L', 4], '612934', 'L', '4', 'Mensal')
# %%
