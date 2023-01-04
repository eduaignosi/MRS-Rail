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


def get_x_y(df):
    "Get x and y for plot function"
    x = df.index
    y = df[:]
    return x, y


def tidy_df_endoded_and_groupedby(df: pd.DataFrame, groupby_frequency: str) -> pd.DataFrame:
    """
        Create one hot enconding to facilitate agregation and return grouped by data frame
        by certain frequency (depending on the granularity of users need to generate the analysis)
    """
    # creating instance of one-hot-encoder
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    encoder_df = pd.DataFrame(
        encoder.fit_transform(df_ab[['Falha de rolamento']]))
    encoder_df.columns = encoder.get_feature_names_out(['Falha de rolamento'])
    # merge one-hot encoded columns back with original DataFrame
    final_df = df_ab.join(encoder_df)
    final_df.set_index('Data da Medição', inplace=True)

    # Groupby to to agregate data, Monthly frequency
    tidy_df = final_df.groupby(
        [pd.Grouper(freq=groupby_frequency), "Veículo", "Lateral do veículo", "Número do eixo do veículo"]).sum()
    # Changing the order of the multilevel index, making the type of fail being the first level
    tidy_df = tidy_df.swaplevel()
    tidy_df = tidy_df.swaplevel()

    return tidy_df


def plot_main_failures_per_vehicle_per_side_per_rodeiro(df_mult_index_sintax: pd.DataFrame, vehicle: str, side: str, rodeiro: str, range: str) -> None:
    """
        Plotting multiple trends in the same graph, main failures (monthly basis)
    """
    colors = ['rgb(37,255,81)', 'rgb(213,242,23)', 'rgb(255,146,50)',
              'rgb(255,50,50)']  # green, yellow, orange, red
    fig = go.Figure()
    x1, y1 = get_x_y(df_mult_index_sintax['Falha de rolamento_.'])
    x2, y2 = get_x_y(df_mult_index_sintax['Falha de rolamento_RS3'])
    x3, y3 = get_x_y(df_mult_index_sintax['Falha de rolamento_RS2'])
    x4, y4 = get_x_y(df_mult_index_sintax['Falha de rolamento_RS1'])
    fig.add_trace(go.Scatter(x=x1, y=y1,
                             mode='lines+markers',
                             name="Falha de rolamento '.' ", line=dict(color=colors[0])))
    fig.add_trace(go.Scatter(x=x2, y=y2,
                             mode='lines+markers',
                             name='Falha de rolamento RS3', line=dict(color=colors[1])))
    fig.add_trace(go.Scatter(x=x3, y=y3,
                             mode='lines+markers', name='Falha de rolamento RS2', line=dict(color=colors[2])))

    # Adding RS1 trace only for the graph where it occurs
    if (rodeiro == str(4)) & (vehicle == '734879'):
        fig.add_trace(go.Scatter(x=x4, y=y4,
                                 mode='markers', name='Falha de rolamento RS1',
                                 textposition='top left',
                                 textfont=dict(color='#233a77'),
                                 text="RS1", line=dict(color=colors[3])))

    fig.update_layout({"title": f"Total de Ocorrências {range} de Falhas Primárias no Rolamento no Veiculo {vehicle}, Lado {side}, Rodeiro {rodeiro}",
                       "xaxis": {"title": "Data"},
                       "yaxis": {"title": "Total de ocorrências"},
                       "showlegend": True},
                      xaxis_range=['2022-01-01', '2023-01-31'])
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        plot_bgcolor='white'
    )
    fig.show()


