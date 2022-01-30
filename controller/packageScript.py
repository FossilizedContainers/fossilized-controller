import click
import docker
import requests


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
def clean():
    pass

# This function prints the url to our helper page or a clickable link that takes the
# user to our help page
@cli.command()
def help():
    # printing the URL to our help page
    print("https://github.com/FossilizedContainers/fossilized-controller")

# This function will upload the container to dockerhub or github
# Functionality will be implemented later
@cli.command()
def upload():
    pass

# This function will pause all or some of the containers specified
# Parameters - container, list of container(s) to be paused ( not required )
@cli.command()
def pause(container = []):
    pass

# main to initiate variables and group
def main():
    global client
    client = docker.from_env()
    cli()


if __name__ == '__main__':
    main()
