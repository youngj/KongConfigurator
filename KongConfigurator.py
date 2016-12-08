from KongStateBuilder import KongStateBuilder
from ConfigBuilder import ConfigBuilder
from ConfigResolver import ConfigResolver
from ConfigImplementor import ConfigImplementor
import sys

#Get the current state of running instance of Kong
kongStateBuilder = KongStateBuilder()
kong_state = kongStateBuilder.buildState()
print "KONG_STATE:" + str(kong_state)

#Generate a Kong configuration as described by our YAML config files
configBuilder = ConfigBuilder()
config_state = configBuilder.get_desired_config()
print "CONFIG_STATE:" + str(config_state)

#Resolve the state desired as specified in our config YAML with the current state of Kong into a list of operations
#To transform the current state to the desired state.
configResolver = ConfigResolver()
operations = configResolver.resolve(kong_state, config_state)

if len(operations) > 0:
    print "The following changes will be made to Kong."
    for op in operations:
        #TODO:Format this output
        print op
    print "Apply proposed changes? [y/n]"
    choice = raw_input()
    if choice == 'n':
        sys.exit(0)
else:
    print "Desired and current states match!"
    sys.exit(0)

#Transform the current state to the desired state one operation at a time.
configImplementor = ConfigImplementor()
for operation in operations:
    print configImplementor.exec_operation(operation)
