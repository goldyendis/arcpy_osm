from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassLanduseArea(AbstractFeatureClass):
    def __init__(self, feature: str) -> None:
        """
        Concrete class to process Landuse Area feature layer
        :param feature: str | The name of the feature layer
        """
        super().__init__(feature = feature)

        self.fcgeometry.simplify_to_scale()
        self.fcgeometry.calculate_area()
