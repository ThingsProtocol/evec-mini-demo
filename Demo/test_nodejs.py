from Naked.toolshed.shell import execute_js, muterun_js

result = execute_js('device_management.js')

if result:
    print ("JavaScript is successfully executed")
else:
    print ("JavaScript is failed")