def plot_secondary_failures_per_vehicle_per_side_per_rodeiro(df_mult_index_sintax: pd.DataFrame, vehicle: str, side: str, rodeiro: str, range: str) -> None:
    """
        Plotting multiple trends in the same graph, secondary failures (monthly basis)
    """
    colors = ['rgb(37,255,81)', 'rgb(213,242,23)', 'rgb(255,146,50)',
              'rgb(255,50,50)']  # green, yellow, orange, red
    fig = go.Figure()
    x1, y1 = get_x_y(df_mult_index_sintax['Falha de rolamento_FBS(RS3)'])
    x2, y2 = get_x_y(df_mult_index_sintax['Falha de rolamento_FBS(RS2)'])
    x3, y3 = get_x_y(df_mult_index_sintax['Falha de rolamento_FBS(4)'])
    x4, y4 = get_x_y(df_mult_index_sintax['Falha de rolamento_RS1'])
    fig.add_trace(go.Scatter(x=x1, y=y1,
                             mode='lines+markers',
                             name="Falha de rolamento FBS(RS3)", line=dict(color=colors[0])))
    fig.add_trace(go.Scatter(x=x2, y=y2,
                             mode='lines+markers',
                             name='Falha de rolamento FBS(RS2)', line=dict(color=colors[1])))
    fig.add_trace(go.Scatter(x=x3, y=y3,
                             mode='lines+markers', name='Falha de rolamento FBS(4)', line=dict(color=colors[2])))
    # Adding RS1 trace only for the graph where it occurs
    if (rodeiro == str(4)) & (vehicle == '734879'):
        fig.add_trace(go.Scatter(x=x4, y=y4,
                                 mode='lines+markers', name='Falha de rolamento RS1',
                                 textposition='top left',
                                 textfont=dict(color='#233a77'),
                                 text="RS1", line=dict(color=colors[3])))
    fig.update_layout({"title": f"Total de Ocorrências {range} de Falhas Secundárias no Rolamento no Veiculo {vehicle}, Lado {side}, Rodeiro {rodeiro}",
                       "xaxis": {"title": "Data"},
                       "yaxis": {"title": "Total de ocorrências"},
                       "showlegend": True},
                      xaxis_range=['2022-01-01', '2023-01-31'])
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        plot_bgcolor='white'
    )
    fig.show()


# ---------------------------------------------------------------------------------
# %%
# Generate tidy datafram for plotting
groupby_frequency = 'M'
final_dff = tidy_df_endoded_and_groupedby(df_ab, groupby_frequency)

# %%
# Plot multiple graphics for vehicle 612934, all rodeiros, all sides
secondray_plot = True
if groupby_frequency == 'M':
    desired_frequency = 'Mensal'
else:
    desired_frequency = 'Diária'

for i in range(1, 4+1):
    plot_main_failures_per_vehicle_per_side_per_rodeiro(
        final_dff.loc[:, 612934, 'L', i], '612934', 'L', str(i), desired_frequency)
    plot_main_failures_per_vehicle_per_side_per_rodeiro(
        final_dff.loc[:, 612934, 'R', i], '612934', 'R', str(i), desired_frequency)
    if secondray_plot:
        plot_secondary_failures_per_vehicle_per_side_per_rodeiro(
            final_dff.loc[:, 612934, 'L', i], '612934', 'L', str(i), desired_frequency)
        plot_secondary_failures_per_vehicle_per_side_per_rodeiro(
            final_dff.loc[:, 612934, 'R', i], '612934', 'R', str(i), desired_frequency)
# ---------------------------------------------------------------------
# %%
# Plot multiple graphics for vehicle 734879, all rodeiros, all sides
secondray_plot = True
for i in range(1, 4+1):
    plot_main_failures_per_vehicle_per_side_per_rodeiro(
        final_dff.loc[:, 734879, 'L', i], '734879', 'L', str(i), desired_frequency)
    plot_main_failures_per_vehicle_per_side_per_rodeiro(
        final_dff.loc[:, 734879, 'R', i], '734879', 'R', str(i), desired_frequency)
    if secondray_plot:
        plot_secondary_failures_per_vehicle_per_side_per_rodeiro(
            final_dff.loc[:, 734879, 'L', i], '734879', 'L', str(i), desired_frequency)
        plot_secondary_failures_per_vehicle_per_side_per_rodeiro(
            final_dff.loc[:, 734879, 'R', i], '734879', 'R', str(i), desired_frequency)
# %%
# Insight, o rodeiro 4, tanto lado esquerdo e direito foi os que mais
# apresentou falha secundaria... tem que ver se o numero de primaria tb...
