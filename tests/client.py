# importing the necessary libraries
import requests

def main():
    # Actual client is in the /controller/model.py
    files = {"metadata": open("metadata.json", 'r'),
             "weldeab": open("lipd-files/GeoB9307_3.Weldeab.2014.lpd", 'rb'),
             "net_cdf": open("nc-files/WMI_Lear.nc", 'rb')}

    response = requests.post('http://localhost:4000', files=files)

    print(response)
    print(response.headers)
    print(response.content)

    response_file = open('new_response_data.zip', 'wb')
    response_file.write(response.content)
    response_file.close()


if __name__ == "__main__":
    main()