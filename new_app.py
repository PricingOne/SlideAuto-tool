
# from flask import Flask, render_template, flash, redirect, url_for,request 
# from flask_wtf import FlaskForm
# from wtforms import FileField, SubmitField, SelectField, StringField
# from flask_wtf.file import FileAllowed
# from wtforms.validators import DataRequired
# from werkzeug.utils import secure_filename
# import os
# import subprocess  # For running external scripts
# import nbformat
# from nbconvert.preprocessors import ExecutePreprocessor
# import time
# import webview
# import threading
# from nbclient import NotebookClient
# from jupyter_client import KernelManager
# import webbrowser 

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'supersecretkey'
# app.config['UPLOAD_FOLDER'] = 'static/files'
# ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

# class UploadFile(FlaskForm):
#     file = FileField("Parameters file")
#     submit = SubmitField("Run")
#     dropdown = SelectField("Which section do you want to create?", 
#                          choices=[('Choose...'), ('Pricing CBC'), ('Innovation CBC'), ('Assortment'), ('PPA'), ('Financials'),('Pricing'),('Landscape'),('Promotion')])
#     section = SelectField("What do you want to do?",
#                         choices=[('Both', 'Both'), ('Extract', 'Extract'), ('Duplicate', 'Duplicate')])

#     def validate(self, extra_validators=None):
#         if not self.submit.data:
#             return True

#         rv = super(UploadFile, self).validate(extra_validators)
        
#         if not rv:
#             return False

#         if self.dropdown.data == 'Choose...':
#             self.dropdown.errors.append('Please select a valid option.')
#             return False

#         return True

# def run_notebook(notebook_path, parameters):
#     notebook_path=str(os.getcwd())+'\\'+notebook_path
#     output_path=str(os.getcwd())+'\\'+'ok.ipynb'

#     with open(notebook_path, encoding='utf-8') as f:
#         nb = nbformat.read(f, as_version=4)
#         print('OPEND NOTEBOOK1')

#         # Replace parameters in the first cell
#         param_cell = nb.cells[0]
#         param_code = "\n".join([f"{key} = {repr(value)}" for key, value in parameters.items()])
#         param_cell.source = param_code

#     with open(notebook_path, 'w', encoding='utf-8') as f:
#         nbformat.write(nb, f)
#     print('Done Write the parameters')


#     # ep = ExecutePreprocessor(timeout=100 0, kernel_name='python3')
#     # ep.preprocess(nb, {'metadata': {'path': './'}})


#     print('notebook_path',notebook_path)
#     # command = [
#     #     "jupyter", "nbconvert",
#     #     "--to", "notebook",
#     #     "--execute",
#     #     # "--output", "C:\\Users\\khaled\\output\\Intro_assortment\\Assortment\\ok.ipynb",
#     #     output_path,
#     #     notebook_path
#     # ]
#     print('start to run')
#     command = [
#         "python", "-m", "nbconvert",
#         "--to", "notebook",
#         "--execute",
#         output_path,
#         notebook_path
#     ]

#     subprocess.run(command, shell=True,check=True)
#     print('end to run')


# @app.route("/", methods=['GET', 'POST'])
# def homepage():
#     """
#     The `homepage` function in Python handles file uploads, validates form data, processes the uploaded
#     file based on selected options, and redirects to the homepage.
#     :return: The `homepage()` function returns the rendered template 'index.html' with the form object.
#     """
#     form = UploadFile()
#     # time.sleep(5)
#     print(form.validate_on_submit(),'form.validate_on_submit()')
#     if form.validate_on_submit():
#         file = form.file.data
#         choice = form.dropdown.data
#         section = form.section.data
#         filename = secure_filename(file.filename)

#         if choice == 'Promotion':
#             slides_name = request.form.getlist('promotion_slides')

