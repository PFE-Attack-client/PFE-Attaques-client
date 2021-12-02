import docker
import os
import argparse
import json
import pathlib
import sys

ABSOLUTE_PATH = str(pathlib.Path(__file__).parent.resolve())
PATH_SCENARIOS = ABSOLUTE_PATH + "/scenarios/"
PATH_PLATFORM = ABSOLUTE_PATH + "/platform/my-vuln-app/"
PATH_DOCKERFILE_DB = PATH_PLATFORM + "bdd/"
PATH_DOCKERFILE_CLIENT = PATH_PLATFORM + "client/"
PATH_DOCKERFILE_SERVER = PATH_PLATFORM + "server/"
PATH_DOCKERFILE_BOT = PATH_PLATFORM + "bot-victim/"
PREFIX_IMAGE = "pfe_sm_lns"
IMAGE_NAME_DB = PREFIX_IMAGE + "_database"
IMAGE_NAME_SERVER = PREFIX_IMAGE + "_server"
IMAGE_NAME_CLIENT = PREFIX_IMAGE + "_client"
IMAGE_NAME_BOT = PREFIX_IMAGE + "_bot"
SUFFIX_CONTAINER = str(os.getpid())

client = docker.from_env()

class Platform_manager:
    """Manager the container depending on the configuration input"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "config_file":
                self.load_config_from_file(value)
            if key == "scenario_name":
                self.load_config_from_file(PATH_SCENARIOS +  value + ".json")

    def load_config_from_file(self, config_file):
        try:
            with open(config_file) as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"File {config_file} can not be opened. Error:\n{e}")
            sys.exit(1)
    
    def run(self):
        self.build_images()
        self.launch_database()
        self.launch_server()
        self.launch_client()
        self.launch_bot()
        self.create_networks()
        self.config_db(self.server_container)
        self.init_server(self.server_container)

    def build_images(self):
        print("---- Building images ----")
        print("-> Building Database image..")
        self.db_img, _ = client.images.build(path=PATH_DOCKERFILE_DB, tag=IMAGE_NAME_DB)
        print(self.db_img.short_id.split(":")[1])
        print("-> Building Client image..")
        self.client_img, _ = client.images.build(path=PATH_DOCKERFILE_CLIENT, tag=IMAGE_NAME_CLIENT)
        print(self.client_img.short_id.split(":")[1])
        print("-> Building Server image..")
        self.server_img, _ = client.images.build(path=PATH_DOCKERFILE_SERVER, tag=IMAGE_NAME_SERVER)
        print(self.server_img.short_id.split(":")[1])
        print("-> Building the bot image..")
        self.bot_img, _ = client.images.build(path=PATH_DOCKERFILE_BOT, tag=IMAGE_NAME_BOT)
        print(self.bot_img.short_id.split(":")[1])
        print("-- Build -> done.")

    def create_networks(self):
        network_config = self.config['scenario']['network']
        ipam_pool = docker.types.IPAMPool(
            subnet= network_config['subnet'],
            gateway= network_config['gateway']
        )
        ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
        self.app_network = client.networks.create(
            name=PREFIX_IMAGE + "_app_network" + SUFFIX_CONTAINER,
            ipam=ipam_config
            )
        self.app_network.connect(
            container=self.client_container.name, 
            ipv4_address=self.config['scenario']['client']['private_ipv4_address'])
        self.app_network.connect(
            container=self.server_container.name,
        ipv4_address=self.config['scenario']['server']['private_ipv4_address'])
        self.app_network.connect(
            container=self.db_container.name,
            ipv4_address=self.config['scenario']['database']['private_ipv4_address'])
        self.app_network.connect(
            container=self.bot_container.name,
            ipv4_address=self.config['scenario']['bot']['private_ipv4_address']
        )
    
    def delete_networks(self):
        print("Deleting used network...")
        self.app_network.remove()
        print("the network has been deleted.")

    
    def launch_database(self):
        print("---- Launching database container ----")
        env_vars = self.from_dic_to_env(self.config['scenario']['database'])

        self.db_container = client.containers.run(
            image=IMAGE_NAME_DB,
            detach=True,
            cap_add=["SYS_NICE"],
            hostname= PREFIX_IMAGE + "_database_" + SUFFIX_CONTAINER,
            name= PREFIX_IMAGE + "_database_" + SUFFIX_CONTAINER,
            environment= env_vars,
            remove=True
        )
        print(f"Database {self.db_container} is running!")

    def launch_server(self):
        env_vars = self.from_dic_to_env(self.config['scenario']['server'])
        env_vars.append("SERVER_NAME_DB=" + PREFIX_IMAGE + "_database_" + SUFFIX_CONTAINER)

        print("---- Launching Server container ----")
        self.server_container = client.containers.run(
            image = IMAGE_NAME_SERVER,
            detach = True,
            hostname = PREFIX_IMAGE + "_server_" + SUFFIX_CONTAINER,
            name = PREFIX_IMAGE + "_server_" + SUFFIX_CONTAINER,
            remove = True,
            environment = env_vars,
            volumes = [PATH_DOCKERFILE_SERVER + ":/server"],
            entrypoint = ["tail", "-f", "/dev/null"],
            ports = {
                self.config['scenario']['server']['app_port']: self.config['scenario']['server']['mapping_port']}
        )

    def config_db(self, server_container):
        exit_code = 1
        tries = 10

        while exit_code != 0 and tries > 0:
            exit_code, _ = server_container.exec_run(cmd = "pip install -r /server/requirements.txt", stdin = True)
            exit_code, _ = server_container.exec_run(cmd = "python3 /server/manage.py initdb", stdin = True)
            exit_code, _ = server_container.exec_run(cmd = "python3 /server/manage.py migratedb", stdin = True)
            exit_code, _ = server_container.exec_run(cmd = "python3 /server/manage.py upgradedb", stdin = True)
            exit_code, _ = server_container.exec_run(cmd = "python3 /server/manage.py seeddb", stdin = True)
            tries = tries - 1
            if exit_code == 0:   
                print("SUCCESS -> Database has been initialized.")
            elif tries == 0:
                print("FAILURE -> Impossible to initialize the database")
                print(_)
                sys.exit(1)
            else :
                print(f"ATTEMPT N{10 - tries} Fail while setting up the database\n-> Retrying...")
    
    def init_server(self, server_container):
        exit_code, _ = server_container.exec_run(cmd = "python3 /server/manage.py run", detach=True)
        if exit_code != 1:
            print(f"Server {server_container} is running!")
        else:
            print("FAIL: Impossible to start the server.")
            sys.exit(1)

    def launch_client(self):
        print("---- Launching Client container ----")
        env_vars = self.from_dic_to_env(self.config['scenario']['client'])
        env_vars.append("VUE_APP_SERVER_IP_ADDRESS=" + self.config['scenario']['server']['private_ipv4_address'])

        self.client_container = client.containers.run(
            image = IMAGE_NAME_CLIENT,
            detach = True,
            hostname = PREFIX_IMAGE + "_client_" + SUFFIX_CONTAINER,
            name = PREFIX_IMAGE + "_client_" + SUFFIX_CONTAINER,
            remove = True,
            volumes = [PATH_DOCKERFILE_CLIENT+ ":/client"],
            entrypoint= ["tail", "-f", "/dev/null"],
            environment= env_vars,
            ports = {'3000/tcp': ('127.0.0.1', '3000')}
        )
        self.init_client(self.client_container)

    def init_client(self, client_container):
        exit_code, _ = client_container.exec_run(cmd = "npm install", workdir = "/client")
        exit_code, _ = client_container.exec_run(cmd = "npm run dev", workdir = "/client", detach=True)

        print(f"Client {client_container.short_id} is running!")

    def launch_bot(self):
        print(f"The bot is launched!")

        self.load_config_from_file(PATH_SCENARIOS +  "no_security" + ".json")
        env_vars = self.from_dic_to_env(self.config['scenario']['bot'])
        self.bot_container = client.containers.run(
            image = IMAGE_NAME_BOT,
            detach = True,
            name= PREFIX_IMAGE + "_bot_" + SUFFIX_CONTAINER,
            hostname = PREFIX_IMAGE + "_bot_" + SUFFIX_CONTAINER,
            remove = True,
            volumes = [PATH_DOCKERFILE_BOT + ":/bot"],
            entrypoint = ["tail", "-f", "/dev/null"],
            environment = env_vars
        )
    def ping_bot(self, url):
        pass

    def from_dic_to_env(self, object):
        env_list = []
    
        for key, value in object.items():
            env_list.append(str(key).upper() + "=" + str(value))
        return(env_list)
    
    def kill_containers(self):
        self.db_container.kill()
        self.server_container.kill()
        self.client_container.kill()

    def clean(self):
        self.kill_container(IMAGE_NAME_CLIENT)
        self.kill_container(IMAGE_NAME_DB)
        self.kill_container(IMAGE_NAME_SERVER)
        self.kill_container(IMAGE_NAME_BOT)
        self.kill_networks()

    def kill_container(self, image_name):
        containers = client.containers.list(
            filters = {
                "status": "running",
                "ancestor": image_name
            }
        )
        for container in containers:
            print(f"Removing container: {container.name} done")
            container.remove(force=True)

    def kill_networks(self):
        networks = client.networks.list(
            names = [PREFIX_IMAGE + "_app_network"]
        )

        for network in networks:
            network.remove()
            print(f"Removing network {network.name}")
    
    def reload_container(self, container_img):
        print(f"Reloading the {container_img}")
        if container_img == 'client':
            img_name = IMAGE_NAME_CLIENT
        elif container_img == 'server':
            img_name = IMAGE_NAME_SERVER
        elif container_img == 'db':
            img_name = IMAGE_NAME_DB
        containers = client.containers.list(
            filters = {
                "status": "running",
                "ancestor": img_name
            }
        )
        for container in containers:
            container.restart()
            if container_img == 'client':
                self.init_client(container)
            if container_img == 'server':
                self.init_server(container)
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--scenario", action="store_true", help="Launch a pre-existing scenario")
    group.add_argument("-f", "--config_file",  action="store_true", help="Launch a custom scenario")
    parser.add_argument("-c", "--clean", action="store_true", help="stop and clean docker related components")
    parser.add_argument("name", type=str, help="the scenario/config name")
    parser.add_argument("-r", "--reload", action="store_true", help="reload the targeted container [client | server | db]")
    parser.add_argument("-b", "--bot", action="store_true", help="Ask the bot to go the a specific url. ex: --bot ")

    args = parser.parse_args()

    if args.clean:
        manager = Platform_manager()
        manager.clean()
    if args.reload:
        manager = Platform_manager()
        manager.reload_container(args.name)
    elif args.bot:
        manager = Platform_manager()
        manager.launch_bot(args.name)
    elif args.scenario:
        manager = Platform_manager(scenario_name=args.name)
        manager.run()
    elif args.config_file:
        manager = Platform_manager(config_file=args.name)
        manager.run()
    else:
        print(f"Usage: you must specified an option [-s | -f] before {args.name}.")
        sys.exit(1)
