import docker
import os
import argparse
import json
import sys
from docker.utils.utils import convert_filters
import config
from network_manager import create_networks
from utils import clean, from_dic_to_env
client = docker.from_env()

class Platform_manager:
    """Manager the container depending on the configuration input"""
    def __init__(self, **kwargs):
        self.services = {}
        self.containers = {}
        for key, value in kwargs.items():
            if key == "config_file":
                self.scenario = key
                self.load_config_from_file(value)
            if key == "scenario_name":
                self.scenario = key
                self.load_config_from_file(config.PATH_SCENARIOS +  value + ".json")

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
        self.launch_malicious_serv()
        create_networks(self.config, self.containers)
        self.config_db(self.containers["server"])
        self.init_server(self.containers["server"])

    def build_images(self):
        stage = 0
        services = config.SERVICES
        print("----- Building images ----")
        for service in services:
            print(f"STAGE {stage} -> building {service}")
            path_dockerfile = services[service]["PATH_DOCKERFILE"]
            img_name = services[service]["IMAGE_NAME"]
            docker_img, _ = client.images.build(path=path_dockerfile, tag=img_name)
            print(docker_img.short_id.split(":")[1])
            self.services[service] = docker_img
            stage += 1
    
    def launch_database(self):
        print("---- Launching database container ----")
        env_vars = from_dic_to_env(self.config['scenario']['database'])
        db_container = client.containers.run(
            image = config.SERVICES["database"]["IMAGE_NAME"],
            detach = True,
            cap_add = ["SYS_NICE"],
            hostname = config.PREFIX_IMAGE + "_database_" + config.SUFFIX_CONTAINER,
            name = config.PREFIX_IMAGE + "_database_" + config.SUFFIX_CONTAINER,
            environment = env_vars,
            remove = True,
            labels= {"config_name": "database", "scenario": self.scenario}
        )
        self.containers["database"] = db_container.name
        print(f"Database {db_container} is running!")

    def launch_server(self):
        env_vars = from_dic_to_env(self.config['scenario']['server'])
        env_vars.append("SERVER_NAME_DB=" + config.PREFIX_IMAGE + "_database_" + config.SUFFIX_CONTAINER)
        running_port = self.config['scenario']['server']['app_port']
        mapping_port = self.config['scenario']['server']['mapping_port']

        print("---- Launching Server container ----")

        server_container = client.containers.run(
            image = config.SERVICES["server"]["IMAGE_NAME"],
            detach = True,
            hostname = config.PREFIX_IMAGE + "_server_" + config.SUFFIX_CONTAINER,
            name = config.PREFIX_IMAGE + "_server_" + config.SUFFIX_CONTAINER,
            remove = True,
            environment = env_vars,
            volumes = [config.SERVICES["server"]["PATH_DOCKERFILE"] + ":/server"],
            entrypoint = ["tail", "-f", "/dev/null"],
            ports = {running_port: mapping_port},
            labels= {"config_name": "server", "scenario": self.scenario}
        )
        self.containers["server"] = server_container.name

    def config_db(self, container_name):
        exit_code = 1
        tries = 10
        server_container = client.containers.get(container_name)
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
    
    def init_server(self, container_name):
        server_container = client.containers.get(container_name)
        exit_code, _ = server_container.exec_run(cmd = "python3 /server/manage.py run", detach=True)
        if exit_code != 1:
            print(f"Server {server_container} is running!")
        else:
            print("FAIL: Impossible to start the server.")
            sys.exit(1)

    def launch_client(self):
        print("---- Launching Client container ----")
        env_vars = from_dic_to_env(self.config['scenario']['client'])
        env_vars.append("VUE_APP_SERVER_IP_ADDRESS=" + self.config['scenario']['server']['private_ipv4_address'])

        client_container = client.containers.run(
            image = config.SERVICES["client"]["IMAGE_NAME"],
            detach = True,
            hostname = config.PREFIX_IMAGE + "_client_" + config.SUFFIX_CONTAINER,
            name = config.PREFIX_IMAGE + "_client_" + config.SUFFIX_CONTAINER,
            remove = True,
            volumes = [config.SERVICES["client"]["PATH_DOCKERFILE"] + ":/client"],
            entrypoint= ["tail", "-f", "/dev/null"],
            environment= env_vars,
            ports = {'3000/tcp': ('127.0.0.1', '3000')},
            labels= {"config_name": "client", "scenario": self.scenario}
        )
        self.init_client(client_container)
        self.containers["client"] = client_container.name

    def init_client(self, client_container):
        exit_code, _ = client_container.exec_run(cmd = "npm install", workdir = "/client")
        exit_code, _ = client_container.exec_run(cmd = "npm run dev", workdir = "/client", detach=True)

        print(f"Client {client_container.short_id} is running!")

    def launch_bot(self):
        print("---- Launching Bot container ----")
        env_vars = from_dic_to_env(self.config['scenario']['bot'])
        
        bot_container = client.containers.run(
            image = config.SERVICES["bot"]["IMAGE_NAME"],
            detach = True,
            name= config.PREFIX_IMAGE + "_bot_" + config.SUFFIX_CONTAINER,
            hostname = config.PREFIX_IMAGE + "_bot_" + config.SUFFIX_CONTAINER,
            remove = True,
            volumes = [config.SERVICES["bot"]["PATH_DOCKERFILE"] + ":/bot"],
            entrypoint = ["tail", "-f", "/dev/null"],
            environment = env_vars,
            labels= {"config_name": "bot", "scenario": self.scenario}
        )
        self.containers["bot"] = bot_container.name

    def trigger_bot(self, url):
        print(f"the bot is navigating to {url}")
        containers = client.containers.list(
            filters = {
                "status": "running",
                "ancestor": config.SERVICES["bot"]["IMAGE_NAME"]
            }
        )
        print(containers)
        for container in containers:
            exit_code, _ = container.exec_run(
                cmd = f"python main.py {url}",
                workdir = "/bot"
            )
            print(f"Done: {_}")

    def launch_malicious_serv(self):
        print("---- Launching Malicious container ----")
        env_vars = from_dic_to_env(self.config['scenario']['malicious_serv'])
        mapping_port = self.config['scenario']['malicious_serv']["mapping_port"]
        running_port = self.config['scenario']['malicious_serv']["running_port"]

        malicious_container = client.containers.run(
            image = config.SERVICES["malicious_server"]["IMAGE_NAME"],
            detach = True,
            name= config.PREFIX_IMAGE + "_malicious_serv_" + config.SUFFIX_CONTAINER,
            hostname = config.PREFIX_IMAGE + "_malicious_serv_" + config.SUFFIX_CONTAINER,
            remove = True,
            volumes = [config.SERVICES["malicious_server"]["PATH_DOCKERFILE"] + ":/malicious_serv", config.ABSOLUTE_PATH + "/malicious_logs" +  ":/malicious_logs"],
            entrypoint = ["tail", "-f", "/dev/null"],
            environment = env_vars,
            ports = {running_port: mapping_port},
            labels= {"config_name": "malicious_serv", "scenario": self.scenario}
        )
        self.containers["malicious_serv"] = malicious_container.name
        exit_code, _ = malicious_container.exec_run(
            cmd = "python malicious_serv.py",
            workdir = "/malicious_serv",
            detach= True
        )
        if exit_code != 1:
            print(f"The Malicious server {malicious_container.short_id} is running.")
        else:
            print("The malicious Server's launch has failed:\b" + _)
    
    def reload_container(self, container_img):
        print(f"Reloading the {container_img}")
        if container_img == 'client':
            img_name = config.IMGS["IMAGE_NAME_CLIENT"]
        elif container_img == 'server':
            img_name = config.IMGS["IMAGE_NAME_SERVER"]
        elif container_img == 'db':
            img_name = config.IMGS["IMAGE_NAME_DB"]
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
    group2 = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--scenario", action="store_true", help="Launch a pre-existing scenario")
    group.add_argument("-f", "--config_file",  action="store_true", help="Launch a custom scenario")
    group2.add_argument("-c", "--clean", action="store_true", help="stop and clean docker related components")
    parser.add_argument("name", type=str, help="the scenario/config name")
    group2.add_argument("-r", "--reload", action="store_true", help="reload the targeted container [client | server | db]")
    group2.add_argument("-b", "--bot", action="store_true", help="Ask the bot to go the a specific url. ex: --bot ")

    args = parser.parse_args()

    if args.clean:
        clean()
    if args.reload:
        manager = Platform_manager()
        manager.reload_container(args.name)
    elif args.bot:
        manager = Platform_manager()
        manager.trigger_bot(args.name)
    elif args.scenario:
        manager = Platform_manager(scenario_name=args.name)
        manager.run()
    elif args.config_file:
        manager = Platform_manager(config_file=args.name)
        manager.run()
    else:
        print(f"Usage: you must specified an option [-s | -f] before {args.name}.")
        sys.exit(1)