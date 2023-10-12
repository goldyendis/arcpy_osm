import arcpy
import arcpy.management
from processing.abstract.feature_process_abstract import AbstractFeatureClass


class FeatureClassBuildingArea(AbstractFeatureClass):
    def __init__(self, feature: str, helper: bool = False) -> None:
        """
        Concrete class to process Building Area feature layer
        :param feature: str | The name of feature layer
        """
        super().__init__(feature=feature)
        self.append_to_building_area()

    def append_to_building_area(self) -> None:
        """
        Append the features from this feature class to the "building_area" feature class in the specified
        geodatabase.
        """
        arcpy.management.Append(
            inputs=self.name,
            target="building_area",
            schema_type="NO_TEST",
            field_mapping="",
            subtype="",
            expression="",
            match_fields=None,
            update_geometry="NOT_UPDATE_GEOMETRY"
)