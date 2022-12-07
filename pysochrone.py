"""Pysochrone
Todo:
    * 現在は任意の点から直近のノードを参照し，そのノードからの等時線を算出している。この点を改善し任意の点からの等時線を求めたい。
    * 計算時間が非常に長いため短くしたい。
"""


import osmnx as ox
import pandas as pd
import networkx as nx
import geopandas as gpd
from shapely.geometry import Point, Polygon


def isochrone(
    lon: float, lat: float, way: str, time: float, speed: float
) -> Polygon:
    """Isochrone

    Calculate isochrone polygon from your indicate point

    Args:
        lon (float): Longitude
        lat (float): Latitude
        way (str): Means of transportation (e.g.) walk, car)
        time (float): Travel time from the indicated point. Unit is minutes.
        speed (float): Travel speed. Unit is meters per minute.

    Returns:
        shapely.geometry.Polygon: Polygon of isochrone

    Examples:

        >>> isochrone(140.08571, 35.63725, "walk", 10, 80)
        POLYGON ((140.08882 35.63135, 140.08456 35.631...
    """
    loc = (lat, lon)
    G = ox.graph_from_point(loc, simplify=True, network_type=way)
    center_node = ox.distance.nearest_nodes(G, lon, lat)

    for u, v, k, data in G.edges(data=True, keys=True):
        data["time"] = data["length"] / speed

    subgraph = nx.ego_graph(G, center_node, radius=time, distance="time")
    node_points = [
        Point(data["x"], data["y"]) for node, data in subgraph.nodes(data=True)
    ]
    return gpd.GeoSeries(node_points).unary_union.convex_hull
