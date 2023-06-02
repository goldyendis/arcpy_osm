from datetime import date

import arcpy.management
import arcpy.conversion

from processing.abstract.feature_process_factory import FeatureProcessFactory
from processing.gdb import GDB
from processing.gdb_refresh import GDBRefresh
from utils_arcpro.utils import base_project_location


def main():
    """Close ArcPro before running the script"""
    gdb = GDB(name=f"{date.today().strftime('%Y%m%d')}")
    gdb_refresh = GDBRefresh(gdb=gdb)
    arcpy.env.workspace = fr"{gdb_refresh.project_location}\{gdb.name}.gdb"
    gdb_refresh.gdb.set_features(arcpy.ListFeatureClasses())
    for feature in gdb_refresh.gdb.features:
        print(feature)
        FeatureProcessFactory.create_factory(feature)
    # gdb_refresh.remove_original_shps()
    # gdb_refresh.update_datasource()


if __name__ == '__main__':
    main()
