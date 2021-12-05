import docker
import config

client = docker.from_env()

def create_networks(app_config, containers):
    network_config = app_config['scenario']['network']
    ipam_pool = docker.types.IPAMPool(
        subnet = network_config['subnet'],
        gateway = network_config['gateway']
    )
    ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
    app_network = client.networks.create(
        name = config.PREFIX_IMAGE + "_app_network" + config.SUFFIX_CONTAINER,
        ipam = ipam_config
        )
    for container_config_name in containers:
        container_name = containers[container_config_name]
        app_network.connect(
            container = container_name,
            ipv4_address = app_config['scenario'][container_config_name]['private_ipv4_address']
        )
    return app_network

def kill_networks():
    networks = client.networks.list(
        names = [config.PREFIX_IMAGE + "_app_network"]
    )
    for network in networks:
        network.remove()
        print(f"Removing network {network.name}")
