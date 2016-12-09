import yaml


# For now we are just reading in the api/plugin definitions. Error checking and any format translation would happen here
class ConfigBuilder:
    def __init__(self, config_file_path):
        # Hard coded to a single file for now.
        f = open(config_file_path)
        self.desired_state = yaml.safe_load(f)
        if self.desired_state is None:
            self.desired_state = {}
        f.close()

    def get_desired_config(self):
        self.desired_state.setdefault('apis', {})
        self.desired_state.setdefault('plugins', {})
        return self.desired_state
