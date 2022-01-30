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
@cli.prompt("Please type the name of the container you would like to clear from the cache: ")
def clean(container):
    # will use container manager to get container object

    # pruning the container or deleting it
    client.prune(container)
    # print that the container has been cleared
    print("Container cache cleared!")


# This function prints the url to our helper page or a clickable link that takes the
# user to our help page
@cli.command()
def help():
    # printing the URL to our help page
    print("https://github.com/FossilizedContainers/fossilized-controller")

# This function will upload the container to dockerhub or github
# Functionality will be implemented later
@cli.command()
@cli.prompt("Please type the name of the container you would like to upload: ")
def upload(container):
    pass

# This function will pause the container specified
@cli.command()
@cli.prompt("Please type the name of the container you would like to pause: ")
def pause(container):
    # will use container manager to get container object

    # using dockers pause function to pause the container
    container.pause()
    # printing that the container has been successfully paused
    print("Container paused \n")

# This function will unpause the container specified
@cli.command()
@cli.prompt("Please type the name of the container you would like to unpause: ")
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
    try:
        cli()
    except:
        print("An exception occurred while trying to perform the latest action")


if __name__ == '__main__':
    main()