#         if '.' not in filename or filename.rsplit('.', 1)[1].strip().lower() not in ALLOWED_EXTENSIONS:
#             flash("Invalid file format.", "error")
#         else:
#             # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             # file_path = os.path.dirname(os.getcwd()).join(app.config['UPLOAD_FOLDER'])
#             # file_path = str(os.path.dirname(os.getcwd()))+"\\"+app.config['UPLOAD_FOLDER'] #container
#             file_path = str(os.getcwd())+'\\'+app.config['UPLOAD_FOLDER']+'\\'+filename #container

#             print('file_path',file_path,filename,choice)
#             # print(os.path.dirname(os.getcwd()))
#             file.save(file_path)
#             print('file_path',file_path,filename,choice)
#             #selected_option = form.dropdown.data

#             # Get the parameters based on the selected option
#             if choice in ['Pricing CBC', 'Innovation CBC', 'Assortment', 'PPA', 'Financials', 'Pricing', 'Landscape','Promotion']:
#                 # market = form.assortmentId.data 
#                 # print("🚀 ~ market:", market)
#                 # if not market:
#                 #     flash("Parameter assortmentId is required.", "error")
#                 # else:
#                 #     # Run the external script with the parameters
#                 #     # process_file(file_path, selected_option, innovationMarket=innovationMarket)
#                 #     print('done')
#                 # parameters = {'market':market,'f_path':file_path}
#                 parameters = {'f_path':file_path}
                
#                 if choice == 'Promotion':
#                     parameters['slides_name'] = slides_name

#                 print(5555555,file_path,parameters)

#                 flash("File has been uploaded and processed.", "success")
#                 #fileCode = {"Assortment":"Assortment\\Assortment Duplicate.ipynb"}
#                 fileCode = {choice: f"{choice}\\{choice} Duplicate.ipynb"}
#                 print(fileCode[choice])
#                 print(section,'section')
#                 if section =='Extract':
                    
#                     run_notebook(f"{choice}\\{choice} Extracting Data.ipynb", parameters)

#                 elif section =='Duplicate':
#                     print("🚀 ~ parameters:", parameters)
#                     run_notebook(f"{choice}\\{choice} Duplicate.ipynb", parameters)

#                 else:
#                     run_notebook(f"{choice}\\{choice} Extracting Data.ipynb", parameters)
#                     print( 'Done Extraction Start Duplicate')
#                     run_notebook(f"{choice}\\{choice} Duplicate.ipynb", parameters)
            
#         return redirect(url_for('homepage'))
#     else:
#         print(form.errors)  # This will show you the fields causing validation errors.


#     return render_template('new_index.html', form=form)


# def open_browser():
#     time.sleep(1.5)  # Wait for Flask to start
#     webbrowser.open('http://127.0.0.1:5001')

# if __name__ == "__main__":
#     # Start browser opening in a separate thread
#     threading.Thread(target=open_browser).start()
    
#     # Run the Flask app
#     app.run(debug=False, port=5001)

import requests
import os
import json
import threading
import time
from datetime import datetime, timedelta
import zipfile
import shutil

