class Schemes:
    area_filter = {2311: 5000000,
                   1155: 4500000,
                   577: 2000000,
                   288: 350000,
                   }

    landuse_area_dissolve = [["name", "landuse", "scale"], "", "SINGLE_PART", "DISSOLVE_LINES"]
    water_area_dissolve = [["name","water", "scale"], "", "SINGLE_PART", "DISSOLVE_LINES"]
    boundary_area_dissolve = [["name","boundary","admin_leve","scale"], "", "SINGLE_PART", "DISSOLVE_LINES"]
    military_area_dissolve = [["name","military","scale"], "", "SINGLE_PART", "DISSOLVE_LINES"]
    natural_area_dissolve = [["name","natural","scale"], "", "SINGLE_PART", "DISSOLVE_LINES"]


    water_area_filter = {2311: 3000000,
                   1155: 2250000,
                   577: 1000000,
                   288: 350000,
                   }

    landuse_area_simplify = {2311: ['BEND_SIMPLIFY', "1 Kilometers", "2 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                        1155: ['BEND_SIMPLIFY', "1 Kilometers", "1 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                        577: ['BEND_SIMPLIFY', "750 Meters", "1 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                        288: ['BEND_SIMPLIFY', "500 Meters", "0,3 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                        144: ['BEND_SIMPLIFY', "250 Meters", "0,05 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                        72: ['BEND_SIMPLIFY', "100 Meters", "0 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP']}

    water_area_simplify = {2311: ['BEND_SIMPLIFY', "1 Kilometers", "2 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                             1155: ['BEND_SIMPLIFY', "1 Kilometers", "1 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                             577: ['BEND_SIMPLIFY', "750 Meters", "1 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                             288: ['BEND_SIMPLIFY', "500 Meters", "0,3 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                             144: ['BEND_SIMPLIFY', "250 Meters", "0,05 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                             72: ['BEND_SIMPLIFY', "100 Meters", "0 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP']}

    boundary_area_simplify = {2311: ['BEND_SIMPLIFY', "1 Kilometers", "2 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                           1155: ['BEND_SIMPLIFY', "1 Kilometers", "1 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                           577: ['BEND_SIMPLIFY', "750 Meters", "1 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                           288: ['BEND_SIMPLIFY', "500 Meters", "0,3 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                           }

    military_area_simplify = {
        2311: ['BEND_SIMPLIFY', "1 Kilometers", "2 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
        1155: ['BEND_SIMPLIFY', "1 Kilometers", "1 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
        577: ['BEND_SIMPLIFY', "750 Meters", "1 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
        288: ['BEND_SIMPLIFY', "500 Meters", "0,3 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
        }

    natural_area_simplify = {2311: ['BEND_SIMPLIFY', "1 Kilometers", "2 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                           1155: ['BEND_SIMPLIFY', "1 Kilometers", "1 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                           577: ['BEND_SIMPLIFY', "750 Meters", "1 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                           288: ['BEND_SIMPLIFY', "500 Meters", "0,3 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                           144: ['BEND_SIMPLIFY', "250 Meters", "0,05 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP'],
                           72: ['BEND_SIMPLIFY', "100 Meters", "0 SquareKilometers", 'RESOLVE_ERRORS', 'NO_KEEP']}

    landuse_area_field_keep = ["name", "landuse", "scale"]

    area_dissolve = {"landuse": landuse_area_dissolve,
                     "water": water_area_dissolve,
                     "boundary": boundary_area_dissolve,
                     "military": military_area_dissolve,
                     "natural": natural_area_dissolve,
                     }

    area_simplify = {"landuse": landuse_area_simplify,
                     "water": water_area_simplify,
                     "boundary": boundary_area_simplify,
                     "military": military_area_simplify,
                     "natural": natural_area_simplify
                     }

    area_field_keep={"landuse":["name", "landuse", "scale"],
                     "water": ["name","water","scale"],
                     "boundary": ["name","boundary","admin_leve","scale"],
                     "military": ["name","military","scale"],
                     "natural": ["name","natural","scale"],



    }



    railway_line_dissolve = {
        "szuk": [["name","railway","usage","service","scale","mergeType"],"","SINGLE_PART", "DISSOLVE_LINES"],
        "bo": [["name","railway","usage","service","scale","tunnel","bridge","mergeType"],"","SINGLE_PART", "DISSOLVE_LINES"],

    }

    railway_line_simplify = {
        2311: ['POINT_REMOVE', "350 Meters", 'RESOLVE_ERRORS', 'NO_KEEP'],
        1155: ['POINT_REMOVE', "200 Meters", 'RESOLVE_ERRORS', 'NO_KEEP'],
        577: ['POINT_REMOVE', "100 Meters", 'RESOLVE_ERRORS', 'NO_KEEP'],
        288: ['POINT_REMOVE', "20 Meters", 'RESOLVE_ERRORS', 'NO_KEEP'],

    }
    railway_line_field_keep = {
        2311:["name", "railway", "scale","usage","service"],
        1155:["name", "railway", "scale","usage","service"],
        577:["name", "railway", "scale","usage","service"],
        288:["name", "railway", "scale","usage","service"],
        144:["name", "railway", "scale","usage","service"],
        72:["name", "railway", "scale","usage","service"],
    }

    highway_line_dissolve = {
        "szuk": [["name", "highway", "ref", "scale"], "", "SINGLE_PART", "DISSOLVE_LINES"],
       "bo": [["name", "highway", "ref", "scale", "tunnel", "bridge"], "", "SINGLE_PART", "DISSOLVE_LINES"],


    }
    highway_line_simplify = {
        2311: ['POINT_REMOVE', "350 Meters", 'RESOLVE_ERRORS', 'NO_KEEP'],
        1155: ['POINT_REMOVE', "200 Meters", 'RESOLVE_ERRORS', 'NO_KEEP'],
        577: ['POINT_REMOVE', "100 Meters", 'RESOLVE_ERRORS', 'NO_KEEP'],
        288: ['POINT_REMOVE', "20 Meters", 'RESOLVE_ERRORS', 'NO_KEEP'],

    }
    highway_line_field_keep = {
        2311: ["name", "highway", "ref", "scale"],
        1155: ["name", "highway", "ref", "scale"],
        577: ["name", "highway", "ref", "scale"],
        288: ["name", "highway", "ref", "scale"],
        144: ["name", "highway", "ref", "scale"],
        72: ["name", "highway", "ref", "scale"],
    }
    aerialway_line_dissolve = [["name", "aerialway", "scale"], "", "SINGLE_PART", "DISSOLVE_LINES"]
    barrier_line_dissolve = [["name", "barrier", "scale"], "", "SINGLE_PART", "DISSOLVE_LINES"]
    cycleway_line_dissolve = [["name", "bridge","tunnel","cycleway", "scale"], "", "SINGLE_PART", "DISSOLVE_LINES"]
    man_made_line_dissolve = [["name", "man_made", "scale"], "", "SINGLE_PART", "DISSOLVE_LINES"]
    natural_line_dissolve = [["name", "natural", "scale"], "", "SINGLE_PART", "DISSOLVE_LINES"]
    power_line_dissolve = [["name", "power", "scale"], "", "SINGLE_PART", "DISSOLVE_LINES"]
    waterway_line_dissolve = [["name", "waterway", "scale"], "", "SINGLE_PART", "DISSOLVE_LINES"]

    line_dissolve = {
        "aerialway": aerialway_line_dissolve,
        "barrier": barrier_line_dissolve,
        "cycleway": cycleway_line_dissolve,
        "highway": highway_line_dissolve,
        "man_made": man_made_line_dissolve,
        "natural": natural_line_dissolve,
        "power": power_line_dissolve,
        "railway": railway_line_dissolve,
        "waterway": waterway_line_dissolve,
                     }
    global_line_simplify = {
        2311: ['POINT_REMOVE', "350 Meters", 'RESOLVE_ERRORS', 'NO_KEEP'],
        1155: ['POINT_REMOVE', "200 Meters", 'RESOLVE_ERRORS', 'NO_KEEP'],
        577: ['POINT_REMOVE', "100 Meters", 'RESOLVE_ERRORS', 'NO_KEEP'],
        288: ['POINT_REMOVE', "20 Meters", 'RESOLVE_ERRORS', 'NO_KEEP'],

    }
    line_simplify = {
        "aerialway":global_line_simplify,
        "barrier":global_line_simplify,
        "cycleway":global_line_simplify,
        "highway":global_line_simplify,
        "man_made":global_line_simplify,
        "natural":global_line_simplify,
        "power":global_line_simplify,
        "railway":global_line_simplify,
        "waterway":global_line_simplify,
    }

    line_field_keep = {"aerialway": ["name", "aerialway", "scale"],
                       "aeroway": ["name", "aeroway", "scale"],
                       "barrier": ["name", "barrier","scale"],
                       "cycleway": ["name", "bridge", "tunnel","cycleway","scale"],
                       "highway": highway_line_field_keep,
                       "historic": ["name", "historic", "scale"],
                       "man_made": ["name", "man_made", "scale"],
                       "natural": ["name", "natural", "scale"],
                       "power": ["name", "power", "scale"],
                       "railway": railway_line_field_keep,
                       "waterway": ["name", "waterway", "scale"],

                       }

