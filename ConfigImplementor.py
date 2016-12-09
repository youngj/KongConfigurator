import requests
import yaml


# Accepts commands to change the current state of Kong
class ConfigImplementor:
    def __init__(self):
        f = open('KongConfiguratorSettings.yaml')
        self.config = yaml.safe_load(f)
        f.close()

    # Process operations into specific commands and arguments
    def exec_operation(self, operation):
        if operation['command'] == "DELETE_API":
            print "Executing DELETE_API: " + operation['api_name']
            return self._delete_api(operation['api_name'])
        if operation['command'] == "ADD_API":
            print "Executing ADD_API: " + operation['opts']['name']
            return self._add_api(operation['opts'])
        if operation['command'] == "UPDATE_API":
            print "Executing ADD_API: " + operation['opts']['name']
            return self._update_api(operation['opts'])
        if operation['command'] == "ADD_PLUGIN":
            print "Executing ADD_PLUGIN: " + operation['opts']['name']
            return self._add_plugin(opts=operation['opts'], api_name=operation['api_name'])
        if operation['command'] == "DELETE_PLUGIN":
            print "Executing DELETE_PLUGIN: " + operation['plugin_id']
            return self._delete_plugin(api_name=operation['api_name'], plugin_id=operation['plugin_id'])
        else:
            raise Exception("No command matching command found.")

    def _delete_api(self, api_name):
        resp = requests.delete(self.config['kong_admin_endpoint'] + '/apis/' + api_name)
        if resp.status_code != 204:
            raise Exception("DELETE_API Failed: " + str(resp.status_code))

        return "API " + api_name + " DELETED"

    def _add_api(self, opts):
        resp = requests.put(self.config['kong_admin_endpoint'] + '/apis/', data=opts)
        if resp.status_code != 201:
            raise Exception("ADD_API Failed: " + str(resp.status_code))

        return resp.json()

    def _update_api(self, opts):
        resp = requests.patch(self.config['kong_admin_endpoint'] + '/apis/' + opts['name'], data=opts)
        if resp.status_code != 200:
            raise Exception("UPDATE_API Failed: " + str(resp.status_code))

        return resp.json()

    def _add_plugin(self, opts, api_name):
        resp = requests.put(self.config['kong_admin_endpoint'] + '/apis/' + api_name + '/plugins', data=opts)
        if resp.status_code != 201:
            raise Exception("ADD_PLUGIN Failed: " + str(resp.status_code))

        return resp.json()

    def _delete_plugin(self, api_name, plugin_id):
        resp = requests.delete(self.config['kong_admin_endpoint'] + '/apis/' + api_name + '/plugins/' + plugin_id)
        if resp.status_code != 204:
            raise Exception("DELETE_PLUGIN Failed: " + str(resp.status_code))

        return "API " + plugin_id + " DELETED"
