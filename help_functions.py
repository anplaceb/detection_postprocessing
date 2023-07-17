import os



def list_files(directory, extension):
    # List files with a given extension
    return [file for file in os.listdir(directory) if file.endswith(extension)]
