from datetime import date

import arcpy.management
import arcpy.cartography
import arcpy.analysis

from utils_arcpro.simplify import Simplify


class FeatureClassGeometry:
    def __init__(self, name: str, geometry: str) -> None:
        """
        Class to manipulate Fields and geometry of the FeatureLayers
        :param name: str | The name of the feature layer
        :param geometry: str | Type of geometry("area","line","point")
        """
        self.name = name
        self.geometry = geometry

    # def dissolve(self, fields, layer = None, ):
    #     if layer is None:
    #         arcpy.management.Dissolve(
    #             fr"{arcpy.env.workspace}\{self.name}",
    #             fr"{arcpy.env.workspace}\{self.name}_dissolve",
    #             "name;landuse", None, "MULTI_PART", "UNSPLIT_LINES", '')
    #         return fr"{arcpy.env.workspace}\{self.name}_dissolve"
    #     else:
    #         arcpy.management.Dissolve(
    #             fr"{arcpy.env.workspace}\{layer}",
    #             fr"{arcpy.env.workspace}\{layer}_dissolve",
    #             *fields, None, "MULTI_PART", "UNSPLIT_LINES", '')
    #         return fr"{arcpy.env.workspace}\{self.name}_dissolve"

    def simplify_to_scale(self) -> None:
        """
        create multiple Simplified feature classes and calculate Area/Length of features
        1 : 2 300 000 -- 1 : 1 155 000 -->> Simplify_1
        1 : 577 000 -- 1 : 288 000 -->> Simplify_2
        1 : 144 000 -- 1 : 72 000 -->> Simplify_3
        """
        for i in range(1, 4):
            if self.geometry == "area":
                print(f"{self.name}_simplify_{i}")
                arcpy.cartography.SimplifyPolygon(
                    fr"{arcpy.env.workspace}\{self.name}",
                    fr"{arcpy.env.workspace}\{self.name}_simplify_{i}",
                    *Simplify().get_simplify_properties(str(i), geometry=self.geometry)
                )
                self.calculate_area(feature_name=fr"{arcpy.env.workspace}\{self.name}_simplify_{i}")

    def calculate_area(self, feature_name: str = None) -> None:
        """
        Insert a new Field and calculating the features area into it
        :param feature_name: str | the name of feature layer to calculate the area
        """
        if feature_name is None:
            arcpy.AddField_management(self.name, "Calc_Area", "DOUBLE")
            arcpy.CalculateField_management(self.name, "Calc_Area", "!SHAPE.AREA@SQUAREMETERS!", "PYTHON_9.3")
        else:
            arcpy.AddField_management(feature_name, "Calc_Area", "DOUBLE")
            arcpy.CalculateField_management(feature_name, "Calc_Area", "!SHAPE.AREA@SQUAREMETERS!", "PYTHON_9.3")

    def copy_feature_layer(self, out_name: str) -> None:
        """
        Copies a feature class into the GDB, with suffix "_1" name
        :param: str | name of the output feature
        """
        arcpy.management.CopyFeatures(
            in_features=self.name,
            out_feature_class=fr"{arcpy.env.workspace}\{out_name}")

    def integrate(self, distance: int, layer: str = None) -> None:
        """
        Cluster together multiple point, which are in the distance each other
        :param layer: str | input feature name
        :param distance: int | point in meters distance each other to aggregate
        """
        if layer is None:
            with arcpy.EnvManager(XYTolerance=f"{distance} Meters"):
                arcpy.analysis.PairwiseIntegrate(self.name, None)
        else:
            with arcpy.EnvManager(XYTolerance=f"{distance} Meters"):
                arcpy.analysis.PairwiseIntegrate(layer, None)

    def add_x_y(self, layer: str = None) -> None:
        """
        Add X an Y coordinates to the layer
        :param layer: str | name of the feature class
        """
        if layer is None:
            arcpy.management.AddXY(in_features=self.name)
        else:
            arcpy.management.AddXY(in_features=layer)

    def dissolve_point(self, fields: list, layer: str = None) -> str:
        """
        Aggregates features based on specified attributes
        :param fields: list[str] | Fields to create dissolve by
        :param layer: str | name of the layer to dissolve
        :return: str | name of the new feature layer
        """
        if layer is None:
            arcpy.management.Dissolve(
                self.name,
                f"{self.name}_dissolve",
                *fields, None, "SINGLE_PART", "DISSOLVE_LINES", '')
            return fr"{self.name}_dissolve"
        else:
            arcpy.management.Dissolve(
                layer,
                f"{layer}_dissolve",
                *fields, None, "SINGLE_PART", "DISSOLVE_LINES", '')
            return fr"{layer}_dissolve"

    def spatial_join_barrier(self, target: str, join: str):
        arcpy.analysis.SpatialJoin(
            target, join, fr"{arcpy.env.workspace}\{self.name}_centralized",
            "JOIN_ONE_TO_ONE",
            "KEEP_ALL",
            'POINT_X "POINT_X" true true false 8 Double 0 0,First,#,barrier_point_1_Dissolve,POINT_X,-1,-1;POINT_Y '
            '"POINT_Y" true true false 8 Double 0 0,First,#,barrier_point_1_Dissolve,POINT_Y,-1,-1;geom_type '
            '"geom_type" true true false 80 Text 0 0,First,#,barrier_point_1,geom_type,0,80;name "name" true true '
            'false 80 Text 0 0,First,#,barrier_point_1,name,0,80;barrier "barrier" true true false 80 Text 0 0,First,'
            '#,barrier_point_1,barrier,0,80',
            "INTERSECT", "5 Meters", '')

    def select_by_attribute(self, attribute: str, out_name: str, inverse: bool = False) -> str:
        arcpy.analysis.Select(
            in_features=self.name,
            out_feature_class=fr"{arcpy.env.workspace}\{out_name}",
            where_clause=f"{self.name[:self.name.rfind('_')]} = '{attribute}'" if not inverse
            else f"{self.name[:self.name.rfind('_')]} <> '{attribute}'"
        )
        return fr"{arcpy.env.workspace}\{out_name}"

    def delete_features(self, attribute: str, field: str):
        arcpy.management.DeleteRows(
            in_rows=arcpy.management.SelectLayerByAttribute(
                in_layer_or_view=self.name,
                selection_type="NEW_SELECTION",
                where_clause=f"{attribute} = '{field}'"
            )
        )

