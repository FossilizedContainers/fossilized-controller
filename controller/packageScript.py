import click
import docker


# creating a group of commands that can be run
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
# TO DO: add an optional argument for an image name.
#        This is so they can use images they pulled from Dockerhub
# TO DO: add error checking for a dockerfile in current directory
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
# An example docker container for testing this command
# docker run -d alpine sh -c 'while sleep 3600; do :; done'
@cli.command()
def display():

    # TO DO: Figure out why the image name does not show
    print("STATUS          NAME")
    for container in client.containers.list():
        # TO DO: Format the string better
        # print(container.image.get("Image"))
        print(container.status + "         " +
              container.name + "\n")

#
# TO DO: Add an option to stop one container
#
@cli.command()
def stop():
    print("Stopping all containers...\n")

    for container in client.containers.list():
        print("The container " + container.name + " has been stopped...\n")
        container.stop()

# This command will clear out the cache of containers currently on the machine
# This function takes no parameters and does not return anything, it simply prints the
# result of deleting the cache
@cli.command()
def clean():
    # initializing variables
    killIndex = 0
    pruneIndex = 0
    # will use container manager to get a list of container objects - check uml diagram at the top of 4
    containers = []
    # loop through the list of containers and kill them
    while killIndex < len(containers):
        containers[killIndex].kill()
        killIndex += 1
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
    print("https://github.com/FossilizedContainers/fossilized-controller")

# NOTE: I had to comment out the @cli.prompts because they were throwing errors for me - Emily

# This function will upload the container to dockerhub or github
# Functionality will be implemented later
@cli.command()
# @cli.prompt("Please type the name of the container you would like to upload: ")
def upload(container):
    pass

# This function will pause the container specified
@cli.command()
# @cli.prompt("Please type the name of the container you would like to pause: ")
def pause(container):
    # will use container manager to get container object

    # using dockers pause function to pause the container
    container.pause()
    # printing that the container has been successfully paused
    print("Container paused \n")

# This function will unpause the container specified
@cli.command()
# @cli.prompt("Please type the name of the container you would like to unpause: ")
def unpause(container):
    # will use container manager to get container object

    # using dockers pause function to pause the container
    container.unpause()
    # printing that the container has been successfully paused
    print("Container unpaused \n")

# main to initiate variables and group
def main():
    global client
    client = docker.from_env()

    # The exception is always showing up for me - Emily
    try:
        cli()
    except:
        print("An exception occurred while trying to perform the latest action")


if __name__ == '__main__':
    main()
