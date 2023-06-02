from manipulation.feature_class_geometry import FeatureClassGeometry
from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassRailwayLine(AbstractFeatureClass):
    def __init__(self, feature: str, helper:bool = False) -> None:
        """
        Concrete class to process Railway Line feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__(feature=feature)

        if not helper:
            print("RAILWAY LINE")
            if self.name.find("egyben") > -1:
                delete_features = ["funicular", "light_rail", "miniature", "narrow_gauge", "platform", "subway","tram"]
                for field in delete_features:
                    self.fcgeometry.delete_features(attribute="railway", field=field)

                self.fcgeometry.dissolve(in_feature=self.name,
                                         fields="railway;service;usage",
                                         unsplit_lines="UNSPLIT_LINES",
                                         )
