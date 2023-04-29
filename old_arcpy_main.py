import math

import arcpy
import glob

from Arcpy.utils import create_temp_feature_dataset
from Simplify_schemes import Schemes
import pathlib
import datetime


class MainMethod:
    now = datetime.date.today()
    date_time = now.strftime("%Y%m%d")
    print(date_time)
    # d:\Baga\egyeb\alapterkep_pyrosm\OSM_TO_MTSZ\Arcpro
    sr = r"d:\Baga\egyeb\alapterkep_pyrosm\OSM_TO_MTSZ\area_landuse.prj"
    arcpy.env.workspace = r"d:\Baga\egyeb\alapterkep_pyrosm\OSM_TO_MTSZ\Arcpro\temp.gdb"
    shape_path = r"d:\Baga\egyeb\alapterkep_pyrosm\OSM_TO_MTSZ\shp_final"

    arcpy.env.overwriteOutput = True
    arcpy.management.CreateFileGDB(r"d:\Baga\egyeb\alapterkep_pyrosm\OSM_TO_MTSZ\Arcpro", "temp.gdb")
    arcpy.management.CreateFileGDB(r"d:\Baga\egyeb\alapterkep_pyrosm\OSM_TO_MTSZ\Arcpro", date_time + ".gdb")
    final_gdb = fr"d:\Baga\egyeb\alapterkep_pyrosm\OSM_TO_MTSZ\Arcpro\{date_time}.gdb"

    file_path = r"d:\Baga\egyeb\alapterkep_pyrosm\OSM_TO_MTSZ\shp_final"
    shp_files = [pathlib.Path(i).name for i in glob.glob(fr"{file_path}\*.shp")]
    feature_scales = [2311, 1155, 577, 288, 144, 72, 36, 18, 9, 4, 2, 1]

    for shp in shp_files:
        shp_file_name = shp[:-4]
        key_attribute = shp_file_name.split("_", maxsplit=2)
        print(shp)

        if key_attribute[0] == "point":
            arcpy.management.CreateFeatureDataset(f"{arcpy.env.workspace}", f"{shp_file_name}_temp",
                                                  spatial_reference=sr)
            arcpy.management.CreateFeatureDataset(final_gdb,
                                                  shp_file_name, spatial_reference=sr)
            arcpy.FeatureClassToFeatureClass_conversion(
                fr"{shape_path}\{shp}",
                fr"{arcpy.env.workspace}\{shp_file_name}_temp", shp_file_name)

            for scale in feature_scales:
                # Szétszedi a fájlt méretarányokként
                arcpy.Select_analysis(fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}",
                                      fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                      f"scale>={scale}")
                rows = arcpy.GetCount_management(fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}")
                num_rows = int(rows.getOutput(0))

                if num_rows != 0:
                    arcpy.Select_analysis(
                        fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                        fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}", )

        if key_attribute[0] == "line":
            print(key_attribute[1], "")

            create_temp_feature_dataset(shp_file_name, shp)

            if key_attribute[1] in Schemes.line_dissolve.keys():
                print("VONAL DISSOLVE")
                if key_attribute[1] == "railway" or key_attribute[1] == "highway":

                    arcpy.management.Dissolve(fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}",
                                              fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_bo_dissolve",
                                              *Schemes.line_dissolve[key_attribute[1]]["bo"])

                    arcpy.management.Dissolve(fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}",
                                              fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_szuk_dissolve",
                                              *Schemes.line_dissolve[key_attribute[1]]["szuk"])
                    for scale in feature_scales:
                        if scale > 36:
                            arcpy.Select_analysis(
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_szuk_dissolve",
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                f"scale>={scale}")
                            # TODO Merge fields
                        else:
                            arcpy.Select_analysis(
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_bo_dissolve",
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                f"scale>={scale}")

                else:
                    arcpy.management.Dissolve(fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}",
                                              fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_dissolve",
                                              *Schemes.line_dissolve[key_attribute[1]])

                    for scale in feature_scales:
                        arcpy.Select_analysis(
                            fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_dissolve",
                            fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                            f"scale>={scale}")

            if key_attribute[1] in Schemes.line_simplify.keys():
                if key_attribute[1] == "railway" or key_attribute[1] == "highway":
                    for scale in feature_scales:
                        if scale in Schemes.line_simplify[key_attribute[1]]:
                            print("simplify")
                            arcpy.cartography.SimplifyLine(
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                f"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp",
                                *Schemes.line_simplify[key_attribute[1]][scale])

                            arcpy.DeleteField_management(
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp",
                                Schemes.line_field_keep[key_attribute[1]][scale],
                                'KEEP_FIELDS')

                            rows = arcpy.GetCount_management(
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp")
                            num_rows = int(rows.getOutput(0))

                            if num_rows != 0:
                                arcpy.Select_analysis(
                                    fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp",
                                    fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                    f"Shape_Length > 0")
                        else:
                            rows = arcpy.GetCount_management(
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}")
                            num_rows = int(rows.getOutput(0))

                            if num_rows != 0:
                                arcpy.Select_analysis(
                                    fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                    fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                    f"Shape_Length > 0")

                else:
                    for scale in feature_scales:
                        if scale in Schemes.line_simplify[key_attribute[1]]:
                            arcpy.cartography.SimplifyLine(
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                f"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp",
                                *Schemes.line_simplify[key_attribute[1]][scale])

                            arcpy.DeleteField_management(
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp",
                                Schemes.line_field_keep[key_attribute[1]],
                                'KEEP_FIELDS')

                            rows = arcpy.GetCount_management(
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp")
                            num_rows = int(rows.getOutput(0))

                            if num_rows != 0:
                                arcpy.Select_analysis(
                                    fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp",
                                    fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                    f"Shape_Length > 0")

                        else:
                            rows = arcpy.GetCount_management(
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}")
                            num_rows = int(rows.getOutput(0))
                            if num_rows != 0:
                                arcpy.Select_analysis(
                                    fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                    fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                    f"Shape_Length > 0")

            else:
                for scale in feature_scales:
                    arcpy.Select_analysis(fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}",
                                          fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                          f"scale>={scale}")

                    rows = arcpy.GetCount_management(
                        fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}")
                    num_rows = int(rows.getOutput(0))

                    if num_rows != 0:
                        arcpy.Select_analysis(
                            fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                            fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                            f"Shape_Length > 0")

        if key_attribute[0] == "area":
            create_temp_feature_dataset(shp_file_name, shp)

            if key_attribute[1] == "landuse":
                arcpy.management.Dissolve(fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}",
                                          fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_dissolve",
                                          *Schemes.area_dissolve[key_attribute[1]])

                for scale in feature_scales:
                    # Szétszedi a fájlt méretarányokként
                    arcpy.Select_analysis(fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_dissolve",
                                          fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                          f"scale>={scale}")

                    if scale in Schemes.area_simplify[key_attribute[1]]:
                        print("ITT 2")
                        # Ha kell egyszerűsíti, simplify
                        arcpy.cartography.SimplifyPolygon(
                            fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                            f"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp",
                            *Schemes.area_simplify[key_attribute[1]][scale])

                        arcpy.DeleteField_management(
                            fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp",
                            Schemes.area_field_keep[key_attribute[1]],
                            'KEEP_FIELDS')

                        rows = arcpy.GetCount_management(
                            fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp")
                        num_rows = int(rows.getOutput(0))

                        if num_rows != 0:
                            if key_attribute[1] != "water":
                                try:
                                    arcpy.Select_analysis(
                                        fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp",
                                        fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                        f"Shape_Area > {Schemes.area_filter[scale]}")

                                except:
                                    arcpy.Select_analysis(
                                        fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp",
                                        fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                        f"Shape_Area > 0")
                            else:
                                try:
                                    arcpy.Select_analysis(
                                        fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp",
                                        fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                        f"Shape_Area > {Schemes.water_area_filter[scale]}")
                                except:
                                    arcpy.Select_analysis(
                                        fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}_simp",
                                        fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                        f"Shape_Area > 0")


                    else:
                        rows = arcpy.GetCount_management(
                            fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}")
                        num_rows = int(rows.getOutput(0))
                        if num_rows != 0:
                            if key_attribute[1] != "water":
                                try:
                                    arcpy.Select_analysis(
                                        fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                        fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                        f"Shape_Area > {Schemes.area_filter[scale]}")
                                except:
                                    arcpy.Select_analysis(
                                        fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                        fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                        f"Shape_Area > 0")
                            else:
                                try:
                                    arcpy.Select_analysis(
                                        fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                        fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                        f"Shape_Area > {Schemes.water_area_filter[scale]}")
                                except:
                                    arcpy.Select_analysis(
                                        fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                        fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                        f"Shape_Area > 0")

            else:
                for scale in feature_scales:
                    arcpy.Select_analysis(fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}",
                                          fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                          f"scale>={scale}")

                    rows = arcpy.GetCount_management(
                        fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}")
                    num_rows = int(rows.getOutput(0))

                    if num_rows != 0:
                        try:
                            arcpy.Select_analysis(
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                f"Shape_Area > {Schemes.area_filter[scale]}")

                        except:
                            arcpy.Select_analysis(
                                fr"{arcpy.env.workspace}\{shp_file_name}_temp\{shp_file_name}_{scale}",
                                fr"{final_gdb}\{shp_file_name}\{shp_file_name}_{scale}",
                                f"Shape_Area > 0")
