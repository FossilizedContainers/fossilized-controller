import click
import docker
from os import walk


# creating a group using the click library in order to make functions commands
@click.group()
def cli():
    pass


# Requires: Initialized docker client,
#           Alpine image pulled and/or available
# TO DO:    Check if docker client is initialized, if not then pass an error
# TO DO:    Check if the image is available, if not then pass an error
# adding the hello-world command to the group
@cli.command()
def create():
    # creating a docker file to create the image
    docker_file = open("Dockerfile", "w")

    # copying all of the files to a list
    files = [file for file in walk("./")]

    # prompting the user for the image they would like to use
    image = cli.prompt("What image would you like your container to use? ( Default is ubuntu ) ", default="ubuntu")
    image = image.lower()
    docker_file.write("FROM " + image + ":latest\n")

    # search the current directory files for the language
    for file in files:
        if file.endswith(".py"):
            language = "python"
            break
        if file.endswith(".r"):
            language = "r"
            break

    # prompting the user for the language that will be used
    language = cli.prompt("What programming language are you using? ( Default is Python or R)", default=language)
    language = language.lower()

    # downloading and installing conda in the environment
    docker_file.write("RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda")
    docker_file.write("RUN ./Miniconda3-latest-Linux-x86_64.sh")

    # copying the users environment file to the Dockerfile and creating the environment
    docker_file.write("COPY environment.yml")
    docker_file.write("RUN conda env create -f environment.yml\n")

    # grab all of the files from the current directory - potentially using gitignore to remove unneeded files
    docker_file.write("COPY . /\n")

    # ask the user for the port number to be used for the containers server
    port = cli.prompt("What port would you like the server to run on? ( Default is 80 ) ", default=80)
    docker_file.write("EXPOSE " + port)

    # writing commands to the docker file
    main_file = cli.prompt("What is the name of the main file in your project?")
    docker_file.write("CMD " + language + "/" + main_file)

    # closing the docker file that was being edited
    docker_file.close()


#
# there will be more here soon
#
@cli.command()
def run():
    # Build the image
    print("Building image from docker_file...\n")
    client.images.build(path=".", tag="tech-demo")
    print("Finished building image...\n")

    # Run the container
    print("Running the container...\n")
    cont = client.containers.run("tech-demo", detach=True)
    print(cont.logs().decode("utf-8"))

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
    containers = []
    # loop / command that clears that cache of containers
    while pruneIndex < len(containers):
        containers[pruneIndex].prune()
        pruneIndex += 1
    # print that the container has been cleared
    print("Container cache cleared!")


# This function prints the url to our helper page or a clickable link that takes the
# user to our help page
@cli.command()
def help():
    # printing the URL to our help page
    print("Temporary link to projects github: https://github.com/FossilizedContainers/fossilized-controller")

# This function allows the user to upload a container image to a docker repository
@cli.command()
def upload():
    # prompting the user for the name of the container as well as the name of the repository
    container = cli.prompt("What container or image would you like to upload? ")
    repository = cli.prompt("What is the name of the repository you wish to upload to?")

    # will get the container object using the get container from the container manager

    # using the push function from the docker library to upload to the specified repository

# This function will pause the container specified
@cli.command()
def pause():
    # prompting the user for the name of the container to be paused
    container = cli.prompt("Please type the name of the container you would like to pause: ")

    # will use container manager to get container object

    # using dockers pause function to pause the container

    # printing that the container has been successfully paused
    print("Container paused! \n")

# This function will unpause the container specified
@cli.command()
def unpause():
    # prompting the user for the name of the container to be unpaused
    container = cli.prompt("Please type the name of the container you would like to unpause: ")

    # will use container manager to get container object

    # using dockers pause function to pause the container

    # printing that the container has been successfully paused
    print("Container unpaused! \n")

# main to initiate variables and group
def main():
    # creating a global container to test functionality
    global client
    client = docker.from_env()
    # try and except block to catch any errors in creating the click group
    try:
        cli()
    except:
        # printing that there was an error ( possibility add a more descriptive message )
        print("An exception occurred while trying to perform the latest action!")


if __name__ == '__main__':
    main()
