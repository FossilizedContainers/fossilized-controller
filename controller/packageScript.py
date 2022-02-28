import click
import docker
import model as controller_model


# creating a group using the click library in order to make functions commands
@click.group()
def cli():
    pass


@cli.command()
def create():
    # creating a docker file to create the image
    docker_file = open("./Dockerfile", "w")

    # prompting the user for the command to run the main file
    print("""What is the command to run your main file?
Here are some examples:
- python3 main.py
- r main.R
- sh main.sh
""")

    run_command = click.prompt("> ")

    file_contents = """FROM continuumio/anaconda3

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
CMD conda run --no-capture-output -n presto_container {run_command}
""".format(run_command=run_command)

    # writing the string to the docker file
    docker_file.write(file_contents)

    # closing the docker file that was being edited
    docker_file.close()

    # call the function to build the container from the dockerfile
    build_in_cwd()

#
# function to build the container
#
def build_in_cwd():
    client = docker.from_env()
    print("Building docker image...")
    client.images.build(path="./", quiet=False)
    print("Docker container built!")

@cli.command()
def build():
    build_in_cwd()

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
    print("List of containers: " + controller.containers)


#
# there will be more here soon
#
@cli.command()
def stop():
    container = click.prompt("What is the name of the container you would like to stop?")
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
    container = click.prompt("What container or image would you like to upload? ")
    repository = click.prompt("What is the name of the repository you wish to upload to?")

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
    container = click.prompt("Please type the name of the container you would like to pause: ")

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
    container = click.prompt("Please type the name of the container you would like to unpause: ")

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


if __name__ == '__main__':
    cli()
