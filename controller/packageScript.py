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
- Rscript main.R
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
# TO DO: update this to make it display the build process
@cli.command()
@click.argument('name')
def build(name):
    # creating a call that builds the container
    controller = controller_model.init_controller()
    print("Building the image.... This might take a while")

    try:
        image_obj, generator = controller.client.images.build(path='.',
                                                              tag=name)
        while True:
            try:
                output = generator.__next__()
                if "stream" in output:
                    click.echo(output['stream'])
            except StopIteration:
                print("Building {} image complete".format(name))
                break
            except ValueError:
                print("Error parsing output")

    except docker.errors.BuildError:
        print("ERROR: The build can not complete")


# Function to run a container
# This function does not return a value and gets a container name as an argument
@cli.command()
@click.argument('name')
def run(name):
    controller = controller_model.init_controller()
    container = controller.get_container(name)
    print("Running the container...")

    try:
        result = controller.run(container, "./metadata.json")

        response_file = open('response_data.zip', 'wb')
        response_file.write(result.content)
        response_file.close()
        print("Output files successfully saved at ./response_data.zip")

    except docker.errors.ContainerError:
        print("ERROR: Container can not run")
    except docker.errors.ImageNotFound:
        print("ERROR: The container {} was not found".format(name))
    except docker.errors.APIError:
        print("ERROR: Issue connecting to the Docker API")


# Function to display all of the container images that exist
# This function takes no parameters and does not return a value
# This does not properly display containers right now
@cli.command()
def display():
    controller = controller_model.init_controller()
    print("List of containers: ")
    # the containers are in a list
    for container in controller.client.containers.list():
        print('Container Name:{}       Container Image:{}'.format(container.attrs['Name'],
                                                                  container.image.tags))


# Function to stop a container that is currently running
# This function takes no parameters and does not return a value
@cli.command()
@click.argument('container_name')
def stop(container_name):
    controller = controller_model.init_controller()

    try:
        container = controller.client.containers.get(container_name)
    except docker.errors.NotFound as exc:
        print("ERROR: container name not found: " + container_name)
    else:
        container.stop()
        print("The container, {}, was successfully stopped".format(container_name))

# Function to clear out the cache of containers currently on the machine
# This function takes no parameters and does not return anything, it simply prints the
# result of deleting the cache
@cli.command()
def clean():
    controller = controller_model.init_controller()

    try:
        result = controller.client.containers.prune()
        print("All stopped containers have been deleted!")
        print("Containers deleted: " + str(result['ContainersDeleted']))
        print("Space recovered: " + str(result["SpaceReclaimed"]) + "MB")
    except docker.errors.APIError:
        print("ERROR: Issue connecting to the Docker API")

# This function prints the url to our helper page or a clickable link that takes the
# user to our help page
@cli.command()
def guide():
    # printing the URL to our help page
    print("Click the following link for a guide on how to use the tool!")
    print("https://fossilizedcontainers.github.io/fossilized-controller/")


# Function allowing the user to upload a container image to a docker repository
# This function takes no parameters and does not return a value
# TO DO: Look into low level API for live logs
@cli.command()
@click.argument('name')
def upload(name):
    controller = controller_model.init_controller()

    try:
        result = controller.client.images.push(name)

        if "errorDetail" in result:
            print("There was an error uploading the image")
        else:
            print("The image: {} was successfully uploaded".format(name))
    except docker.errors.APIError:
        print("ERROR: {} could not be uploaded".format(name))


# Function allowing the user to download a container image from a docker repository
# This function takes no parameters and does not return a value
# TO DO: Look into low level API for live logs
@cli.command()
@click.argument('name')
def download(name):
    controller = controller_model.init_controller()
    # pulls the image from Dockerhub
    # this makes sure an image actually exists on dockerhub
    try:
        controller.client.images.pull(name)
        print("The image: {} was successfully downloaded".format(name))
    except docker.errors.APIError:
        print("ERROR: {} could not be downloaded".format(name))


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

# Function to delete the image from the local docker client
@cli.command()
@click.argument('image')
def delete(image):
    # creating a controller object and container information object
    controller = controller_model.init_controller()
    container = (controller.get_container(image)).container

    # checking that the image exists before removing it
    try:
        controller.client.images.remove(image)
        print("The image was successfully deleted!")
    except docker.errors.APIError:
        print("ERROR: image name not found: " + image)


# building the package requires a main function
def main():
    cli()

if __name__ == '__main__':
    main()
