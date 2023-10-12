import glob
import pathlib
import re

from processing.gdb import GDB
from utils_arcpro.utils import base_project_location, shp_location, shp_files, project_file_location, \
    coordinate_system, \
    extra_features
import arcpy.management
import arcpy.conversion
import arcpy.mp
import arcpy.da


class GDBRefresh:
    def __init__(self, gdb: GDB) -> None:
        self.project_location = base_project_location
        self.gdb = gdb
        self.shp_location = shp_location
        self.shp_files = shp_files
        self.aprx = arcpy.mp.ArcGISProject(project_file_location)
        self.create_gdb()
        self.import_to_gdb()
        self.import_extra_features_to_gdb()

    def create_gdb(self) -> None:
        arcpy.management.CreateFileGDB(
            out_folder_path=self.project_location,
            out_name=self.gdb.name,
        )

    def import_to_gdb(self) -> None:
        out_gdb = f"{self.project_location}\\{self.gdb.name}.gdb"
        arcpy.conversion.FeatureClassToGeodatabase(
            Input_Features=[self.shp_location + "\\" + x for x in self.shp_files],
            Output_Geodatabase=out_gdb
        )
        arcpy.CreateFeatureclass_management(
            out_path=out_gdb,
            out_name="building_area",
            geometry_type="POLYGON"
        )
        arcpy.CreateFeatureclass_management(
            out_path=out_gdb,
            out_name="highway_line",
            geometry_type="POLYLINE"
        )
        arcpy.CreateFeatureclass_management(
            out_path=out_gdb,
            out_name="highway_egyben_line",
            geometry_type="POLYLINE"
        )
        arcpy.CreateFeatureclass_management(
            out_path=out_gdb,
            out_name="highway_line_hid",
            geometry_type="POLYLINE"
        )

    def import_extra_features_to_gdb(self):
        arcpy.conversion.FeatureClassToGeodatabase(
            Input_Features=[self.project_location + "\\" + x for x in extra_features],
            Output_Geodatabase=f"{self.project_location}\\{self.gdb.name}.gdb"
        )

    # def remove_original_shps(self) -> None:
    #     files = [pathlib.Path(file).name for file in glob.glob(fr"{self.shp_location}\*.*")]
    #     for file in files:
    #         os.remove(f"{self.shp_location}\\{file}")

    def update_datasource(self) -> None:
        pro_map = self.aprx.listMaps()[0]
        project_gdbs = [pathlib.Path(i).name for i in glob.glob(fr"{self.project_location}\\*.gdb") if
                        re.match("^\d{8}", pathlib.Path(i).name) is not None]
        project_gdbs.sort(reverse=True)

        # TODO két IF-et kivenni a véglegesben, más réteg ne legyen a Proban,csak amihez van a gdb-ben is feature
        for layer in pro_map.listLayers():
            if layer.name != "fonts":
                new_connection_properties = layer.connectionProperties
                if new_connection_properties["connection_info"]["database"] is not None:
                    new_connection_properties["connection_info"]["database"] = \
                        fr"{self.project_location}\{project_gdbs[0]}"
                    layer.updateConnectionProperties(layer.connectionProperties, new_connection_properties)
                    print(layer.connectionProperties)

    def change_name_to_nulla(self):
        pro_map = self.aprx.listMaps()[0]
        for layer in pro_map.listLayers():
            arcpy.management.CalculateField(
                in_table= layer,
                field="name",
                expression="change_name(!name!)",
                code_block="""def change_name(name):
                                  if name == "None":
                                      return "nulla" """
            )
            arcpy.management.SelectLayerByAttribute(layer, "CLEAR_SELECTION")

        self.aprx.save()
