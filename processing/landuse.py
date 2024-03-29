from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassLanduseArea(AbstractFeatureClass):
    def __init__(self, feature: str, helper: bool = False) -> None:
        """
        Concrete class to process Landuse Area feature layer
        :param feature: str | The name of the feature layer
        """
        super().__init__(feature = feature)

        if not helper:
            self.fcgeometry.simplify_to_scale()
            self.fcgeometry.calculate_area()
            self.fcgeometry.dissolve_boundaries(
                input_feature = "landuse_area_simplify_3",
                fields=["landuse","name"]

            )
