#!/usr/bin/python3
import sys
import os
import logging
import configparser

SCRIPT_PATH = str(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = SCRIPT_PATH + "/dynamicScv.log"
CFG_FILE = SCRIPT_PATH + "/dynamicScv.cfg"
GCODE_CMD = "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY={SCV_VALUE} ;DynamicSCV({TYPE})\n"
DEFAULT_PROFILE_NAME = "default_profile"
PROFILE_NAME = ""
SRC_FILE_PATH = ""

# ;TYPE:Default <-- this type does not exist. But we need insert the fail-safe SCV value at the start of gcode.
# ;TYPE:Custom
# ;TYPE:Skirt/Brim
# ;TYPE:Perimeter
# ;TYPE:External perimeter
# ;TYPE:Solid infill
# ;TYPE:Support material
# ;TYPE:Overhang perimeter
# ;TYPE:Bridge infill
# ;TYPE:Internal infill
# ;TYPE:Top solid infill
# ;TYPE:Support material interface
lineTypes = {
    "default" : "TYPE:Default",
    "custom" : ";TYPE:Custom",
    "skirt_brim" : ";TYPE:Skirt/Brim",
    "perimeter" : ";TYPE:Perimeter",
    "external_perimeter" : ";TYPE:External perimeter",
    "solid_infill" : ";TYPE:Solid infill",
    "support_material" : ";TYPE:Support material",
    "overhang_perimeter" : ";TYPE:Overhang perimeter",
    "bridge_infill" : ";TYPE:Bridge infill",
    "internal_infill" : ";TYPE:Internal infill",
    "top_solid_infill" : ";TYPE:Top solid infill",
    "support_material_interface" : ";TYPE:Support material interface"
}

#OUTPUT_FILE_PATH = str(os.getenv('SLIC3R_PP_OUTPUT_NAME'))

# delete old log file
try:
    os.remove(LOG_FILE)
except Exception as e:
    print(str(e))

logger =  logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
loggerFileHandler = logging.FileHandler(LOG_FILE)
loggerFileHandler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
loggerStreamHandler = logging.StreamHandler()
loggerStreamHandler.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
logger.addHandler(loggerFileHandler)
logger.addHandler(loggerStreamHandler)

if len(sys.argv) > 2:
    if "profile=" in sys.argv[1]:
        PROFILE_NAME = sys.argv[1].replace("profile=","")
        SRC_FILE_PATH=sys.argv[2]
    else:
        logger.error("Config file is empty")
        sys.exit(1)
else:
    SRC_FILE_PATH=sys.argv[1]
    PROFILE_NAME = DEFAULT_PROFILE_NAME

logger.info("Source file : %s",SRC_FILE_PATH)
logger.info("Profile : %s",PROFILE_NAME)

config = configparser.ConfigParser(delimiters=(':','='))
try:
    config.read(CFG_FILE)
    if len(config.sections()) ==0:
        logger.error("Config file is empty")
        sys.exit(1)
    
    if PROFILE_NAME not in config.sections():
        logger.error("Invalid config file! Missing config for [" + PROFILE_NAME + "] profile.")
        sys.exit(1)

    for key, _ in lineTypes.items():
        if key not in config[PROFILE_NAME]:
            logger.error("Invalid config file! Missing %s config.",key)
            sys.exit(1)
            
except Exception as e:
    logging.error(str(e))
    sys.exit(1)


srcGcode = []
try:
    with open(SRC_FILE_PATH, mode='r', encoding='UTF-8') as srcFile:
        srcGcode = srcFile.readlines()
        srcFile.close()
except Exception as e:
    logging.error(str(e))
    sys.exit(1)

if len(srcGcode) == 0:
    logging.error("Source file is empty!")
    sys.exit(1)

logger.debug("Source gcode line count : %s",len(srcGcode))

modifiedGcode = []
# insert default SCV at the start of gcode
modifiedGcode.append(GCODE_CMD.replace("{SCV_VALUE}",config[PROFILE_NAME]["default"]).replace("{TYPE}","default"))
for line in srcGcode:
    for key, value in lineTypes.items():
        if line.startswith(value):
            modifiedGcode.append(GCODE_CMD.replace("{SCV_VALUE}",config[PROFILE_NAME][key]).replace("{TYPE}",key))
            break
    modifiedGcode.append(line)

# overwrite the tmp file
try:
    with open(SRC_FILE_PATH, mode='w', encoding='UTF-8') as outputFile:
    #with open(SCRIPT_PATH + "/output.gcode", mode='w', encoding='UTF-8') as outputFile:
        outputFile.writelines(modifiedGcode)
        outputFile.close()
    sys.exit(0)
except Exception as e:
    logging.error(str(e))
    sys.exit(1)
