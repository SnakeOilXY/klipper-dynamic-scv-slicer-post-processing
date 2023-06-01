import os

SRC_FILE_PATH = str(os.path.dirname(os.path.abspath(__file__))) + "/sample.gcode"

try:
    with open(SRC_FILE_PATH, mode='r', encoding='UTF-8') as srcFile:
        srcGcode = srcFile.readlines()
        srcFile.close()

        typeArr = []
        for line in srcGcode:
            if line.startswith(";TYPE:"):
                if line not in typeArr:
                    typeArr.append(line)
        
        for lineType in typeArr:
            print(lineType)
except Exception as e:
    print(str(e))

print("end")