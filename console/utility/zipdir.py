import os
import zipfile

# , exclusion
def zipdir(input_directory, output_file):

    initial_dir = os.getcwd()
    os.chdir(input_directory)
    if not input_directory.endswith('/'):
        input_directory = input_directory + "/"
    output = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            #if not root.endswith(exclusion):
            output.write(os.path.join(root[len(input_directory):], file))
            
    output.close()
    os.chdir(initial_dir)
