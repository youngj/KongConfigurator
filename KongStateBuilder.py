import requests
import yaml

#Builds a local representation of the current state of our Kong instance.
class KongStateBuilder:
    def __init__(self):
        f = open('KongConfiguratorSettings.yaml')
        self.config = yaml.safe_load(f)
        f.close()

    def buildState(self):
        local_rep = {}
        #Build enpoints state
        resp = requests.get(self.config['kong_admin_endpoint'] + '/apis/')
        if resp.status_code != 200:
            raise ApiError(resp.status_code)

        content = resp.json()
        if 'data' not in content:
            print "Kong Error"

        for api in content['data']:
            api['plugins'] = []
            local_rep[api['name']] = api

        #Build Plugins state
        for api in local_rep:
            local_api = local_rep[api]
            resp = requests.get(self.config['kong_admin_endpoint'] + '/apis/' + local_api['name'] + '/plugins')
            if resp.status_code != 200:
                raise ApiError(resp.status_code)

            content = resp.json()
            if 'data' not in content:
                print "Kong Error"
            local_api['plugins'] = content['data']

        return local_rep