# KongConfigurator

Usage:

Setup:
activate your virtualenv.
run: pip install -r requirements.txt in your shell.
Set Kong Admin Endpoint in KongConfiguratorSettings.yaml

Execution:
activate your virtualenv.
python KongConfigurator.py [Path to configuration.yaml]

You will be prompted with a list of proposed changes. If you enter 'y' to accept the changes, they will be applied to
the Kong admin api specified in KongConfiguratorSettings.yaml.

Example configuration YAML:
apis:
    foo:
        name: foo
        upstream_url: http://foo.com/
        request_host: foo.com
    mockbin:
        name: mockbin
        upstream_url: http://mockbin.com/
        request_host: mockbin.com

plugins:
    foo:
        rate-limiting:
            config.hour: 10000
            config.second: 5
        key-auth:
            config.key_names: ['apikey']

There are two main sections, apis and plugins. Apis simply specify the name and configuration settings.
The plugins section first specifies which api the section is applicable to, then the configuration details of the
plugin are provided.

Future Improvements:
    Unit testing. The ConfigResolver.py is especially well situated for unit testing as it receives two local data
    structures and results are easily verify by looking at the operations it returns.

    Proper logging.

    Implement retry logic.

    Refactor ConfigResolver.py: split apis and plugins into two different structures.

    Only parse KongConfiguratorSettings.yaml settings once.

    Handle Update of plugins.

    Handle consumers.

    Tripwires to add additional user conformation for unlikely operations. ie: delete everything.

    Sort operations by parent/child before applying them. ie. Don't bother updating a plugin on a api that is being
    deleted.

    Potentially support multiple config files although there are several issues. One is risk that if a file is missing
    from a run for whatever reason, all configurations that it implemented will be deleted.
    Another case to handle would be the issues of multiple instances of configuration for the same api or plugin.
    A mitigation strategy would be to ensure we always process the files in the same order so at least there won't
    be any random behavior and the last duplicate to be executed will always be the applied state.