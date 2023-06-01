import re
from ..Script import Script


class DynamicScv(Script):

    def getSettingDataString(self):
        return """{
            "name": "Dynamic Square Corner Velocity",
            "key": "DynamicScv",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "enable_dynamic_scv":
                {
                    "label": "Enable",
                    "description": "Enable dynamic Square Corner Velocity",
                    "type": "bool",
                    "default_value": true
                },
                "default_scv":
                {
                    "label": "    Default SCV",
                    "description": "Default Square Corner Velocity",
                    "type": "int",
                    "default_value": 5,
                    "minimum_value": "1",
                    "maximum_value" : "100",
                    "enabled": "enable_dynamic_scv"
                },
                "skirt_scv":
                {
                    "label": "    Skirt/brim SCV",
                    "description": "Skirt/brim Square Corner Velocity",
                    "type": "int",
                    "default_value": 5,
                    "minimum_value": "1",
                    "maximum_value" : "100",
                    "enabled": "enable_dynamic_scv"
                },
                "outer_wall_scv":
                {
                    "label": "    Outer wall SCV",
                    "description": "Outer wall Square Corner Velocity",
                    "type": "int",
                    "default_value": 5,
                    "minimum_value": "1",
                    "maximum_value" : "100",
                    "enabled": "enable_dynamic_scv"
                },
                "inner_wall_scv":
                {
                    "label": "    Inner wall SCV",
                    "description": "Inner wall Square Corner Velocity",
                    "type": "int",
                    "default_value": 10,
                    "minimum_value": "1",
                    "maximum_value" : "100",
                    "enabled": "enable_dynamic_scv"
                },
                "skin_scv":
                {
                    "label": "    Skin SCV",
                    "description": "Skin Square Corner Velocity",
                    "type": "int",
                    "default_value": 15,
                    "minimum_value": "1",
                    "maximum_value" : "100",
                    "enabled": "enable_dynamic_scv"
                },
                "infill_scv":
                {
                    "label": "    Infill SCV",
                    "description": "Infill Square Corner Velocity",
                    "type": "int",
                    "default_value": 20,
                    "minimum_value": "1",
                    "maximum_value" : "100",
                    "enabled": "enable_dynamic_scv"
                },
                "support_scv":
                {
                    "label": "    Support SCV",
                    "description": "Support Square Corner Velocity",
                    "type": "int",
                    "default_value": 10,
                    "minimum_value": "1",
                    "maximum_value" : "100",
                    "enabled": "enable_dynamic_scv"
                },
                "support_interface_scv":
                {
                    "label": "    Support interface SCV",
                    "description": "Support interface Square Corner Velocity",
                    "type": "int",
                    "default_value": 10,
                    "minimum_value": "1",
                    "maximum_value" : "100",
                    "enabled": "enable_dynamic_scv"
                }
            }
        }"""

    def execute(self, data):
        enable_dynamic_scv = self.getSettingValueByKey("enable_dynamic_scv")
        default_scv = self.getSettingValueByKey("default_scv")
        outer_wall_scv = self.getSettingValueByKey("outer_wall_scv")
        inner_wall_scv = self.getSettingValueByKey("inner_wall_scv")
        skin_scv = self.getSettingValueByKey("skin_scv")
        infill_scv = self.getSettingValueByKey("infill_scv")
        skirt_scv = self.getSettingValueByKey("skirt_scv")
        support_scv = self.getSettingValueByKey("support_scv")
        support_interface_scv = self.getSettingValueByKey("support_interface_scv")

        for layerNumber, layerData in enumerate(data):            
            if enable_dynamic_scv:
                lines = data[layerNumber].split("\n")
                for lineNumber,lineData in enumerate(lines):
                    if lineData.startswith(";TYPE:FILL"):
                        lines[lineNumber] = lineData + "\n" + "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=" + str(infill_scv)
                    elif lineData.startswith(";TYPE:WALL-INNER"):
                        lines[lineNumber] = lineData + "\n" + "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=" + str(inner_wall_scv)
                    elif lineData.startswith(";TYPE:WALL-OUTER"):
                        lines[lineNumber] = lineData + "\n" + "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=" + str(outer_wall_scv)
                    elif lineData.startswith(";TYPE:SKIN"):
                        lines[lineNumber] = lineData + "\n" + "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=" + str(skin_scv)
                    elif lineData.startswith(";TYPE:SKIRT"):
                        lines[lineNumber] = lineData + "\n" + "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=" + str(skirt_scv)
                    elif lineData.startswith(";TYPE:SUPPORT"):
                        lines[lineNumber] = lineData + "\n" + "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=" + str(support_scv)
                    elif lineData.startswith(";TYPE:SUPPORT-INTERFACE"):
                        lines[lineNumber] = lineData + "\n" + "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=" + str(support_interface_scv)
                    elif lineData.startswith(";TYPE:") or lineData.startswith(";LAYER:"):
                        lines[lineNumber] = lineData + "\n" + "SET_VELOCITY_LIMIT SQUARE_CORNER_VELOCITY=" + str(default_scv)
                    else:
                        continue
                    
                data[layerNumber] = "\n".join(lines)

        return data



# ;TYPE:WALL-INNER
# ;TYPE:WALL-OUTER
# ;TYPE:SKIN
# ;TYPE:FILL
# ;TYPE:SUPPORT-INTERFACE
# ;TYPE:SKIRT
# ;TYPE:SUPPORT
