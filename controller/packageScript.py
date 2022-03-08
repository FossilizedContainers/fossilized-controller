import click
import docker
import model as controller_model
import os


# creating a group using the click library in order to make functions commands
@click.group()
def cli():
    pass

# Function to create a docker file
# This function takes no parameters and does not return a value
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

    print("Dockerfile created!")

# Function to build an image from a Dockerfile
# This function does not return a value and gets a name for the image as an argument
@cli.command()
@click.argument('name')
def build(name):
    # creating a call that builds the container
    os.system('Docker build -t {imageName} .'.format(imageName=name))

# Function to run a container
# This function does not return a value and gets a container name as an argument
@cli.command()
@click.argument('container')
def run(container):
    controller = controller_model.init_controller()
    container = controller.get_container(container)
    print("Running the container...")
    result = controller.run(container, "./metadata.json")


# Function to display all of the container images that exist
# This function takes no parameters and does not return a value
# This does not properly display containers right now
@cli.command()
def display():
    controller = controller_model.init_controller()
    print("List of containers: ")
    # the containers are in a list
    for container_name in controller.containers:
        print(container_name.image)


# Function to stop a container that is currently running
# This function takes no parameters and does not return a value
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

# Function to clear out the cache of containers currently on the machine
# This function takes no parameters and does not return anything, it simply prints the
# result of deleting the cache
# The formatting of the results needs to be changed
@cli.command()
def clean():
    controller = controller_model.init_controller()
    result = controller.client.containers.prune()
    print("All stopped containers have been deleted!")
    print("RESULT:\n")
    print(result)

# This function prints the url to our helper page or a clickable link that takes the
# user to our help page
@cli.command()
def guide():
    # printing the URL to our help page
    print("Temporary link to projects github: https://github.com/FossilizedContainers/fossilized-controller")


# Function allowing the user to upload a container image to a docker repository
# This function takes no parameters and does not return a value
@cli.command()
def upload():
    # prompting the user for the name of the container as well as the name of the repository
    repository = click.prompt("What is the name of the repository you wish to upload to? (NOTE: it should have the same name as your container)")

    # creating a system call to upload the image to the repository
    os.system('docker image push {repositoryName}'.format(repositoryName=repository))


# Function allowing the user to download a container image from a docker repository
# This function takes no parameters and does not return a value
@cli.command()
def download():
    # prompting the user for the name of the container image
    name = click.prompt("What image or container would you like to download?")

    controller = controller_model.init_controller()

    # pulls the image from Dockerhub
    # this makes sure an image actually exists on dockerhub
    try:
        controller.client.images.pull(name)
        print("The image: " + name + " was successfully downloaded")
    except docker.errors.APIError:
        print(name + " could not be downloaded")


# Function to pause the container specified
# This function takes no parameters and does not return a value
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


# Function to unpause the container specified
# This function takes no parameters and does not return a value
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

# building the package requires a main function
def main():
    cli()

if __name__ == '__main__':
    main()
