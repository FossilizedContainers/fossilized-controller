import sys
from click.testing import CliRunner
from packageScript import *
sys.path.insert(0, 'C:/Users/Golde/PycharmProjects/fossilized-controller/python-adapter')
import adapter
adapter = adapter.global_adapter

# Unit testing for packageScript.py

# create
def test_create():
    runner = CliRunner()
    result = runner.invoke(create, input='python unitTest.py')
    with open('DockerFile', 'r') as i:
        print(i.read())

# display
def test_display():
    runner = CliRunner()
    result = runner.invoke(display)
    print(result.output)

# clean
def test_clean():
    runner = CliRunner()
    cleanResult = runner.invoke(clean)
    displayResult = runner.invoke(display)
    print(cleanResult.output)
    print(displayResult.output)


# Unit testing for model.py
def test_containerManager():
    # make the controller
    controller = controller_model.init_controller()
    # call get container several times

    # check that get container is creating an object and caching it


# Unit testing for adapter.py
def test_adapter():
    # start the flask server
    print(adapter.start_server())
    # send files to the server

    # receive some files

    # check the data was recieved as a zip file


# Unit testing for r adapter

def main():
    test_create()
    test_display()
    test_clean()
    test_adapter()

if __name__ == '__main__':
    main()