# helper.py

import locale

locale.setlocale(locale.LC_ALL, "pt_BR.utf8")
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from shapely.geometry import Point, LineString
import geopandas as gpd
import shapely.geometry
import plotly.express as px
import plotly.io as pio

evs_name = {
    "en": {
        "vehev1": "EV1",
        "vehev2": "EV2",
        "vehev3": "EV3",
        "vehev4": "EV1-Synthetic",
        "vehev5": "EV2-Synthetic",
        "vehev6": "EV3-Synthetic",
        "vehev7": "EV4",
        "veh11651": "EV",
        "veh4856": "EV",
        "boundary": "Experiment Area",
        "expcenter": "Expanded Center",
    },
    "br": {
        "vehev1": "VE1",
        "vehev2": "VE2",
        "vehev3": "VE3",
        "vehev4": "VE1-Sintético",
        "vehev5": "VE2-Sintético",
        "vehev6": "VE3-Sintético",
        "vehev7": "VE4",
        "veh11651": "VE",
        "veh4856": "VE",
        "boundary": "Área do Experimento",
        "expcenter": "Centro Expandido",
    },
}
algs_name = {
    "en": {
        "kapusta2": "Queue based",
        "kapustaimp": "Queue based (Imp.)",
        "allgreen": "All Green",
        "tpn4": "TPN",
        "tpn6": "TPN6",
        "tpnx": "TPN",
        "fuzzy": "Fuzzy",
        "rfid": "RFId",
        "no-preemption": "No Preemption",
    },
    "br": {
        "kapusta2": "Filas",
        "kapustaimp": "Choque de Onda",
        "allgreen": "Tudo Verde",
        "tpn4": "TPN",
        "tpn6": "TPN6",
        "tpnx": "Choque de Onda + TPN*",
        "fuzzy": "Fuzzy",
        "rfid": "RFID",
        "no-preemption": "Sem Preempção",
    },
}

algs_order = [
    "rfid",
    "fuzzy",
    "kapusta2",
    "kapustaimp",
    "tpn4",
    "tpn6",
    "tpnx",
    "allgreen",
    "no-preemption",
]

scenarios = {
    "en": {
        "turin": "Turin SUMO Traffic (TuST) Scenario",
        "cologne": "TAPAS Cologne",
        "metro-od-2017": "Metro OD 2017 (Exp. Center of SP)",
        "metro-od-2017-zones": "Zones - Metro OD 2017",
        "synth-sp": "Synthetic SP - First Experiment",
        "synth-ny": "Synthetic NY - First Experiment",
        "synth-sp-new": "Synthetic SP - Second Experiment",
        "synth-ny-new": "Synthetic NY - Second Experiment",
        "oneintersection": "One Intersection",
        "turinkap": "Turin",
        "colognekap": "Cologne",
        "sumohighteleporttime": "High Teleport Time",
    },
    "br": {
        "turin": "Turim",
        "cologne": "Colônia",
        "metro-od-2017": "Centro Expandido - Metro OD SP 2017",
        "metro-od-2017-zones": "Zones - Metro OD 2017",
        "synth-sp": "São Paulo - Sintético",
        "synth-ny": "Nova York - Sintético",
        "synth-sp-new": "Synthetic SP - Second Experiment",
        "synth-ny-new": "Synthetic NY - Second Experiment",
        "oneintersection": "Uma Interseção",
        "turinkap": "Turim",
        "colognekap": "Colônia",
        "sumohighteleporttime": "Alto Tempo de Teletransporte",
    },
}