class SilentUpdater:
    def __init__(self, update_url, check_interval_hours=24):
        self.update_url = update_url  # Your server endpoint
        self.check_interval = check_interval_hours
        self.version_file = "app_version.json"
        self.updating = False
        
    def get_local_version_info(self):
        """Get current version and last check time"""
        try:
            if os.path.exists(self.version_file):
                with open(self.version_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            "version": "0.0.0",
            "last_check": None,
            "notebooks_hash": None
        }
    
    def should_check_for_updates(self):
        """Check if it's time to look for updates"""
        info = self.get_local_version_info()
        
        if not info.get("last_check"):
            return True
            
        last_check = datetime.fromisoformat(info["last_check"])
        return datetime.now() - last_check > timedelta(hours=self.check_interval)
    
    def check_updates_available(self):
        """Silently check if updates are available"""
        try:
            response = requests.get(self.update_url, timeout=10)
            if response.status_code == 200:
                remote_info = response.json()
                local_info = self.get_local_version_info()
                
                # Compare versions or hashes
                return (
                    remote_info.get("version") != local_info.get("version") or
                    remote_info.get("notebooks_hash") != local_info.get("notebooks_hash")
                ), remote_info
        except:
            pass
        return False, None
    
    def download_file(self, url, local_path):
        """Download a single file"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Create directories if needed
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return False
    
    def update_notebooks(self, remote_info):
        """Silently update all notebooks"""
        updated_files = []
        
        for notebook in remote_info.get("notebooks", []):
            local_path = notebook["path"]
            download_url = notebook["download_url"]
            
            if self.download_file(download_url, local_path):
                updated_files.append(local_path)
        
        # Update version info
        version_info = {
            "version": remote_info["version"],
            "notebooks_hash": remote_info["notebooks_hash"],
            "last_check": datetime.now().isoformat(),
            "last_update": datetime.now().isoformat(),
            "updated_files": updated_files
        }
        
        with open(self.version_file, 'w') as f:
            json.dump(version_info, f, indent=2)
        
        return len(updated_files)
    
    def background_update_check(self):
        """Run update check in background thread"""
        if self.updating or not self.should_check_for_updates():
            return
        
        self.updating = True
        
        try:
            has_updates, remote_info = self.check_updates_available()
            
            if has_updates and remote_info:
                print("Silently updating notebooks...")
                updated_count = self.update_notebooks(remote_info)
                print(f"Updated {updated_count} files silently")
            else:
                # Update last check time even if no updates
                info = self.get_local_version_info()
                info["last_check"] = datetime.now().isoformat()
                with open(self.version_file, 'w') as f:
                    json.dump(info, f, indent=2)
        
        finally:
            self.updating = False
    
    def start_background_updater(self):
        """Start the background update service"""
        def update_loop():
            while True:
                self.background_update_check()
                time.sleep(3600)  # Check every hour, but respects check_interval
        
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()

from flask import Flask, render_template, flash, redirect, url_for, request 
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, SelectField, StringField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os
import subprocess  # For running external scripts
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import time
import webview
import threading
from nbclient import NotebookClient
from jupyter_client import KernelManager
import webbrowser 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['PRICING_CBC_FOLDER'] = 'Pricing CBC/Pricing CBC Datasets Test'
app.config['INNOVATION_CBC_FOLDER'] = 'Innovation CBC/Innovation CBC Datasets Test'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

class UploadFile(FlaskForm):
    file = FileField("Parameters file")
    pricing_cbc_file = FileField("Pricing CBC Dataset file")  # New field for Pricing CBC
    innovation_cbc_file = FileField("Innovation CBC Dataset file") 
    submit = SubmitField("Run")
    dropdown = SelectField("Which section do you want to create?", 
                         choices=[('Choose...'), ('Pricing CBC'), ('Innovation CBC'), ('Assortment'), ('PPA'), ('Financials'),('Pricing'),('Landscape'),('Promotion')])
    section = SelectField("What do you want to do?",
                        choices=[('Both', 'Both'), ('Extract', 'Extract'), ('Duplicate', 'Duplicate')])

    def validate(self, extra_validators=None):
        if not self.submit.data:
            return True

        rv = super(UploadFile, self).validate(extra_validators)
        
        if not rv:
            return False

        if self.dropdown.data == 'Choose...':
            self.dropdown.errors.append('Please select a valid option.')
            return False
        

        # Additional validation for Pricing CBC
        if self.dropdown.data == 'Pricing CBC' and not self.pricing_cbc_file.data:
            self.pricing_cbc_file.errors.append('Pricing CBC dataset file is required.')
            return False
        
        if self.dropdown.data == 'Innovation CBC' and not self.innovation_cbc_file.data:
            self.innovation_cbc_file.errors.append('Pricing CBC dataset file is required.')
            return False
        

        return True

def run_notebook(notebook_path, parameters):
    notebook_path=str(os.getcwd())+'\\'+notebook_path
    output_path=str(os.getcwd())+'\\'+'ok.ipynb'

    with open(notebook_path, encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        print('OPEND NOTEBOOK1')

        # Replace parameters in the first cell
        param_cell = nb.cells[0]
        param_code = "\n".join([f"{key} = {repr(value)}" for key, value in parameters.items()])
        param_cell.source = param_code

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print('Done Write the parameters')

    print('notebook_path',notebook_path)
    print('start to run')
    command = [
        "python", "-m", "nbconvert",
        "--to", "notebook",
        "--execute",
        output_path,
        notebook_path
    ]

    subprocess.run(command, shell=True,check=True)
    print('end to run')


@app.route("/", methods=['GET', 'POST'])
def homepage():
    """
    The `homepage` function in Python handles file uploads, validates form data, processes the uploaded
    file based on selected options, and redirects to the homepage.
    :return: The `homepage()` function returns the rendered template 'index.html' with the form object.
    """
    form = UploadFile()
    print(form.validate_on_submit(),'form.validate_on_submit()')
    if form.validate_on_submit():
        file = form.file.data
        choice = form.dropdown.data
        section = form.section.data
        filename = secure_filename(file.filename)

        # Handle Pricing CBC specific file
        pricing_cbc_file = None
        pricing_cbc_path = None
        if choice == 'Pricing CBC' and form.pricing_cbc_file.data:
            slides_name = request.form.getlist('pricingCBC_slides')
            pricing_cbc_file = form.pricing_cbc_file.data
            pricing_cbc_filename = pricing_cbc_file.filename
            
            # Create Pricing CBC folder if it doesn't exist
            pricing_cbc_folder = os.path.join(os.getcwd(), app.config['PRICING_CBC_FOLDER'])
            if not os.path.exists(pricing_cbc_folder):
                os.makedirs(pricing_cbc_folder)
            
            pricing_cbc_path = os.path.join(pricing_cbc_folder, pricing_cbc_filename)
        
        innovation_cbc_file = None
        innovation_cbc_path = None
        if choice == 'Innovation CBC' and form.innovation_cbc_file.data:
            slides_name = request.form.getlist('innovationCBC_slides')
            innovation_cbc_file = form.innovation_cbc_file.data
            innovation_cbc_filename = innovation_cbc_file.filename
            
            # Create Pricing CBC folder if it doesn't exist
            innovation_cbc_folder = os.path.join(os.getcwd(), app.config['INNOVATION_CBC_FOLDER'])
            if not os.path.exists(innovation_cbc_folder):
                os.makedirs(innovation_cbc_folder)
            
            innovation_cbc_path = os.path.join(innovation_cbc_folder, innovation_cbc_filename)
        
        if choice == 'Promotion':
            slides_name = request.form.getlist('promotion_slides')
        
        if choice == 'Assortment':
            slides_name = request.form.getlist('assortment_slides')

        if choice == 'Financials':
            slides_name = request.form.getlist('financials_slides')
        
        if choice == 'Pricing':
            slides_name = request.form.getlist('pricing_slides')
        
        if choice == 'Landscape':
            slides_name = request.form.getlist('landscape_slides')
        
        if choice == 'PPA':
            slides_name = request.form.getlist('ppa_slides')

        if '.' not in filename or filename.rsplit('.', 1)[1].strip().lower() not in ALLOWED_EXTENSIONS:
            flash("Invalid file format.", "error")
        else:
            file_path = str(os.getcwd())+'\\'+app.config['UPLOAD_FOLDER']+'\\'+filename

            print('file_path',file_path,filename,choice)
            file.save(file_path)
            
            # Save Pricing CBC file if it exists
            if pricing_cbc_file and pricing_cbc_path:
                if '.' not in pricing_cbc_filename or pricing_cbc_filename.rsplit('.', 1)[1].strip().lower() not in ALLOWED_EXTENSIONS:
                    flash("Invalid Pricing CBC file format.", "error")
                    return redirect(url_for('homepage'))
                
                pricing_cbc_file.save(pricing_cbc_path)
                print('Pricing CBC file saved to:', pricing_cbc_path)

            print('file_path',file_path,filename,choice)

            if innovation_cbc_file and innovation_cbc_path:
                if '.' not in innovation_cbc_filename or innovation_cbc_filename.rsplit('.', 1)[1].strip().lower() not in ALLOWED_EXTENSIONS:
                    flash("Invalid Innovation CBC file format.", "error")
                    return redirect(url_for('homepage'))

                innovation_cbc_file.save(innovation_cbc_path)
                print('Innovation CBC file saved to:', innovation_cbc_path)

            # Get the parameters based on the selected option
            if choice in ['Pricing CBC', 'Innovation CBC', 'Assortment', 'PPA', 'Financials', 'Pricing', 'Landscape','Promotion']:
                parameters = {'f_path': file_path}
                
                # Add Pricing CBC specific parameters
                if choice == 'Pricing CBC' and pricing_cbc_path:
                    parameters['pricing_cbc_path'] = pricing_cbc_path
                    parameters['slides_name'] = slides_name
                
                if choice == 'Innovation CBC' and innovation_cbc_path:
                    parameters['innovation_cbc_path'] = innovation_cbc_path
                    parameters['slides_name'] = slides_name
                                
                if choice == 'Promotion':
                    parameters['slides_name'] = slides_name
                
                if choice == 'Assortment':
                    parameters['slides_name'] = slides_name
                
                if choice == 'Financials':
                    parameters['slides_name'] = slides_name
                
                if choice == 'Pricing':
                    parameters['slides_name'] = slides_name

                if choice == 'Landscape':
                    parameters['slides_name'] = slides_name
                
                if choice == 'PPA':
                    parameters['slides_name'] = slides_name

                print(5555555, file_path, parameters)

                flash("File has been uploaded and processed.", "success")
                fileCode = {choice: f"{choice}\\{choice} Duplicate.ipynb"}
                print(fileCode[choice])
                print(section,'section')
                
                if section =='Extract':
                    if choice == 'Pricing CBC' or choice == 'Innovation CBC':
                        run_notebook(f"{choice}\\{choice} Duplicate.ipynb", parameters)
                    else:
                        run_notebook(f"{choice}\\{choice} Extracting Data.ipynb", parameters)
                elif section =='Duplicate':
                    print("🚀 ~ parameters:", parameters)
                    run_notebook(f"{choice}\\{choice} Duplicate.ipynb", parameters)
                else:
                    if choice == 'Pricing CBC' or choice == 'Innovation CBC':
                        run_notebook(f"{choice}\\{choice} Duplicate.ipynb", parameters)
                    else:
                        run_notebook(f"{choice}\\{choice} Extracting Data.ipynb", parameters)
                        print( 'Done Extraction Start Duplicate')
                        run_notebook(f"{choice}\\{choice} Duplicate.ipynb", parameters)
            
        return redirect(url_for('homepage'))
    else:
        print(form.errors)  # This will show you the fields causing validation errors.

    return render_template('new_index.html', form=form)


def open_browser():
    time.sleep(1.5)  # Wait for Flask to start
    webbrowser.open('http://127.0.0.1:5001')

if __name__ == "__main__":
    # Start silent updater immediately
    updater.start_background_updater()
    
    # Do initial update check
    threading.Thread(target=updater.background_update_check, daemon=True).start()
    
    # Start browser
    threading.Thread(target=open_browser).start()
    
    # Run Flask app
    app.run(debug=False, port=5001)

    # # Start browser opening in a separate thread
    # threading.Thread(target=open_browser).start()
    
    # # Run the Flask app
    # app.run(debug=False, port=5001)