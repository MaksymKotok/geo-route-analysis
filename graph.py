import folium
from folium.plugins import HeatMap
import pandas as pd
import osmnx as ox
import networkx as nx
import webbrowser
import os
from random import randint

ox.settings.use_cache=True
ox.settings.log_console=True

COLORS = [
    'red',
    'blue',
    'gray',
    'darkred',
    # 'lightred',
    'orange',
    # 'beige',
    'green',
    'darkgreen',
    # 'lightgreen',
    'darkblue',
    'lightblue',
    'purple',
    'darkpurple',
    'pink',
    # 'cadetblue',
    # 'lightgray',
    # 'black'
]

def render_heatmap(df: pd.DataFrame) -> str:
    center = (49.83, 24.02)

    _map = folium.Map(
        location=center,
        tiles='cartodbpositron',
        zoom_start=13, 
        control_scale=True
    )
    
    data = df[["LATITUDE", "LONGITUDE"]].values.tolist()
    _ = HeatMap(
        data,
        min_opacity=0.05,
        max_opacity=0.9,
        radius=25
    ).add_to(_map)

    if not os.path.exists('maps/'):
        os.makedirs('maps/')

    path = 'maps/heatmap.html'
    _map.save(path)
    webbrowser.open(f'file://{os.path.abspath(path)}')
    return path


def render_route(df: pd.DataFrame) -> str:
    def get_frame(i: int, lat: float, lon: float) -> folium.IFrame:
        popup_html = f"<b>Number:</b> {i}<br /><b>Latitude:</b> {lat}<br /><b>Longitude:</b> {lon}"
        return folium.IFrame(width=200, height=110, html=popup_html)

    _points = [(row["LATITUDE"], row["LONGITUDE"]) for _, row in df.iterrows()]

    # FILTERING POINTS THAT ARE LOCATED IN LVIV
    points = []
    dist = lambda x, y: ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** (1/2)
    center = (49.83, 24.02) # CENTER OF LVIV
    radius = 0.06
    for p in _points:
        if dist(center, p) < radius:
            points.append(p)

    _map = folium.Map(
        location=center,
        tiles='cartodbpositron',
        zoom_start=13, 
        control_scale=True
    )

    folium.Marker(
        location=points[0],
        popup=folium.Popup(get_frame(0, points[0][0], points[0][1]))
    ).add_to(_map)

    for i in range(len(points) - 1):
        G_walk = ox.graph_from_place("Lviv, Ukraine", network_type='drive', simplify=True, retain_all=False)
        orig_node = ox.nearest_nodes(G_walk, points[i][1], points[i][0])
        dest_node = ox.nearest_nodes(G_walk, points[i + 1][1], points[i + 1][0])

        route = nx.shortest_path(G_walk, orig_node, dest_node, weight='length', method='dijkstra')

        color = COLORS[randint(0, len(COLORS) - 1)]
        _map = ox.plot_route_folium(G_walk, route, route_map=_map, color=color)

        folium.Marker(
            location=points[i + 1],
            popup=folium.Popup(get_frame(i + 1, points[i + 1][0], points[i + 1][1])),
            icon=folium.Icon(color=color)
        ).add_to(_map)

    if not os.path.exists('maps/'):
        os.makedirs('maps/')

    path = 'maps/route.html'
    _map.save(path)
    webbrowser.open(f'file://{os.path.abspath(path)}')
    return path
