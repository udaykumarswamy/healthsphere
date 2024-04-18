
import os
pdf_directory = '/Users/uday_kumar_swamy/Documents/work/spring-2024/IR/IR_project/HealthSphere/healthsphere/healthdata'



def list_files_in_directory(pdf_directory):
    """
    List file names in a directory.

    Args:
        directory (str): The path to the directory.

    Returns:
        list: A list of file names in the directory.
    """
    files = []
    for filename in os.listdir(pdf_directory):
        if os.path.isfile(os.path.join(pdf_directory, filename)):
            files.append(filename)
    return files


# List files in the directory
files_in_directory = list_files_in_directory(pdf_directory)

# Print the list of file names
print("Files in directory:")
for file_name in files_in_directory:
    print(file_name)
