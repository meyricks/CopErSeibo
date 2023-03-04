# file de backend
import xml.etree.ElementTree as ET
from math import sin, cos, sqrt, atan2, radians
import heapq
import folium

class UCS:
    def __init__(self, graph):
        self.graph = graph

    # Implemetación del algoritmo UCS
    def ucs(self, start, goal):
        visited = set()
        queue = [(0, start, [])]
        heapq.heapify(queue)
        while queue:
            (cost, node, path) = heapq.headppop(queue)
            if node not in visited:
                visited.add(node)
                path = path + [node]
                if node == goal:
                    return path
                for neighboor, distance in self.graph[node]:
                    if neighboor not in visited:
                        heapq.heappush(queue, (cost + distance, neighboor, path))
        return []
        
    # Funcion para calcular la distancia entre dos puntos dados sus coordenadas latitud y longitud
    @staticmethod

    def distance(loc1, loc2):
        R = 6373.0 # radio de la tierra en km
        lat1, lon1, lat2, lon2 = map(radians, list(loc1+loc2))
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance
        
class AdjacentList:
    adj_list = {}
    nodes_dict = {}

    def __init__(self, filename):
        self.root = self.parse_osm(filename) 
        self.create_adj_list()

        #Crear una lista de adyacencia de los nodos y sus nodos adyacentes con sus distancias
    def create_adj_list(self):
        self.set_node_coordinates(self.root)

        for way in self.root.findall("./way"):
            # Obtener los nodos que forman el way
            nodes = [node.attrib["ref"] for node in way.findall("./nd")]
            # Agregar las conexiones a la lista de adyacencia
            for i, node in enumerate(nodes):
              self.set_node_distance(i, node, nodes)
        
    def set_node_distance(self, i, node, nodes):
        if i > 0:
            dist = UCS.distance(
                (self.nodes_dict[node]["lat"], self.nodes_dict[node]["lon"]),
                (self.nodes_dict[nodes[i-1]]["lat"], self.nodes_dict[nodes[i-1]]["lon"])
            
            )
            self.adj_list.setdefault(node, []).append((nodes[i-1], dist))
            if i < len(nodes)-1:
                dist = UCS.distance(
                    (self.nodes_dict[node]["lat"], self.nodes_dict[node]["lon"]),
                    (self.nodes_dict[nodes[i+1]]["lat"], self.nodes_dict[nodes[i+1]]["lon"])
                )
                self.adj_list.setdefault(node, []).append((nodes[i+1], dist))

        # Parsear el archivo XML

    def parse_osm(self, filename):
        tree = ET.parse("el_seibo.osm")
        return tree.getroot()
    
    def set_node_coordinates(self, root):
        for node in root.findall("./node"):
            node_id = node.attrib["id"]
            self.nodes_dict[node_id] = {
                "lat": float(node.attrib["lat"]),
                "lon": float(node.attrib["lon"])
            }
    def get_coordinates(self, node_id):
        return self.nodes_dict[node_id]["lat"], self.nodes_dict[node_id]["lon"]
                    
class Graph:
    def __init__(self, from_file="el_seibo.osm"):
        self.adjacent_list = AdjacentList(from_file)
        self.ucs_algo = UCS(self.adjacent_list.adj_list)

    def get_optimal_route(self, start_node, goal_node):
        # Buscamos la ruta mas optima entre los nodos de inicio y final
        # Devuelve una lista con los nodos transitorios

        return self.ucs_algo.ucs(start_node, goal_node)
    
    def generate_map(self, start_node, goal_node, zoom_start=15):
        # Obtenemos la ruta optima y sus coordenadas
        path = self.get_optimal_route(start_node, goal_node)
        path_coords = [self.adjacent_list.get_coordinates(node) for node in path]

        # Configuracion del mapa
        folium_map = folium.Map(location=path_coords[0], zoom_start=15)

        # Marcador del inicio
        folium.Marker(location=path_coords[0], icon=folium.Icon(color="green")).add_to(folium_map)

        # Marcador del fin
        folium.Marker(location=path_coords[-1], icon=folium.Icon(color="red")).add_to(folium_map)

        # Dibujar la ruta
        folium.PolyLine(locations=path_coords, color="blue").add_to(folium_map)

        # Mostrar el mapa
        return folium_map
    
if __name__ == "__main___":
    # Definimos los nodos de incio y final
    start_node = input("Ingrese el primer nodo: ")
    goal_node = input("Ingrese el segundo nodo: ")
    graph = Graph()
    path = graph.get_optimal_route(start_node, goal_node)

    # Imprimimos la ruta encontrada
    if not path:
        print(f"No se encontro ruta entre {start_node} y {goal_node}")
    else:
        print(f"Ruta encontrada: {' -> '.join(path)}")


        