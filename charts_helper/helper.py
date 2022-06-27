# helper.py

import numpy as np
import plotly.graph_objects as go
from shapely.geometry import Point, LineString
import geopandas as gpd
import shapely.geometry
import plotly.express as px
import plotly.io as pio

evs_name = {
    'en': {'vehev1': 'EV1', 'vehev2': 'EV2', 'vehev3': 'EV3',
           'vehev4': 'EV1-Synthetic', 'vehev5': 'EV2-Synthetic', 'vehev6': 'EV3-Synthetic',
           'vehev7': 'EV4',
           'veh11651': 'EV',
           'veh4856': 'EV',
           'boundary': 'Experiment Area', 'expcenter': 'Expanded Center'},
    'br': {'vehev1': 'EV1', 'vehev2': 'EV2', 'vehev3': 'EV3',
           'vehev4': 'EV1-Sintético', 'vehev5': 'EV2-Sintético', 'vehev6': 'EV3-Sintético',
           'vehev7': 'EV4',
           'veh11651': 'EV',
           'veh4856': 'EV',
           'boundary': 'Área do Experimento', 'expcenter': 'Centro Expandido'}}
algs_name = {
    'en': {
        'kapusta2': 'Queue based',
        'kapustaimp': 'Queue based (Improved)',
        'allgreen': 'All Green',
        'tpn4': 'TPN',
        'fuzzy': 'Fuzzy',
        'rfid': 'RFId',
        'no-preemption': 'No Preemption', },
    'br': {
        'kapusta2': '[Kapusta et al., 2017]',
        'kapustaimp': 'Algoritmo proposto',
        'allgreen': 'Tudo Verde',
        'tpn4': 'TPN',
        'fuzzy': 'Fuzzy',
        'rfid': 'RFId',
        'no-preemption': 'Sem Preempção', }
}

algs_order = ['rfid', 'fuzzy', 'kapusta2', 'kapustaimp',
              'tpn4', 'allgreen', 'no-preemption']

scenarios = {'en': {
    'turin': 'Turin SUMO Traffic (TuST) Scenario',
    'cologne': 'TAPAS Cologne',
    'metro-od-2017': 'Metro OD 2017 (Exp. Center of SP)',
    'metro-od-2017-zones': 'Zones - Metro OD 2017',
    'synth-sp': 'Synthetic SP - First Experiment',
    'synth-ny': 'Synthetic NY - First Experiment',
    'synth-sp-new': 'Synthetic SP - Second Experiment',
    'synth-ny-new': 'Synthetic NY - Second Experiment',
    'oneintersection': 'One Intersection',
    'turinkap': 'Turin (Kapusta)',
    'colognekap': 'Cologne (Kapusta)'},
    'br': {
    'turin': 'Turin SUMO Traffic (TuST) Scenario',
    'cologne': 'TAPAS Cologne',
    'metro-od-2017': 'Metro OD 2017 (Exp. Center of SP)',
    'metro-od-2017-zones': 'Zones - Metro OD 2017',
    'synth-sp': 'Synthetic SP - First Experiment',
    'synth-ny': 'Synthetic NY - First Experiment',
    'synth-sp-new': 'Synthetic SP - Second Experiment',
    'synth-ny-new': 'Synthetic NY - Second Experiment',
    'oneintersection': 'Uma Intersecção',
    'turinkap': 'Turim',
    'colognekap': 'Colônia'}

}

y_axis_labels = {'en': {
    'imp': 'Time-Loss Improvement (times)',
    'perc': 'Time-Loss Improvement (%)',
    'tl': 'Time-Loss (s)',
    'rt': 'Runtime (s)',
    'tl-ttt': 'Time-Loss/Actual Travel Time (%)',
    'preemptime': 'Mean Preemption Time (s)'},
    'br': {
    'imp': 'Melhoria do Tempo Perdido (vezes)',
    'perc': 'Melhoria do Tempo Perdido (%)',
    'tl': 'Tempo Perdido (s)',
    'rt': 'Tempo de Execução (s)',
    'tl-ttt': 'Tempo Perdido/Tempo Total de Viagem (%)',
    'preemptime': 'Tempo de Preempção Médio (s)'}
}

