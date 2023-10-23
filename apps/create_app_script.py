import sys
import os
import shutil

def create_app(app_name):
    
    app_name_capitalized = app_name[0].upper() + app_name[1:]
    app_name_lowercase = app_name[0].lower() + app_name[1:]
    
    tamplate_path = os.path.join(os.getcwd(),'tamplate')
    dest_path = app_name_capitalized

    shutil.copytree(tamplate_path, dest_path)

    for subdir, _, files in os.walk(dest_path):
            for file_name in files:
                file_path = os.path.join(subdir, file_name)
                with open(file_path, 'r') as file:
                    file_contents = file.read()

                file_contents = file_contents.replace("Appname", app_name_capitalized)
                file_contents = file_contents.replace("appname", app_name_lowercase)

                with open(file_path, 'w') as file:
                    file.write(file_contents)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        app_name = sys.argv[1]
        create_app(app_name)
    else:
        print("Proporciona el nombre de la aplicación como argumento.")