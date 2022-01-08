from subprocess import check_output
import os.path

## Function that adds CSP Headers in "index.html"
def indexHeaders(params):
    index = open('../index.html')
    lines = index.readlines()
    index.close()
    index = open('../index.html', 'w')
    for line in lines:
        index.write(line)
        if line == '  <head>\n':
            index.write('    <meta\n')
            index.write('      http-equiv="Content-Security-Policy"\n')
            index.write('      content="script-src \'sefl\'; ' + params + '"/>\n')

## Create a new empty config_env.js file 
if os.path.isfile('config_env.js') == True:
    os.remove('config_env.js')
conf = open('config_env.js', 'x')

## store outputs of 'env' com in all_env list
all_env = check_output("env").decode("utf-8").splitlines()

## Create new list which will contain "VUE" related env variables with name and value
vue_env = []

## Create new list which will contain "VUE" related env variable with only the name
vue_env_name = []

## Boolean that will contain whether a CSP rule must be written or not
csp = False

## Only keep "VUE" related environment variables
for el in all_env:
    if el.find('VUE') == 0:
        vue_env_name.append(el.split("=")[0])
        if el.split("=")[0] == 'VUE_CSP' and el.split('=')[1] == 'true':
            csp = True
        if el.split("=")[0] == 'VUE_CSP_DIRECTIVE' and csp == True:
            indexHeaders(el.split("=")[1])
        vue_env.append(el.split("=")[0] + ' = ' + '"' + el.split('=')[1] + '"')
        
## Fill the config_env.js file
ind = '    '
conf.write('export const getEnv = () => {\n')

for ol in vue_env:
    conf.write(ind + 'const ' + ol + '\n')

conf.write(ind + 'return {\n')

for ol in vue_env_name:
    conf.write(ind + ind + ol + ' : ' + ol + ',\n')

conf.write(ind + '}\n')
conf.write('}')
    
conf.close()
index.close()