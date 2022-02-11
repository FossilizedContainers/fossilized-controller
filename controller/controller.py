import json
import pickle
import os
import docker
import requests


# Class for information about a container
class ContainerInfo:
    def __init__(self, image, address="127.0.0.1", port=80):
        self.container_port = None
        self.image = image
        self.address = address
        self.port = port
        self.container = None

    def start(self, controller, run_metadata_file):
        # None in the ports dict assigns it to a random host port
        self.container = controller.client.containers.run(self.image, detach=True, ports={self.port: None})
        self.container.reload()
        # get the randomly assigned port
        self.container_port = self.container.ports['HostPort']

        run_metadata = json.load(open(run_metadata_file))

        files = {
            "metadata.json": open(run_metadata_file, 'rb')
        }
        for file_input in run_metadata['inputs']:
            typ = run_metadata['inputs'][file_input]['type']
            location = run_metadata['inputs'][file_input]['location']
            # add the external files listed in the run metadata to the post request
            files[str(file_input)] = open(location, 'rb')

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
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.containers, f)

    def add_container(self, container):
        self.containers.append(container)
        self.save()

    def run(self, container, run_metadata_file):
        return container.start(self, run_metadata_file)
