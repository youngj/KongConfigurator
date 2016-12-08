import requests
import yaml

#Accepts commands to change the current state of Kong
class ConfigImplementor:
    def __init__(self):
        f = open('KongConfiguratorSettings.yaml')
        self.config = yaml.safe_load(f)
        f.close()

    #Process operations into specific commands and arguments
    def exec_operation(self, opperation):
        if opperation['command'] == "DELETE_API":
            print "Executing DELETE_API: " + opperation['api_name']
            return self._delete_api(opperation['api_name'])
        else:
            print "Operation Error"


    def _delete_api(self, api_name):
        resp = requests.delete(self.config['kong_admin_endpoint'] + '/apis/' + api_name)
        if resp.status_code != 204:
            print "Error"

        return "API " + api_name + " DELETED"
