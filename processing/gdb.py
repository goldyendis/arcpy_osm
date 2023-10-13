from typing import List


class GDB:
    """ESRI GeoDatabase to create"""
    def __init__(self, name: str, features: List[str] = None):
        self.name = name
        self.features = features

    def set_features(self, value):
        self.features = value
