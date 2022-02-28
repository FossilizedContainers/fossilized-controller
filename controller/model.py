import json
import pickle
import os
import docker
import requests
from os.path import expanduser


# Class for information about a container
class ContainerInfo:
    def __init__(self, image: str, address: str = "127.0.0.1", port: int = 80):
        self.container_port = None
        self.image = image
        self.address = address
        self.port = port
        self.container = None

    def start(self, controller, run_metadata_file: str):
        # None in the ports dict assigns it to a random host port
        self.container = controller.client.containers.run(self.image, detach=True, ports={self.port: None})
        self.container.reload()
        # get the randomly assigned port
        self.container_port = list(self.container.ports.values())[0][0]['HostPort']

        run_metadata = json.load(open(run_metadata_file))

        files = {
            "metadata.json": open(run_metadata_file, 'rb')
        }
        for file_input in run_metadata['inputs']:
            typ = run_metadata['inputs'][file_input]['type']
            location = run_metadata['inputs'][file_input]['location']
            # add the external files listed in the run metadata to the post request
            files[str(file_input)] = open(location, 'rb')

        print(self.container.attrs['State'])
        results = requests.post("http://{}:{}/start".format(self.address, self.container_port), files=files)
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
