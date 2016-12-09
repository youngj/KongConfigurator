
# Generates individual commands to migrate the current state of Kong to the state desired as specified in the config
class ConfigResolver:
    def __init__(self):
        pass

    def resolve(self, cur_state, desired_state):
        operations = []
        # APIS
        # Find any APIs we should delete from the current state and add a remove command.
        for api in cur_state['apis']:
            if api not in desired_state['apis']:
                operations.append({'command': 'DELETE_API', 'api_name': api})

        # Find any APIs that are in the desired state but not currently running on Kong.
        for api in desired_state['apis']:
            if api not in cur_state['apis']:
                operations.append({'command': 'ADD_API', 'opts': desired_state['apis'][api]})

        # Check all the APIs options to see which ones might need updates
        for api, api_value in desired_state['apis'].iteritems():
            for opt, opt_value in api_value.iteritems():
                # TODO If this opt is missing bad things will happen.
                if api in cur_state['apis'] and cur_state['apis'][api][opt] != opt_value:
                    operations.append({'command': 'UPDATE_API', 'opts': {'name': api, opt: opt_value},
                                       'original_state': cur_state['apis'][api][opt]})

        # PLUGINS
        # Check all apis for plugins in the current state that are not in the desired state
        for api, api_value in cur_state['plugins'].iteritems():
            for plugin_name, plugin_value in api_value.iteritems():
                if api not in desired_state['plugins'] or plugin_name not in desired_state['plugins'][api]:
                    operations.append({'command': 'DELETE_PLUGIN', 'api_name': api, 'plugin_id': plugin_value['id'],
                                       'plugin_name': plugin_value['name']})

        # Check all apis for plugins in the desired state that are not in the current state
        for api, api_value in desired_state['plugins'].iteritems():
            for plugin_name, api_plugin in api_value.iteritems():
                if api not in cur_state['plugins'] or plugin_name not in cur_state['plugins'][api]:
                    api_plugin['name'] = plugin_name
                    operations.append({'command': 'ADD_PLUGIN', 'opts': api_plugin, 'api_name': api})
        return operations
