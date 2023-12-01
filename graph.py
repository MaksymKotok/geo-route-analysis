import folium
from folium.plugins import HeatMap
import pandas as pd
import osmnx as ox
import networkx as nx
import webbrowser
import os

ox.settings.use_cache=True
ox.settings.log_console=True


def render_heatmap(df: pd.DataFrame) -> str:
    center = (49.83, 24.02)

    _map = folium.Map(
        location=center, 
        zoom_start=13, 
        control_scale=True
    )
    
    data = df[["LATITUDE", "LONGITUDE"]].values.tolist()
    _heatmap = HeatMap(
        data,
        min_opacity=0.05,
        max_opacity=0.9,
        radius=25
    ).add_to(_map)

    path = 'maps/heatmap.html'
    _map.save(path)
    webbrowser.open(f'file://{os.path.abspath(path)}')
    return path


def render_route(df: pd.DataFrame) -> str:
    def get_frame(i: int, lat: float, lon: float) -> folium.IFrame:
        popup_html = f"<b>Number:</b> {i}<br /><b>Latitude:</b> {lat}<br /><b>Longitude:</b> {lon}"
        return folium.IFrame(width=200, height=110, html=popup_html)

    _points = [(row["LATITUDE"], row["LONGITUDE"]) for _, row in df.iterrows()]

    points = []
    dist = lambda x, y: ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** (1/2)
    center = (49.83, 24.02)
    radius = 0.06
    for p in _points:
        if dist(center, p) < radius:
            points.append(p)

    _map = folium.Map(
        location=center, 
        zoom_start=13, 
        control_scale=True
    )

    G_walk = ox.graph_from_place("Lviv, Ukraine", network_type='drive', simplify=True, retain_all=False)
    orig_node = ox.nearest_nodes(G_walk, points[0][1], points[0][0])
    dest_node = ox.nearest_nodes(G_walk, points[-1][1], points[-1][0])

    route = nx.shortest_path(G_walk, orig_node, dest_node, weight='length')
    _map = ox.plot_route_folium(G_walk, route)

    # for i in range(len(points)):
    folium.Marker(location=points[0], popup=folium.Popup(get_frame(0, points[0][0], points[0][1]))).add_to(_map)
    folium.Marker(location=points[-1], popup=folium.Popup(get_frame(1, points[-1][0], points[-1][1]))).add_to(_map)

    path = 'maps/route.html'
    _map.save(path)
    webbrowser.open(f'file://{os.path.abspath(path)}')
    return path


# if __name__ == '__main__':
#     df = pd.read_csv('csv/266.csv')
#     df.rename({
#         1: "LATITUDE",
#         2: "LONGITUDE"
#     })
#     # render_heatmap(df)
#     render_route(df)
