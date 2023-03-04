import io
import osmnx as ox
import folium
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
 # pip install PyQtWebEngine
from backpack import Graph

# el querido frontend 

class Map(QWidget):
      def __init__(self) :
            super().__init__()
            self.setWindowTitle('Map routing')
            self.resize(800, 720)
            self._graph = Graph()
            self.view_zoom = 15
            self.webView = QWebEngineView()
            layout = QHBoxLayout()
            self.setLayout(layout)

            G = ox.graph_from_xml('el_seibo.osm', simplify=False)

            location = (18.873231, -69.042034) #hay que poner la coordenada de centrado o el nodo del centro
            m = folium.Map (
                  zoom_start = self.view_zoom,
                  location=location
            ) 

            # save map data to data object
            self.update_map(m)

            layout.addWidget(self.webView, stretch=7)

            # Contenedor para los textfields y el button
            textFieldLayout = QVBoxLayout()

            self.src = QLineEdit(self)
            self.src.setPlaceholderText("Origen nodeID..")
            textFieldLayout.addWidget(self.src)

            self.dst = QLineEdit(self)
            self.dst.setPlaceholderText("Destino nodeID..")
            textFieldLayout.addWidget(self)

            button = QPushButton("Encontrar ruta")
            button.clicked.connect(self.find_route)
            textFieldLayout.addWidget(button)

            layout.addLayout(textFieldLayout)
            
      def find_route(self):
            m = self._graph.generate_map(self.src.text(), self.dst.text())
            self.update_map(m)

      def update_map(self, m):
            data = io.BytesIO()
            m.save(data, close_file=False)
            self.webView.setHtml(data.getvalue().decode())


