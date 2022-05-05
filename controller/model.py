import json
import pickle
import os
import docker
import requests
from os.path import expanduser

# delete later
import time


# Class for information about a container
class ContainerInfo:
    def __init__(self, image: str, address: str = "127.0.0.1", port: int = 80):
        self.container_port = None
        self.image = image
        self.address = address
        self.port = port
        self.container = None

    def start(self, controller, run_metadata_file: str):
        #checks if the container already exists before running it
        self.container = controller.client.containers.run(self.image, detach=True, ports= {'4000/tcp': ('127.0.0.1', 4000)})
        self.container.reload()
        # get the randomly assigned port
        #self.container_port = list(self.container.ports.values())[0][0]['HostPort']
        # This is the same port that the adapter sets for the server
        self.container_port=4000

        # parsing json file and indicating every file that needs to be sent
        run_metadata = open('metadata.json')

        files = {
            "metadata": open(run_metadata_file, 'rb')
        }

        metadata_read = json.loads(run_metadata.read())
        inputs_dict = metadata_read['inputs']

        for file_input in inputs_dict:
            location = inputs_dict[file_input]
            files[str(file_input)] = open(location, 'rb')

        print(self.container.attrs['State'])

        # I needed to add this because the server takes a bit to start up
        # TODO: add a way to wait to send the post until we detect the server is up
        time.sleep(10)
        results = requests.post("http://{}:{}".format(self.address, self.container_port), files=files)
        return results


# Main controller class
# Managers
class Controller:
    def __init__(self, cache_file):
        self.cache_file = cache_file
        self.client = docker.from_env()
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                self.containers = pickle.load(f)
        else:
            self.containers = []

    def save(self):
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.containers, f)

    # search through the list of containers to find the one with the given image
    def __find_container(self, image: str):
        for container in self.containers:
            if container.image == image:
                return container

    # find an existing container, or create one and to the list of containers
    def get_container(self, image: str):
        c = self.__find_container(image)
        if c is None:

            c = ContainerInfo(image)
            self.containers.append(c)
            self.save()
        return c

    def run(self, container: ContainerInfo, run_metadata_file: str):
        return container.start(self, run_metadata_file)


# main controller instance, use init_controller() below
__controller = None
# location of the cache file on disk
__cache_file = expanduser("~") + "/.presto/controller.cache"


# Initialize the controller singleton if it doesn't exist
def init_controller() -> Controller:
    global __controller
    if __controller is None:
        __controller = Controller(__cache_file)
    return __controller
