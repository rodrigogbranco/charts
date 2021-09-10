# helper.py

import numpy as np
import plotly.graph_objects as go
from shapely.geometry import Point, LineString
import geopandas as gpd
import shapely.geometry
import plotly.express as px

marker_colors = ['#FF851B', '#FF4136', '#3D9970']
marker_patterns_shape= ['.', 'x', '+']

evs_name = {'vehev1' : 'EV1', 'vehev2' : 'EV2', 'vehev3' : 'EV3', 'boundary' : 'Experiment Area'}
algs_name = {
        'kapusta2': 'Kapusta et al (2017)',
        'allgreen': 'Hyphotetical all-green',
        'tpn3' : 'TPN',
        'no-preemption' : 'No Preemption'
    }

algs_order = ['kapusta2', 'tpn3', 'allgreen', 'no-preemption']

scenarios = {
    'turin' : 'Turin TuSTScenario',
    'cologne' : 'TAPAS Cologne',
    'metro-od-2017' : 'Metro OD 2017 Survey (Expanded Center of São Paulo)'
}

y_axis_labels = {
    'imp' : 'Time-Loss Improvement (times)',
    'perc' : 'Time-Loss Improvement (%)',
    'tl' : 'Time-Loss (s)',
    'rt' : 'Runtime (s)'
}

title_label = {
    'route' : 'Routes - {}',
    'tl-imp' : 'Time-Loss Improvement - {}',
    'tl-perc' : 'Time-Loss Improvement - {}',
    'tl-no-preemption' : 'Time-Loss - No Preemption - {}',
    'tl-algs' : 'Time-Loss - Solutions - {}',
    'runtime' : 'Runtime - Solutions - {}'
}

def make_boxplot_grouped(df,metric,title_label):
    evs = sorted(df['ev'].unique().tolist())
    algs = df['alg'].unique().tolist()

    df = df[df[metric].notnull()]

    fig = go.Figure()

    for index,alg in enumerate([alg for alg in algs_order if alg in algs]):
        complete_values = []
        xlabels = []
        for ev in evs:
            values = df[(df['alg'] == alg) & (df['ev'] == ev)][metric].tolist()
            xlabels += [evs_name[ev]]*len(values)
            complete_values += values

        fig.add_trace(go.Box(
            y=complete_values,
            x=xlabels,
            name=algs_name[alg],
            marker_color=marker_colors[index]
        ))

    fig.update_layout(
        yaxis_title=y_axis_labels[metric],
        title=title_label,
        boxmode='group'
    )
    fig.show() 

def make_boxplot(df,metric,title_label):
    evs = sorted(df['ev'].unique().tolist())

    fig = go.Figure()

    df = df[df[metric].notnull()]

    for ev in evs:
        fig.add_trace(go.Box(y=df[(df['alg'] == 'no-preemption') & (df['ev'] == ev)][metric].tolist(), name=evs_name[ev]))

    fig.update_layout(
        yaxis_title=y_axis_labels[metric],
        title=title_label
    )        

    fig.show()  

def csv_to_geo(df):
    geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
    geo_df = gpd.GeoDataFrame(df, geometry=geometry)

    geo_df2 = geo_df.groupby(['scenario', 'ev'])['geometry'].apply(lambda x: LineString(x.tolist()))
    return gpd.GeoDataFrame(geo_df2, geometry='geometry')  

def make_map(df,zoom,title):
    geo_df = csv_to_geo(df)
    lats = []
    lons = []
    names = []
    colors = []

    for index, row in geo_df.iterrows():
        feature = row['geometry']
        name = evs_name[index[1]]

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

    fig = px.line_mapbox(lat=lats, lon=lons, hover_name=names, mapbox_style="open-street-map", zoom=zoom, color=colors, title=title)
    fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
    fig.show()        

def make_title(title,key):
    return title_label[title].format(scenarios[key])