y_axis_labels = {
    "en": {
        "imp": "Time-Loss Improvement (times)",
        "perc": "Time-Loss Improvement (%)",
        "tl": "Time-Loss (s)",
        "rt": "Runtime (s)",
        "tl-ttt": "Time-Loss/Actual Travel Time (%)",
        "preemptime": "Mean Preemption Time (s)",
        "n_teleported": "Teleported Vehicles",
        "avg_trip_speed_perc": "Average Trip Speed (%)",
        "avg_trip_timeloss_perc": "Average Timeloss (%)",
        "teleported_perc": "Teleported Vehicles (%)",
    },
    "br": {
        "imp": "Melhoria do Tempo Perdido (vezes)",
        "perc": "Melhoria do Tempo Perdido (%)",
        "tl": "Tempo Perdido (s)",
        "rt": "Tempo de Execução (s)",
        "tl-ttt": "Tempo Perdido/Tempo Total de Viagem (%)",
        "preemptime": "Tempo de Preempção Médio (s)",
        "n_teleported": "Veículos Teletransportados",
        "avg_trip_speed_perc": "Velocidade Média (%)",
        "avg_trip_timeloss_perc": "Tempo Perdido Médio (%)",
        "teleported_perc": "Veículos Teletransportados (%)",
    },
}

title_label = {
    "en": {
        "route": "Routes - {}",
        "tl-imp": "Time-Loss Improvement - {}",
        "tl-perc": "Time-Loss Improvement - {}",
        "tl-no-preemption": "Time-Loss - No Preemption - {}",
        "tl-algs": "Time-Loss - Solutions - {}",
        "runtime": "Runtime - Solutions - {}",
        "tl-ttt": "Timeloss over Total Travel Time - {}",
        "preemptime": "Mean Preemption Time - {}",
        "n_teleported": "Number of teleported vehicles - {}",
        "avg_trip_speed_perc": "Average Trip Speed - All Vehicles - {}",
        "avg_trip_timeloss_perc": "Average Timeloss - All Vehicles - {}",
        "teleported_perc": "Teleported Vehicles - {}",
    },
    "br": {
        "route": "Rotas - Cenário {}",
        "tl-imp": "Melhoria do Tempo Perdido - Cenário {}",
        "tl-perc": "Melhoria do Tempo Perdido - Cenário {}",
        "tl-no-preemption": "Tempo Perdido - Sem Preempção - Cenário {}",
        "tl-algs": "Tempo Perdido - Soluções - Cenário {}",
        "runtime": "Tempo de Execução - Soluções - Cenário {}",
        "tl-ttt": "Tempo Perdido sobre Tempo Total de Viagem - Cenário {}",
        "preemptime": "Tempo de Preempção Médio - Cenário {}",
        "n_teleported": "N° de veículos teletransportados - Cenário {}",
        "avg_trip_speed_perc": "Velocidade Média das Viagens - Todos os veículos - Cenário {}",
        "avg_trip_timeloss_perc": "Tempo Perdido Médio - Todos os veículos - Cenário {}",
        "teleported_perc": "Veículos Teletransportados - {}",
    },
}


def get_quartiles_data(values_list, label):
    df = pd.DataFrame(sorted(values_list))
    mediana = df[0].median()
    q1 = df[0].quantile(0.25, interpolation="midpoint")
    q3 = df[0].quantile(0.75, interpolation="midpoint")

    iqr = q3 - q1
    lower_fence = q1 - (1.5 * iqr)
    upper_fence = q3 + (1.5 * iqr)

    min_value = df[0].iloc[0]
    max_value = df[0].iloc[-1]

    for i in df[0]:
        if i >= lower_fence:
            lower_fence = i
            break

    for i in df[0].loc[::-1]:
        if i <= upper_fence:
            upper_fence = i
            break

    min_value = (
        locale.format_string("%.2f", min_value) if min_value < lower_fence else " - "
    )
    max_value = (
        locale.format_string("%.2f", max_value) if max_value > upper_fence else " - "
    )
    print(
        locale.format_string(
            "%s & %s & %.2f & %.2f & %.2f & %.2f & %.2f & %s \\\\",
            (label, min_value, lower_fence, q1, mediana, q3, upper_fence, max_value),
            grouping=True,
        )
    )


