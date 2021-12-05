import config
import docker
from network_manager import kill_networks

client = docker.from_env()

def kill_container(image_name):
    containers = client.containers.list(
        filters = {
            "status": "running",
            "ancestor": image_name
        }
    )
    for container in containers:
        print(f"Removing container: {container.name} done")
        container.remove(force=True)

def clean():
        services = config.SERVICES
        for service in services:
            kill_container(services[service]["IMAGE_NAME"])
        kill_networks()

def from_dic_to_env(object):
    env_list = []
 
    for key, value in object.items():
        env_list.append(str(key).upper() + "=" + str(value))
    return(env_list)
    