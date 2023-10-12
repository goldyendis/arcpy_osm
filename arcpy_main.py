from datetime import date

import arcpy.management
import arcpy.conversion

from processing.abstract.feature_process_factory import FeatureProcessFactory
from processing.building_area import FeatureClassBuildingArea
from processing.gdb import GDB
from processing.gdb_refresh import GDBRefresh
from processing.highway_line import FeatureClassHighwayLine


def main():
    """Close ArcPro before running the script"""
    gdb = GDB(name=f"{date.today().strftime('%Y%m%d')}")
    gdb_refresh = GDBRefresh(gdb=gdb)
    arcpy.env.workspace = fr"{gdb_refresh.project_location}\{gdb.name}.gdb"
    gdb_refresh.gdb.set_features(arcpy.ListFeatureClasses())
    for feature in gdb_refresh.gdb.features:
        print(feature)
        FeatureProcessFactory.create_factory(feature)
    FeatureClassBuildingArea(feature="building_area").process_buildings()
    # gdb_refresh.remove_original_shps()
    # gdb_refresh.update_datasource()
    # gdb_refresh.change_name_to_nulla()


if __name__ == '__main__':
    main()
