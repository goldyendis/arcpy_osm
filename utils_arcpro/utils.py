import glob
import pathlib
from datetime import date

base_project_location = r"D:\Baga\egyeb\alapterkep_pyrosm\OSM_TO_MTSZ\Arcpro"
project_file_location = r"d:\Baga\egyeb\alapterkep_pyrosm\OSM_TO_MTSZ\Arcpro\Alapterkep_new.aprx"
base_gdb = "Alapterkep.gdb"
# shp_location = r"d:\Baga\egyeb\alapterkep_pyrosm\OSM_TO_MTSZ\pyrosm_test\budapest"
# shp_location = r"d:\Baga\egyeb\alapterkep_pyrosm\OSM_TO_MTSZ\pyrosm_test\budapest\test"
shp_location = r"d:\Baga\egyeb\alapterkep_pyrosm\OSM_TO_MTSZ\pyrosm_test\orszag_test"
shp_files = [pathlib.Path(i).name for i in glob.glob(fr"{shp_location}\*.shp")]
coordinate_system = '''PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",
                        GEOGCS["GCS_WGS_1984",
                        DATUM["D_WGS_1984",
                        SPHEROID["WGS_1984",6378137.0,298.257223563]],
                        PRIMEM["Greenwich",0.0],
                        UNIT["Degree",0.0174532925199433]],
                        PROJECTION["Mercator_Auxiliary_Sphere"],
                        PARAMETER["False_Easting",0.0],
                        PARAMETER["False_Northing",0.0],
                        PARAMETER["Central_Meridian",0.0],
                        PARAMETER["Standard_Parallel_1",0.0],
                        PARAMETER["Auxiliary_Sphere_Type",0.0],
                        UNIT["Meter",1.0]],
                        '-20037700 -30241100 10000;#;#;0.001;#;#;IsHighPrecision'
                        '''
extra_features = ["kistajak.shp","kozeptajak.shp","nagytajak.shp","country_border.shp"]