title_label = {'en': {
    'route': 'Routes - {}',
    'tl-imp': 'Time-Loss Improvement - {}',
    'tl-perc': 'Time-Loss Improvement - {}',
    'tl-no-preemption': 'Time-Loss - No Preemption - {}',
    'tl-algs': 'Time-Loss - Solutions - {}',
    'runtime': 'Runtime - Solutions - {}',
    'tl-ttt': 'Timeloss over Total Travel Time - {}',
    'preemptime': 'Mean Preemption Time'},
    'br': {
    'route': 'Rotas - Cenário {}',
    'tl-imp': 'Melhoria do Tempo Perdido - Cenário {}',
    'tl-perc': 'Melhoria do Tempo Perdido - Cenário {}',
    'tl-no-preemption': 'Tempo Perdido - Sem Preempção - Cenário {}',
    'tl-algs': 'Tempo Perdido - Soluções - Cenário {}',
    'runtime': 'Tempo de Execução - Soluções - Cenário {}',
    'tl-ttt': 'Tempo Perdido sobre Tempo Total de Viagem - Cenário {}',
    'preemptime': 'Tempo de Preempção Médio - Cenário {}'}
}


def make_boxplot_grouped(df, metric, title_label, figname, width=600, height=480, lang='en'):
    evs = sorted(df['ev'].unique().tolist())
    algs = df['alg'].unique().tolist()

    df = df[df[metric].notnull()]

    fig = go.Figure()

    for alg in [alg for alg in algs_order if alg in algs]:
        complete_values = []
        xlabels = []
        for ev in evs:
            tmp_df = df[(df['alg'] == alg) & (df['ev'] == ev)][metric]
            values = tmp_df.nlargest(tmp_df.size-1).tolist()
            xlabels += [evs_name[lang][ev]]*len(values)
            complete_values += values

        fig.add_trace(go.Box(
            y=complete_values,
            x=xlabels,
            name=algs_name[lang][alg]
        ))

    fig.update_layout(
        yaxis_title=y_axis_labels[lang][metric],
        title=title_label,
        boxmode='group',
        font=dict(
            size=14
        )
    )
    fig.show()
    pio.write_image(fig, 'figs/{}.pdf'.format(figname),
                    format='pdf', width=600, height=480)


def make_boxplot(df, metric, title_label, figname, width=600, height=480, lang='en'):
    evs = sorted(df['ev'].unique().tolist())

    fig = go.Figure()

    df = df[df[metric].notnull()]

    for ev in evs:
        tmp_df = df[(df['alg'] == 'no-preemption') & (df['ev'] == ev)][metric]
        fig.add_trace(go.Box(y=tmp_df.nlargest(
            tmp_df.size-1).tolist(), name=evs_name[lang][ev]))

    fig.update_layout(
        yaxis_title=y_axis_labels[lang][metric],
        title=title_label,
        font=dict(
            size=14
        )
    )

    fig.show()
    pio.write_image(fig, 'figs/{}.pdf'.format(figname),
                    format='pdf', width=600, height=480)


def csv_to_geo(df):
    geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
    geo_df = gpd.GeoDataFrame(df, geometry=geometry)

    geo_df2 = geo_df.groupby(['scenario', 'ev'])['geometry'].apply(
        lambda x: LineString(x.tolist()))
    return gpd.GeoDataFrame(geo_df2, geometry='geometry')


def make_map(df, zoom, title, figname, width=600, height=480, lang='en'):
    geo_df = csv_to_geo(df)
    lats = []
    lons = []
    names = []
    colors = []

    for index, row in geo_df.iterrows():
        feature = row['geometry']

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
            names = np.append(names, [name]*len(y))
            lats = np.append(lats, None)
            lons = np.append(lons, None)
            names = np.append(names, None)
            colors = np.append(colors, [name]*(len(y)+1))

    lat_extreme = df[df['ev'] == 'boundary']['lat'].unique()
    lon_extreme = df[df['ev'] == 'boundary']['lon'].unique()

    fig = px.line_mapbox(lat=lats, lon=lons, hover_name=names, mapbox_style="open-street-map", zoom=zoom,
                         color=colors, title=title, center={'lat': np.mean(lat_extreme), 'lon': np.mean(lon_extreme)})
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        font=dict(
            size=14
        )
    )
    fig.show()
    pio.write_image(fig, 'figs/{}.pdf'.format(figname),
                    format='pdf', width=width, height=height)


def make_title(title, key, lang='en'):
    return title_label[lang][title].format(scenarios[lang][key])
