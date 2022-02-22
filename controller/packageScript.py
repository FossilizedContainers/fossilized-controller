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
    controller = controller_model.init_controller()
    print(controller.containers)


#
# there will be more here soon
#
@cli.command()
def stop():
    container = cli.prompt("What is the name of the container you would like to stop?")
    controller = controller_model.init_controller()
    container = controller.get_container(container)
    # checking that the container is running and exists before stopping
    if not isinstance(container.container, type(None)):
        container.container.stop()
    else:
        print("ERROR: container name not found: " + container.image)

# This command will clear out the cache of containers currently on the machine
# This function takes no parameters and does not return anything, it simply prints the
# result of deleting the cache
@cli.command()
def clean():
    # TODO: re-write based on container manager functions
    result = docker.prune()
    print("All stopped containers have been deleted!")
    print("RESULT: " + result)

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

    controller = controller_model.init_controller()
    container = controller.get_container(container)
    # checking that the container is running and exists before uploading
    if not isinstance(container.container, type(None)):
        container_object = (controller.get_container(container)).container
        container_object.push(repository)  # need to test functionality more
    else:
        print("ERROR: container name not found: " + container.image)


# This function will pause the container specified
@cli.command()
def pause():
    # prompting the user for the name of the container to be paused
    container = cli.prompt("Please type the name of the container you would like to pause: ")

    # use container manager to get container object
    controller = controller_model.init_controller()
    container = (controller.get_container(container)).container
    # checking that the container is running and exists before pausing
    if not isinstance(container.container, type(None)):
        container_object = (controller.get_container(container)).container
        container_object.pause()
        print("Container paused! \n")
    else:
        print("ERROR: container name not found: " + container.image)


# This function will unpause the container specified
@cli.command()
def unpause():
    # prompting the user for the name of the container to be unpaused
    container = cli.prompt("Please type the name of the container you would like to unpause: ")

    # use container manager to get container object
    controller = controller_model.init_controller()
    container = controller.get_container(container)
    # checking that the container is running and exists before unpausing
    if not isinstance(container.container, type(None)):
        container_object = (controller.get_container(container)).container
        container_object.pause()
        print("Container unpaused! \n")
    else:
        print("ERROR: container name not found: " + container.image)


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
