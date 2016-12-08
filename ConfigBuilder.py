import yaml

#For now we are just reading in the api/plugin definitions. Error checking and any format translation would happen here.
class ConfigBuilder:
    def __init__(self):
        #Hard coded to a single file for now.
        f = open('test_config.yaml')
        self.desired_state = yaml.safe_load(f)
        f.close()

    def get_desired_config(self):
        return self.desired_state