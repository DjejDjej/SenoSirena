import json
def loadjson(file_path): 

    with open(file_path, 'r') as file:
        loadedjson = json.load(file)

    return loadedjson

#Returns config file
def loadcfg():
    return loadjson("cfg/settings.json")
config = loadcfg()



def clearLogs(file_path):
    limit = config["logsLineDeletion"]
    if(config["logAutoDeletion"] == True):

        try:
            with open(file_path, 'r') as file:
                # Read all lines into a list
                lines = file.readlines()

                # Count the number of lines
                num_lines = len(lines)
                if(num_lines >= limit):
                    with open(file_path, 'w') as file:
                        pass   



        except Exception as e:
            print(f"An error occurred: {e}")
