class GDB:
    """ESRI GeoDatabase to create"""
    def __init__(self, name, features=None):
        self.name = name
        self.features = features

    def set_features(self, value):
        self.features = value
