import folium
from folium.plugins import HeatMap
import pandas as pd
import osmnx as ox
import networkx as nx

ox.config(log_console=True, use_cache=True)


def render_heatmap(df: pd.DataFrame):
    _map = folium.Map(
        location=[df["LATITUDE"].mean(), df["LONGITUDE"].mean()], 
        zoom_start=6, 
        control_scale=True
    )
    
    data = df[["LATITUDE", "LONGITUDE"]].values.tolist()
    _heatmap = HeatMap(
        data,
        min_opacity=0.05,
        max_opacity=0.9,
        radius=25
    ).add_to(_map)
    _map.save('maps/index_heatmap.html')


def render_route(df: pd.DataFrame):
    def get_frame(i: int) -> folium.IFrame:
        popup_html = f"<b>Number:</b> {i}"
        return folium.IFrame(width=200, height=110, html=popup_html)

    points = [(row["LATITUDE"], row["LONGITUDE"]) for i, row in df.iterrows()]

    # points = [points[i] for i in [3939, 4714]]

    _map = folium.Map(
        location=[df["LATITUDE"].mean(), df["LONGITUDE"].mean()], 
        zoom_start=6, 
        control_scale=True
    )

    # G_walk = ox.graph_from_place("Lviv, Ukraine", network_type='drive', simplify=True, retain_all=False)
    # orig_node = ox.nearest_nodes(G_walk, points[0][1], points[0][0])
    # dest_node = ox.nearest_nodes(G_walk, points[1][1], points[1][0])

    # route = nx.shortest_path(G_walk, orig_node, dest_node, weight='length')
    # _map = ox.plot_route_folium(G_walk, route)

    for i in range(len(points)):
        folium.Marker(location=points[i], popup=folium.Popup(get_frame(i))).add_to(_map)

    _map.save('maps/index_route.html')

    # sw = df[["LATITUDE", "LONGITUDE"]].min().values.tolist()
    # ne = df[["LATITUDE", "LONGITUDE"]].max().values.tolist()
    # _map.fit_bounds([sw, ne])


if __name__ == '__main__':
    df = pd.read_csv('csv/266.csv')
    df.rename({
        1: "LATITUDE",
        2: "LONGITUDE"
    })
    # render_heatmap(df)
    render_route(df)
