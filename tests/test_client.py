# importing the necessary libraries
import requests


def main():
    # creating a dictionary to send the LiPD file to the server
    files = {"metadata": open("metadata.json", 'r'),
             "weldeab": open("lipd-files/GeoB9307_3.Weldeab.2014.lpd", 'rb')}

    response = requests.post('http://localhost:4000', files=files)

    # printing the file that the client received back from the server in the response message
    print(response)


if __name__ == "__main__":
    main()