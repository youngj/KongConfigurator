
#Gennerates individual commands to migrate the current state of Kong to the state desired as specified in the config files.
class ConfigResolver:
    def __init__(self):
        pass

    def resolve(self, cur_state, desired_state):
        operations = []
        #Find any APIs we should delete from the current state and add a remove command.
        for api in cur_state:
            if api not in desired_state:
                operations.append({'command': 'DELETE_API', 'api_name': api})

        return operations
