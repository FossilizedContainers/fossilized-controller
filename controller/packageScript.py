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
def help():
    pass

#
# there will be more here soon
#
@cli.command()
def upload():
    pass

#
# there will be more here soon
#
@cli.command()
def clean():
    print("Stopping all containers...\n")
    for container in client.containers.list():
        container.stop()

    print("Deleting all containers...\n")
    client.containers.prune()

#
# the client to connect to containers
#
def client():
    pass

# main to initiate variables and group
def main():
    global client
    client = docker.from_env()
    cli()


if __name__ == '__main__':
    main()
