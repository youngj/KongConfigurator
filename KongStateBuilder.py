import requests
import yaml


# Builds a local representation of the current state of our Kong instance.
class KongStateBuilder:
    def __init__(self):
        f = open('KongConfiguratorSettings.yaml')
        self.config = yaml.safe_load(f)
        f.close()

    def build_state(self):
        local_rep = {'apis': {}, 'plugins': {}}
        # Build enpoints state
        resp = requests.get(self.config['kong_admin_endpoint'] + '/apis/')
        if resp.status_code != 200:
            raise Exception("GET_APIS Failed: " + str(resp.status_code))

        content = resp.json()
        if 'data' not in content:
            raise ValueError("Kong Error")

        for api in content['data']:
            api['plugins'] = []
            local_rep['apis'][api['name']] = api

        # Build Plugins state for each api we got in the step above
        for api in local_rep['apis']:
            resp = requests.get(self.config['kong_admin_endpoint'] + '/apis/' + api + '/plugins')
            if resp.status_code != 200:
                raise Exception("GET_PLUGINS Failed: " + str(resp.status_code))

            content = resp.json()
            if 'data' not in content:
                raise ValueError("Kong Error")
            local_rep['plugins'].setdefault(api, {})
            for data in content['data']:
                local_rep['plugins'][api][data['name']] = data

        return local_rep
