import os
import pathlib


# DIRECTORY PATH
ABSOLUTE_PATH = str(pathlib.Path(__file__).parent.resolve())
PATH_SCENARIOS = ABSOLUTE_PATH + "/scenarios/"
PATH_PLATFORM = ABSOLUTE_PATH + "/platform/my-vuln-app/"

#DOCKERFILES PATH

PREFIX_IMAGE = "pfe_sm_lns"
SUFFIX_CONTAINER = str(os.getpid())

SERVICES = {
    "client":
    {
        "PATH_DOCKERFILE": PATH_PLATFORM + "client/",
        "IMAGE_NAME": PREFIX_IMAGE + "_client"

    },
    "server":
    {
        "PATH_DOCKERFILE": PATH_PLATFORM + "server/",
        "IMAGE_NAME": PREFIX_IMAGE + "_server",
    },
    "database":
    {
        "PATH_DOCKERFILE": PATH_PLATFORM + "bdd/",
        "IMAGE_NAME": PREFIX_IMAGE + "_database",
    },
    "bot":
    {
        "PATH_DOCKERFILE": PATH_PLATFORM + "bot-victim/",
        "IMAGE_NAME": PREFIX_IMAGE + "_bot",

    },
    "malicious_server":
    {
        "PATH_DOCKERFILE": ABSOLUTE_PATH + "/platform/malicious_serv",
        "IMAGE_NAME": PREFIX_IMAGE + "_malicious_serv"
    }
}