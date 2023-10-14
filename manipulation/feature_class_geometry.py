from datetime import date

import arcpy.management
import arcpy.cartography
import arcpy.analysis
import arcpy.edit

from utils_arcpro.simplify import Simplify


class FeatureClassGeometry:
    def __init__(self, name: str, geometry: str) -> None:
        """Class to manipulate Fields and geometry of the FeatureLayers.
        :param name: str | The name of the feature layer
        :param geometry: str | Type of geometry("area","line","point")
        """
        self.name = name
        self.geometry = geometry

    def dissolve(self, in_feature, fields=None, multi_part: str = "SINGLE_PART", unsplit_lines: str = "DISSOLVE_LINES",
                 diff_name: str = None):
        arcpy.management.Dissolve(
            in_features=in_feature,
            dissolve_field=fields,
            statistics_fields=None,
            multi_part=multi_part,
            unsplit_lines=unsplit_lines,
            out_feature_class=fr"{arcpy.env.workspace}\{in_feature}_dissolve" if diff_name is None else fr"{arcpy.env.workspace}\{diff_name}_dissolve", )

        return fr"{arcpy.env.workspace}\{self.name}_dissolve" if diff_name is None else fr"{arcpy.env.workspace}\{diff_name}_dissolve"

    def simplify_to_scale(self, input_feature: str = None) -> None:
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
                    fr"{arcpy.env.workspace}\{self.name}" if input_feature is None else input_feature,
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

    def calculate_field(self, field: str, code_block: str, expression: str = None,
                        expression_type: str = "PYTHON3", field_type: str = "TEXT", in_table=None):
        arcpy.CalculateField_management(
            in_table=self.name if in_table is None else in_table,
            field=field, expression="function()" if expression is None else expression,
            expression_type=expression_type,
            code_block=code_block, field_type=field_type
        )

    def copy_feature_layer(self, out_name: str, input_feature: str = None) -> None:
        """
        Copies a feature class into the GDB, with suffix "_1" name
        :param: str | name of the output feature
        """
        arcpy.management.CopyFeatures(
            in_features=self.name if input_feature is None else input_feature,
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

    def delete_features(self, attribute: str = None, field: str = None, in_view=None):
        if in_view is not None:
            arcpy.management.DeleteRows(
                in_rows=in_view)
        else:
            arcpy.management.DeleteRows(
                arcpy.management.SelectLayerByAttribute(
                    in_layer_or_view=self.name,
                    selection_type="NEW_SELECTION",
                    where_clause=f"{attribute} = '{field}'"
                )
            )

    def select_features_by_attributes(self, attribute: str = None, field: str = None,
                                      selection_type: str = "NEW_SELECTION",
                                      invert="NON_INVERT", in_view: str = None, where_clause: str = None):
        return arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=self.name if in_view is None else in_view,
            selection_type=selection_type,
            where_clause=where_clause if where_clause is not None else f"{attribute} = '{field}'",
            invert_where_clause=invert
        )

    def select_feature_by_locations(self, target, in_layer=None, selection_type="NEW_SELECTION", invert=True,
                                    overlap_type: str = None, distance: str = None):
        return arcpy.management.SelectLayerByLocation(
            in_layer=self.name if in_layer is None else in_layer,
            overlap_type=overlap_type if overlap_type is not None else "WITHIN_A_DISTANCE",
            select_features=target,
            search_distance=distance,
            selection_type=selection_type,
            invert_spatial_relationship=invert
        )

    def snap_railway_stations_to_line(self, line):
        railway_line_light_rail = line.select_features_by_attributes(attribute="railway", field="light_rail")
        railway_line_rail = line.select_features_by_attributes(attribute="railway", field="rail")
        railway_line_rail_all = line.select_features_by_attributes(
            attribute="railway", field="narrow_gauge", in_view=railway_line_rail, selection_type="ADD_TO_SELECTION")
        railway_line_subway = line.select_features_by_attributes(attribute="railway", field="subway")

        arcpy.edit.Snap(
            in_features=self.select_features_by_attributes(attribute="station", field="light_rail"),
            snap_environment=f"{railway_line_light_rail} EDGE '50 Meters';{railway_line_light_rail} VERTEX '50 Meters'"
        )

        railway_with_tram = self.select_features_by_attributes(attribute="station", field="None")
        railway = self.select_features_by_attributes(selection_type="REMOVE_FROM_SELECTION", attribute="railway",
                                                     field="tram_stop", in_view=railway_with_tram)
        arcpy.edit.Snap(
            in_features=railway,
            snap_environment=f"{railway_line_rail_all} EDGE '50 Meters';{railway_line_rail_all} VERTEX '50 Meters'"
        )
        arcpy.edit.Snap(
            in_features=self.select_features_by_attributes(attribute="station", field="subway"),
            snap_environment=f"{railway_line_subway} EDGE '50 Meters';{railway_line_subway} VERTEX '50 Meters'"
        )
        railway_not_touch = self.select_feature_by_locations(in_layer="railway_point", target="railway_egyben_line",
                                                             distance="1 Meters")
        railway_to_delete_one = self.select_features_by_attributes(
            attribute="station", field="funicular", in_view=railway_not_touch, selection_type="REMOVE_FROM_SELECTION")
        railway_to_delete_two = self.select_features_by_attributes(
            attribute="railway", field="tram_stop", in_view=railway_to_delete_one,
            selection_type="REMOVE_FROM_SELECTION")
        railway_to_delete = self.select_features_by_attributes(
            attribute="station", field="light_rail", in_view=railway_to_delete_two,
            selection_type="REMOVE_FROM_SELECTION")

        self.delete_features(in_view=railway_to_delete)

    def buffer(self, in_feature: str, distance: str = "15"):
        arcpy.analysis.PairwiseBuffer(
            in_features=in_feature,
            out_feature_class=fr"{arcpy.env.workspace}\{self.name}_buffer",
            buffer_distance_or_field=f"{distance} Meters",
            dissolve_option="NONE",
            dissolve_field=None,
            method="PLANAR",
            max_deviation="0 Meters"
        )

    def clip(self, in_feature: str, clippe: str):
        arcpy.analysis.PairwiseClip(
            in_features=in_feature,
            clip_features=clippe,
            out_feature_class=fr"{arcpy.env.workspace}\{in_feature}_clipped",
            cluster_tolerance=None
        )

    def multipart_to_singlepart(self, in_feature: str):
        arcpy.management.MultipartToSinglepart(
            in_features=in_feature,
            out_feature_class=fr"{arcpy.env.workspace}\{in_feature}_singlepart"
        )

    def spatial_join_railway_angle(self):
        arcpy.analysis.SpatialJoin(
            target_features=self.name,
            join_features=fr"{arcpy.env.workspace}\railway_egyben_line_clipped_singlepart_dissolve",
            out_feature_class=fr"{arcpy.env.workspace}\{self.name}_angle",
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            field_mapping='geom_type "geom_type" true true false 80 Text 0 0,First,#,railway_point,geom_type,0,'
                          '80;name "name" true true false 80 Text 0 0,First,#,railway_point,name,0,80;railway '
                          '"railway" true true false 80 Text 0 0,First,#,railway_point,railway,0,80;station "station" '
                          'true true false 80 Text 0 0,First,#,railway_point,station,0,80;angle "angle" true true '
                          'false 4 Float 0 0,First,#,railway_egyben_line_clipped_singlepart_dissolve,angle,-1,-1',
            match_option="WITHIN_A_DISTANCE",
            search_radius="1 Meters",
            distance_field_name=""
        )

    def spatial_join_waterway_angle(self):
        arcpy.analysis.SpatialJoin(
            target_features=self.name,
            join_features=fr"{arcpy.env.workspace}\waterway_line_clipped_singlepart_dissolve",
            out_feature_class=fr"{arcpy.env.workspace}\{self.name}_angle",
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            field_mapping='geom_type "geom_type" true true false 80 Text 0 0,First,#,waterway_point,geom_type,0,'
                          '80;name "name" true true false 80 Text 0 0,First,#,waterway_point,name,0,80;waterway '
                          '"waterway" true true false 80 Text 0 0,First,#,waterway_point,waterway,0,80;angle "angle" '
                          'true true false 8 Double 0 0,First,#,waterway_line__PairwiseDisso_4,angle,-1,-1',
            match_option="WITHIN_A_DISTANCE",
            search_radius="2 Meters",
            distance_field_name=""
        )

    def split_line_at_vertices(self, in_feature: str = None):
        return arcpy.management.SplitLine(
            in_features= in_feature,
            out_feature_class=fr"{arcpy.env.workspace}\{in_feature}_split"
        )

    def append_pedestrian(self, in_feature):
        arcpy.management.Append(
            inputs=in_feature,
            target="highway_line",
            schema_type="TEST",
            field_mapping=None,
            subtype="",
            expression="highway = 'pedestrian'",
            match_fields=None,
            update_geometry="NOT_UPDATE_GEOMETRY"
        )

    def append(self, in_feature: str, target: str, exp_column: str = None, exp_value: str = None, sql: str = None):
        arcpy.management.Append(
            inputs=in_feature,
            target=target,
            schema_type="TEST",
            field_mapping=None,
            subtype="",
            expression=f"{exp_column} = '{exp_value}'" if sql is None else sql,
            match_fields=None,
            update_geometry="NOT_UPDATE_GEOMETRY"
        )

    def append_highway_line_hid(self, in_feature: str):
        arcpy.management.Append(
            inputs=in_feature,
            target=fr"{arcpy.env.workspace}\highway_line_hid",
            schema_type="NO_TEST",
            expression="""highway LIKE '%hid'""",
            subtype="",
            field_mapping="",
            # field_mapping='geom_type "geom_type" true true false 80 Text 0 0,First,#,highway_line,geom_type,0,'
            #               '80;name "name" true true false 80 Text 0 0,First,#,highway_line,name,0,80;highway '
            #               '"highway" true true false 80 Text 0 0,First,#,highway_line,highway,0,80;bridge "bridge" '
            #               'true true false 80 Text 0 0,First,#,highway_line,bridge,0,80;tunnel "tunnel" true true '
            #               'false 80 Text 0 0,First,#,highway_line,tunnel,0,80;ref "ref" true true false 80 Text 0 0,'
            #               'First,#,highway_line,ref,0,80;Shape_Length "Shape_Length" false true true 8 Double 0 0,'
            #               'First,#,highway_line,Shape_Length,-1,-1',
            match_fields=None,
            update_geometry="NOT_UPDATE_GEOMETRY"
        )

    def export_railway_line_alagut(self):
        arcpy.conversion.ExportFeatures(
            in_features="railway_line",
            out_features=fr"{arcpy.env.workspace}\railway_line_alagut",
            where_clause="railway LIKE '%alagut'",
            use_field_alias_as_name="NOT_USE_ALIAS",
            field_mapping='geom_type "geom_type" true true false 80 Text 0 0,First,#,railway_line,geom_type,0,'
                          '80;name "name" true true false 80 Text 0 0,First,#,railway_line,name,0,80;railway '
                          '"railway" true true false 80 Text 0 0,First,#,railway_line,railway,0,80;Shape_Length '
                          '"Shape_Length" false true true 8 Double 0 0,First,#,railway_line,Shape_Length,-1,-1',
            sort_field=None
        )

    def delete_fields(self, delete_field: list[str], input_feature: str = None):
        arcpy.management.DeleteField(
            in_table=self.name if input_feature is None else input_feature,
            drop_field=delete_field,
            method="DELETE_FIELDS"
        )

    def erase(self, erase, input_feature):
        arcpy.analysis.Erase(
            in_features=input_feature,
            erase_features=erase,
            out_feature_class=fr"{arcpy.env.workspace}\{self.name}_erase",
            cluster_tolerance=None
        )

    def dissolve_boundaries(self, input_feature: str, fields: list[str]):
        arcpy.gapro.DissolveBoundaries(
            input_layer=input_feature,
            out_feature_class=fr"{arcpy.env.workspace}\{input_feature}_dissolve",
            multipart="SINGLE_PART",
            dissolve_fields="DISSOLVE_FIELDS",
            fields=fields,
            summary_fields=None
        )