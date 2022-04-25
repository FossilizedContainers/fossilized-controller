import os
import sys
import requests
from click.testing import CliRunner
from packageScript import *
import docker
import unittest
import model as controller_model
import tempfile
import json
import requests

controller_dir = os.path.dirname(os.path.realpath(__file__))
fc_dir = os.path.dirname(controller_dir)

python_adapter_dir = os.path.join(fc_dir, "python-adapter")
sys.path.append(python_adapter_dir)

tests_dir = os.path.join(fc_dir, "tests")

import adapter
import time

adapter = adapter.global_adapter


class TestPackageMethods(unittest.TestCase):
    @unittest.skip("Testing")
    def test_create(self):
        runner = CliRunner()
        result = runner.invoke(create, input='python unitTest.py')
        expectedResult = """FROM continuumio/anaconda3

RUN conda update -n base -c defaults conda

# setup conda environment
COPY presto_environment.yml .
RUN conda env create -f presto_environment.yml
RUN echo "conda activate presto_container" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]
RUN conda activate presto_container

# copy all files to the root directory of the container
COPY . /

# run the command in the context of the environment we made
CMD conda run --no-capture-output -n presto_container python unitTest.py
"""
        # read file to a string and then compare
        receivedResult = ""
        file = open('Dockerfile', 'r')
        receivedResult = file.read()
        self.assertEqual(expectedResult, receivedResult)

    @unittest.skip("Testing")
    # clean
    def test_clean(self):
        client = docker.from_env()
        runner = CliRunner()
        cleanResult = runner.invoke(clean)
        # check that prune deleted all of the containers
        self.assertEqual(client.containers.list(), [])


class TestContainerManager(unittest.TestCase):
    @unittest.skip("Testing")
    def test_containerManager(self):
        cacheFile = tempfile.NamedTemporaryFile()
        cacheFile.close()
        # make the controller
        controller = controller_model.init_controller(cacheFile.name)
        # call get container several times
        num = 10
        index = 0
        while index < num :
            controller.get_container(f'unitTest - get_container:  {index}')
            index += 1
        # delete the controller
        controller_model.delete_controller()
        # create a new controller and check that the container is cached
        controller = controller_model.init_controller(cacheFile.name)
        # need container info object
        self.assertEqual(len(controller.containers), num)


# Unit testing for adapter library
class TestAdapterLibrary(unittest.TestCase):

    def setUp(self):
        self.app = adapter.server
        self.app.config['TESTING'] = True
        self.app = self.app.test_client()

        os.chdir(tests_dir)

    def test_start_server(self):
        rv = self.app.get("/testGET")
        assert b'Accepting get requests' in rv.data

    def test_handle_post(self):
        rv = self.app.post("/testPOST")
        assert b'Accepting post requests' in rv.data

if __name__ == '__main__':
    unittest.main()
