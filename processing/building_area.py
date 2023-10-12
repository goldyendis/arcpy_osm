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

    def process_buildings(self):
        from processing.landuse import FeatureClassLanduseArea
        from processing.feature_class_common import FeatureClassCommon
        landuse_area = FeatureClassLanduseArea(feature="landuse_area", helper=True)
        power_area = FeatureClassCommon(feature="power_area")
        amenity_area = FeatureClassCommon(feature="amenity_area")
        man_made_area = FeatureClassCommon(feature="man_made_area")
        aeroway_area = FeatureClassCommon(feature="aeroway_area")

        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_feature_by_locations(
                overlap_type="COMPLETELY_WITHIN",
                target=landuse_area.fcgeometry.select_features_by_attributes(
                    where_clause="landuse IN ('brownfield', 'construction', 'landfill', 'railway', "
                                 "'industrial') "
                ),
                distance="0 Meters",
                selection_type="NEW_SELECTION",
                invert_spatial_relationship="NOT_INVERT"

            ),
            field="type",
            expression="ipari",
            code_block="",

        )
        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_feature_by_locations(
                overlap_type="COMPLETELY_WITHIN",
                target=power_area.fcgeometry.select_features_by_attributes(
                    attribute="power",
                    field="plant"
                ),
                distance="0 Meters",
                selection_type="NEW_SELECTION",
                invert_spatial_relationship="NOT_INVERT"

            ),
            field="type",
            expression="ipari",
            code_block="",

        )
        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_feature_by_locations(
                overlap_type="COMPLETELY_WITHIN",
                target=amenity_area.fcgeometry.select_features_by_attributes(
                    where_clause="amenity IN ('prison', 'refugee_site', 'vehicle_inspection')"
                ),
                distance="0 Meters",
                selection_type="NEW_SELECTION",
                invert_spatial_relationship="NOT_INVERT"

            ),
            field="type",
            expression="ipari",
            code_block="",

        )
        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_feature_by_locations(
                overlap_type="COMPLETELY_WITHIN",
                target=man_made_area.fcgeometry.select_features_by_attributes(
                    where_clause="man_made IN ('monitoring_station', 'pumping_station', 'wastewater_plant', "
                                 "'water_works')"
                ),
                distance="0 Meters",
                selection_type="NEW_SELECTION",
                invert_spatial_relationship="NOT_INVERT"

            ),
            field="type",
            expression="ipari",
            code_block="",

        )
        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_feature_by_locations(
                overlap_type="COMPLETELY_WITHIN",
                target=aeroway_area.fcgeometry.select_features_by_attributes(
                    attribute="aeroway", field="aerodrome"
                ),
                distance="0 Meters",
                selection_type="NEW_SELECTION",
                invert_spatial_relationship="NOT_INVERT"

            ),
            field="type",
            expression="ipari",
            code_block="",

        )
        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_feature_by_locations(
                overlap_type="COMPLETELY_WITHIN",
                target=landuse_area.fcgeometry.select_features_by_attributes(
                    attribute="landuse", field="farmyard"
                ),
                distance="0 Meters",
                selection_type="NEW_SELECTION",
                invert_spatial_relationship="NOT_INVERT"

            ),
            field="type",
            expression="mezőgazdasági",
            code_block="",

        )
        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_feature_by_locations(
                overlap_type="COMPLETELY_WITHIN",
                target=amenity_area.fcgeometry.select_features_by_attributes(
                    where_clause="amenity IN ('animal_breeding', 'animal_shelter', 'animal_training')"
                ),
                distance="0 Meters",
                selection_type="NEW_SELECTION",
                invert_spatial_relationship="NOT_INVERT"

            ),
            field="type",
            expression="mezőgazdasági",
            code_block="",

        )

        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_features_by_attributes(
            where_clause="amenity = 'None' And shop = 'None' And tourism = 'None' And leisure = 'None' And man_made = "
                         "'None' And historic = 'None' And type = ' '",
        ),
            field="type",
            expression="!building!",
            expression_type="PYTHON3",
            code_block="",
        )

        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_features_by_attributes(
                where_clause="amenity <> 'None' And shop = 'None' And tourism = 'None' And leisure = 'None' And "
                             "man_made = "
                             "'None' And historic = 'None' And type = ' '",
            ),
            field="type",
            expression="!amenity!",
            expression_type="PYTHON3",
            code_block="",
        )

        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_features_by_attributes(
                where_clause="amenity = 'None' And shop <> 'None' And tourism = 'None' And leisure = 'None' And "
                             "man_made = "
                             "'None' And historic = 'None' And type = ' '",
            ),
            field="type",
            expression="!shop!",
            expression_type="PYTHON3",
            code_block="",
        )

        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_features_by_attributes(
                where_clause="amenity = 'None' And shop = 'None' And tourism <> 'None' And leisure = 'None' And "
                             "man_made = "
                             "'None' And historic = 'None' And type = ' '",
            ),
            field="type",
            expression="!tourism!",
            expression_type="PYTHON3",
            code_block="",
        )

        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_features_by_attributes(
                where_clause="amenity = 'None' And shop = 'None' And tourism = 'None' And leisure <> 'None' And "
                             "man_made = "
                             "'None' And historic = 'None' And type = ' '",
            ),
            field="type",
            expression="!leisure!",
            expression_type="PYTHON3",
            code_block="",
        )

        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_features_by_attributes(
                where_clause="amenity = 'None' And shop = 'None' And tourism = 'None' And leisure = 'None' And "
                             "man_made <> "
                             "'None' And historic = 'None' And type = ' '",
            ),
            field="type",
            expression="!man_made!",
            expression_type="PYTHON3",
            code_block="",
        )

        self.fcgeometry.calculate_field(
            in_table=self.fcgeometry.select_features_by_attributes(
                where_clause="amenity = 'None' And shop = 'None' And tourism = 'None' And leisure = 'None' And "
                             "man_made = "
                             "'None' And historic <> 'None' And type = ' '",
            ),
            field="type",
            expression="!historic!",
            expression_type="PYTHON3",
            code_block="",
        )

