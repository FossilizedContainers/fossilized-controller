# importing the necessary libraries
import requests
import json

def main():
    run_metadata = open('metadata.json')

    files = {
        "metadata": open('metadata.json', 'rb')
    }

    metadata_read = json.loads(run_metadata.read())
    inputs_dict = metadata_read['input_files']

    for file_input in inputs_dict:
        location = inputs_dict[file_input]
        files[str(file_input)] = open(location, 'rb')
        #print(location)

    response = requests.post('http://172.17.0.2:4000', files=files)

    response_file = open('new_response_data.zip', 'wb')
    response_file.write(response.content)
    response_file.close()


if __name__ == '__main__':
    main()
