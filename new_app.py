
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

class GitHubAutoUpdater:
    def __init__(self, github_username, repo_name, branch="main"):
        self.github_username = github_username  # Your GitHub username
        self.repo_name = repo_name  # Your repository name
        self.branch = branch
        self.base_url = f"https://api.github.com/repos/{github_username}/{repo_name}"
        self.raw_base_url = f"https://raw.githubusercontent.com/{github_username}/{repo_name}/{branch}"
        
    def get_latest_commit_id(self):
        """Check what's the latest version on GitHub"""
        try:
            url = f"{self.base_url}/commits/{self.branch}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()['sha'][:10]  # Short commit ID
        except:
            pass
        return None
    
    def get_current_version(self):
        """Check what version we have locally"""
        try:
            with open('current_version.txt', 'r') as f:
                return f.read().strip()
        except:
            return None
    
    def download_notebook(self, notebook_path):
        """Download a single notebook from GitHub"""
        try:
            # Convert local path to GitHub raw URL
            url = f"{self.raw_base_url}/{notebook_path}"
            
            print(f"Downloading: {notebook_path}")
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                # Create folder if it doesn't exist
                folder = os.path.dirname(notebook_path)
                if folder and not os.path.exists(folder):
                    os.makedirs(folder, exist_ok=True)
                
                # Save the file
                with open(notebook_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"✓ Updated: {notebook_path}")
                return True
            else:
                print(f"✗ Failed to download: {notebook_path}")
                return False
        except Exception as e:
            print(f"Error downloading {notebook_path}: {e}")
            return False
    
    def update_all_notebooks(self):
        """Download all your notebooks from GitHub"""
        
        # List of all your notebook files (you need to list them here)
        notebooks_to_update = [
            "Assortment/Assortment Duplicate.ipynb",
            "Assortment/Assortment Replacement Function.ipynb",
            "Assortment/Assortment Extracting Data.ipynb",
            "Pricing CBC/Pricing CBC Duplicate.ipynb",
            "Pricing CBC/Pricing CBC Replacement Function.ipynb",
            "Innovation CBC/Innovation CBC Duplicate.ipynb",
            "Innovation CBC/Innovation CBC Replacement Function.ipynb",
            "PPA/PPA Duplicate.ipynb",
            "PPA/PPA Replacement Function.ipynb",
            "PPA/PPA Extracting Data.ipynb",
            "Financials/Financials Duplicate.ipynb",
            "Financials/Financials Replacement Function.ipynb",
            "Financials/Financials Extracting Data.ipynb",
            "Pricing/Pricing Duplicate.ipynb",
            "Pricing/Pricing Replacement Function.ipynb",
            "Pricing/Pricing Extracting Data.ipynb",
            "Landscape/Landscape Duplicate.ipynb",
            "Landscape/Landscape Replacement Function.ipynb",
            "Landscape/Landscape Extracting Data.ipynb",
            "Promotion/Promotion Duplicate.ipynb",
            "Promotion/Promotion Replacement Function.ipynb",
            "Promotion/Promotion Extracting Data.ipynb"
        ]
        
        updated_count = 0
        for notebook in notebooks_to_update:
            if self.download_notebook(notebook):
                updated_count += 1
        
        return updated_count
    
    def save_current_version(self, version):
        """Remember what version we just downloaded"""
        with open('current_version.txt', 'w') as f:
            f.write(version)
    
    def check_and_update(self):
        """Main function: Check if updates available and download them"""
        print("Checking for updates...")
        
        latest_version = self.get_latest_commit_id()
        current_version = self.get_current_version()
        
        if latest_version and latest_version != current_version:
            print(f"New version available: {latest_version}")
            print("Downloading updates...")
            
            updated_count = self.update_all_notebooks()
            
            if updated_count > 0:
                self.save_current_version(latest_version)
                print(f"✓ Successfully updated {updated_count} files!")
                return True
            else:
                print("✗ Update failed")
                return False
        else:
            print("✓ Already up to date")
            return False

# Add this to your main Flask app file (new_app.py)

# At the top, add the updater
updater = GitHubAutoUpdater(
    github_username="PricingOne",  # Replace with your GitHub username
    repo_name="SlideAuto-tool",              # Replace with your repository name
    branch="main"                            # Your branch name
)

def auto_update_in_background():
    """Run this once when app starts"""
    try:
        updater.check_and_update()
    except Exception as e:
        print(f"Auto-update failed: {e}")

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
    # Check for updates when app starts (runs in background)
    update_thread = threading.Thread(target=auto_update_in_background, daemon=True)
    update_thread.start()
    
    # Start browser opening in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Run the Flask app
    app.run(debug=False, port=5001)

# if __name__ == "__main__":
#     # # Start browser opening in a separate thread
#     threading.Thread(target=open_browser).start()
#     # # Run the Flask app
#     app.run(debug=False, port=5001)