import click
import docker


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
    example = click.prompt("Please specify what image you would like to use", type=str)
    message = "echo "
    message += click.prompt("Please enter a message for the container to display", type=str)
    print("\nCreating new container...")


#
# there will be more here soon
#
@cli.command()
def run():
    # Build the image
    print("Building image from Dockerfile...\n")
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
