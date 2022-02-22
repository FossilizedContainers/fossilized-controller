import click
import docker
from os import walk
import controller.model as controller_model


# creating a group using the click library in order to make functions commands
@click.group()
def cli():
    pass


@cli.command()
def create():
    # creating a docker file to create the image
    docker_file = open("Dockerfile", "w")

    # prompting the user for the command to run the main file
    print("""
    What is the command to run your main file?
    Here are some examples:
    - python3 main.py
    - r main.R
    - sh main.sh
    """)
    run_command = cli.prompt("> ")

    file_contents = """
    FROM continuumio/anaconda3

    # copy all files to the root directory of the container
    COPY . /

    # create the conda environment
    RUN conda env create -f environment.yml

    CMD {run_command}
    """

    # adding the run command from the user to the string
    file_contents.format(run_command=run_command)

    # writing the string to the docker file
    docker_file.write(file_contents)

    # closing the docker file that was being edited
    docker_file.close()


#
# there will be more here soon
#
@cli.command()
@click.argument('container')
def run(container):
    controller = controller_model.init_controller()
    container = controller.get_container(container)
    print("Running the container...")
    result = controller.run(container, "./run_metadata.json")


#
# there will be more here soon
#
@cli.command()
def display():
    pass


#
# there will be more here soon
#
@cli.command()
def stop():
    pass


# This command will clear out the cache of containers currently on the machine
# This function takes no parameters and does not return anything, it simply prints the
# result of deleting the cache
@cli.command()
def clean():
    # initializing variables
    pruneIndex = 0

    # loop through the list of containers and kill them if there are running containers
    if ():  # function call to get a list of running containers, stops the running containers if there are any
        killIndex = 0
        while killIndex < len(containers):
            containers[killIndex].kill()
            killIndex += 1

    # will use container manager to get a list of container objects - check uml diagram at the top of 4
    containers = docker.list()

    # loop / command that clears that cache of containers
    while pruneIndex < len(containers):
        containers[pruneIndex].prune()
        pruneIndex += 1
    # print that the container has been cleared
    print("Container cache cleared!")


# This function prints the url to our helper page or a clickable link that takes the
# user to our help page
@cli.command()
def guide():
    # printing the URL to our help page
    print("Temporary link to projects github: https://github.com/FossilizedContainers/fossilized-controller")


# This function allows the user to upload a container image to a docker repository
@cli.command()
def upload():
    # prompting the user for the name of the container as well as the name of the repository
    container = cli.prompt("What container or image would you like to upload? ")
    repository = cli.prompt("What is the name of the repository you wish to upload to?")

    # will get the container object using the get container from the container manager
    controller = controller_model.init_controller()
    container_object = controller.get_container(container)

    # using the push function from the docker library to upload to the specified repository
    container_object.push(repository)  # need to test functionality more


# This function will pause the container specified
@cli.command()
def pause():
    # prompting the user for the name of the container to be paused
    container = cli.prompt("Please type the name of the container you would like to pause: ")

    # use container manager to get container object
    controller = controller_model.init_controller()
    container_object = controller.get_container(container)

    # using dockers pause function to pause the container
    container_object.pause()

    # printing that the container has been successfully paused
    print("Container paused! \n")


# This function will unpause the container specified
@cli.command()
def unpause():
    # prompting the user for the name of the container to be unpaused
    container = cli.prompt("Please type the name of the container you would like to unpause: ")

    # use container manager to get container object
    controller = controller_model.init_controller()
    container_object = controller.get_container(container)

    # using dockers unpause function to pause the container
    container_object.unpause()

    # printing that the container has been successfully paused
    print("Container unpaused! \n")


# main to initiate variables and group
def main():
    # try and except block to catch any errors in creating the click group
    try:
        cli()
    except:
        # printing that there was an error ( possibility add a more descriptive message )
        print("An exception occurred while trying to perform the latest action!")


if __name__ == '__main__':
    main()