def make_boxplot_grouped(
    df,
    metric,
    title_label,
    figname,
    width=600,
    height=480,
    lang="en",
    output_dir="figs",
):
    evs = sorted(df["ev"].unique().tolist())
    algs = df["alg"].unique().tolist()

    df = df[df[metric].notnull()]

    fig = go.Figure()

    for alg in [alg for alg in algs_order if alg in algs]:
        complete_values = []
        xlabels = []
        print("{}: ".format(alg))
        for ev in evs:
            tmp_df = df[(df["alg"] == alg) & (df["ev"] == ev)][metric]
            values = tmp_df.nlargest(tmp_df.size - 1).tolist()
            xlabels += [evs_name[lang][ev]] * len(values)
            complete_values += values
            get_quartiles_data(values, evs_name[lang][ev])
        print()

        fig.add_trace(go.Box(y=complete_values, x=xlabels, name=algs_name[lang][alg]))

    fig.update_layout(
        yaxis_title=y_axis_labels[lang][metric],
        title=title_label,
        boxmode="group",
        font=dict(size=14),
    )
    fig.show()
    pio.write_image(
        fig,
        "{}/{}.pdf".format(output_dir, figname),
        format="pdf",
        width=width,
        height=height,
    )
    pio.write_image(
        fig,
        "{}/{}.png".format(output_dir, figname),
        format="png",
        width=width,
        height=height,
    )


def make_boxplot(
    df,
    metric,
    title_label,
    figname,
    width=600,
    height=480,
    lang="en",
    output_dir="figs",
):
    evs = sorted(df["ev"].unique().tolist())

    fig = go.Figure()

    df = df[df[metric].notnull()]

    for ev in evs:
        tmp_df = df[(df["alg"] == "no-preemption") & (df["ev"] == ev)][metric]
        dataframe = tmp_df.nlargest(tmp_df.size - 1).tolist()
        fig.add_trace(go.Box(y=dataframe, name=evs_name[lang][ev]))
        get_quartiles_data(dataframe, evs_name[lang][ev])

    fig.update_layout(
        yaxis_title=y_axis_labels[lang][metric], title=title_label, font=dict(size=14)
    )

    fig.show()
    pio.write_image(
        fig,
        "{}/{}.pdf".format(output_dir, figname),
        format="pdf",
        width=width,
        height=height,
    )
    pio.write_image(
        fig,
        "{}/{}.png".format(output_dir, figname),
        format="png",
        width=width,
        height=height,
    )


def csv_to_geo(df):
    geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
    geo_df = gpd.GeoDataFrame(df, geometry=geometry)

    geo_df2 = geo_df.groupby(["scenario", "ev"])["geometry"].apply(
        lambda x: LineString(x.tolist())
    )
    return gpd.GeoDataFrame(geo_df2, geometry="geometry")


def make_map(
    df, zoom, title, figname, width=600, height=480, lang="en", output_dir="figs"
):
    geo_df = csv_to_geo(df)
    lats = []
    lons = []
    names = []
    colors = []

    for index, row in geo_df.iterrows():
        feature = row["geometry"]

        try:
            name = int(index[1])
        except ValueError:
            name = evs_name[lang][index[1]]

        if isinstance(feature, shapely.geometry.linestring.LineString):
            linestrings = [feature]
        elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
            linestrings = feature.geoms
        else:
            continue
        for linestring in linestrings:
            x, y = linestring.xy
            lats = np.append(lats, y)
            lons = np.append(lons, x)
            names = np.append(names, [name] * len(y))
            lats = np.append(lats, None)
            lons = np.append(lons, None)
            names = np.append(names, None)
            colors = np.append(colors, [name] * (len(y) + 1))

    lat_extreme = df[df["ev"] == "boundary"]["lat"].unique()
    lon_extreme = df[df["ev"] == "boundary"]["lon"].unique()

    fig = px.line_mapbox(
        lat=lats,
        lon=lons,
        hover_name=names,
        mapbox_style="open-street-map",
        zoom=zoom,
        color=colors,
        title=title,
        center={"lat": np.mean(lat_extreme), "lon": np.mean(lon_extreme)},
    )
    fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0}, font=dict(size=14))
    fig.show()
    pio.write_image(
        fig,
        "{}/{}.pdf".format(output_dir, figname),
        format="pdf",
        width=width,
        height=height,
    )
    pio.write_image(
        fig,
        "{}/{}.png".format(output_dir, figname),
        format="png",
        width=width,
        height=height,
    )


def make_title(title, key, lang="en"):
    return title_label[lang][title].format(scenarios[lang][key])
