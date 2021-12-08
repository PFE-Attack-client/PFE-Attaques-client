from subprocess import check_output
import os.path

## Create a new empty config_env.js file 
if os.path.isfile('config_env.js') == True:
    os.remove('config_env.js')
file = open('config_env.js', 'x')

## store outputs of 'env' com in all_env list
all_env = check_output("env").decode("utf-8").splitlines()

## Create new list which will contain "VUE" related env variables with name and value
vue_env = []

## Create new list which will contain "VUE" related env variable with only the name
vue_env_name = []

## Only keep "VUE" related environment variables
for el in all_env:
    if el.find('VUE') == 0:
        vue_env_name.append(el.split("=")[0])
        vue_env.append(el.split("=")[0] + ' = ' + '"' + el.split('=')[1] + '"')
        
## Fill the config_env.js file 
ind = '    '
file.write('export const getEnv = () => {')
file.write('\n')

for ol in vue_env:
    file.write(ind + 'const ' + ol)
    file.write('\n')

file.write(ind + 'return {')
file.write('\n')

for ol in vue_env_name:
    file.write(ind + ind + ol + ' : ' + ol + ',')
    file.write('\n')

file.write(ind + '}')
file.write('\n')
file.write('}')
        