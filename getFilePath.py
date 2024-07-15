import os

def get_file_path(directory='../Content/inputContent'):

    filepaths = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            absolute_path = os.path.abspath(os.path.join(directory, filename))
            filepaths.append(absolute_path)
    return filepaths


