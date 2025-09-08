from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, SelectField, StringField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os
import pandas as pd
import nbformat 
from nbconvert.preprocessors import ExecutePreprocessor

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

class UploadFile(FlaskForm):
    file = FileField("Parameters file")
    submit = SubmitField("Run")
    dropdown = SelectField("Which section do you want to create?", 
                         choices=[('Choose...'), ('Pricing CBC'), ('Innovation CBC'), ('Assortment'), ('PPA'), ('Financials')])
    
    market = StringField("Parameter 1")
    currency = StringField("Parameter 2")
    pricingPlus = StringField("Parameter 3")
    pricingMinus = StringField("Parameter 4")
    innovationMarket = StringField("Parameter 5")
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

        # Only validate if form is submitted with file
        if self.file.data:
            if self.dropdown.data == 'Pricing CBC':
                if not all([self.market.data, self.currency.data, self.pricingPlus.data, self.pricingMinus.data]):
                    self.market.errors.append('All parameters for "Pricing CBC" must be filled.')
                    return False
            elif self.dropdown.data == 'Innovation CBC':
                if not self.innovationMarket.data:
                    self.innovationMarket.errors.append('Parameter 5 (Market) is required for "Innovation CBC".')
                    return False
            # elif self.dropdown.data in ['Assortment', 'PPA']:
            #     print('ppa or assort')
            #     if not self.market.data:
            #         print('error')
            #         self.market.errors.append(f'Market parameter is required for "{self.dropdown.data}".')
            #         return False

        return True
def run_notebook(notebook_path: str, parameters: dict) -> bool:
    """
    Execute a Jupyter notebook with specified parameters using the jupyter nbconvert command line tool.
    
    Args:
        notebook_path (str): Path to the notebook to execute
        parameters (dict): Dictionary of parameters to inject into the first cell
        
    Returns:
        bool: True if execution was successful, False otherwise
    """
    try:
        print(f"Starting notebook execution: {notebook_path}")
        
        # Validate notebook path
        if not os.path.exists(notebook_path):
            print(f"Notebook not found: {notebook_path}")
            return False
        
        # Get the absolute paths
        base_dir = os.getcwd()
        notebook_abs_path = os.path.abspath(notebook_path)
        notebook_dir = os.path.dirname(notebook_abs_path)
        
        print(f"Notebook directory: {notebook_dir}")
        
        # Read the notebook
        try:
            with open(notebook_abs_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
                print("Successfully read notebook")
        except Exception as e:
            print(f"Failed to read notebook: {str(e)}")
            return False
        
        # Process notebook cells to handle dependencies
        for idx, cell in enumerate(nb.cells):
            if cell.cell_type == 'code' and '%run' in cell.source:
                print(f"Processing cell {idx} with %run command")
                new_source_lines = []
                for line in cell.source.split('\n'):
                    if '%run' in line:
                        # Handle different notebook dependencies
                        if 'general_functions' in line:
                            dep_path = os.path.join(base_dir, 'general_functions', 'generalFunctions.ipynb')
                            if not os.path.exists(dep_path):
                                print(f"Dependency not found: {dep_path}")
                                return False
                            new_source_lines.append(f'%run "{dep_path}"')
                            print(f"Updated path for general_functions: {dep_path}")
                        elif 'Assortment Replacement Function' in line:
                            dep_path = os.path.join(notebook_dir, 'Assortment Replacement Function.ipynb')
                            if not os.path.exists(dep_path):
                                print(f"Dependency not found: {dep_path}")
                                return False
                            new_source_lines.append(f'%run "{dep_path}"')
                            print(f"Updated path for Assortment Replacement: {dep_path}")
                        else:
                            new_source_lines.append(line)
                    else:
                        new_source_lines.append(line)
                cell.source = '\n'.join(new_source_lines)
        
        # Set parameters in first cell
        if len(nb.cells) == 0:
            print("Notebook contains no cells")
            return False
            
        param_cell = nb.cells[0]
        param_lines = []
        for key, value in parameters.items():
            param_lines.append(f"{key} = {repr(value)}")
        param_cell.source = "\n".join(param_lines)
        print("Parameters set in first cell")
        
        # Save the modified notebook
        modified_notebook_path = notebook_abs_path + '.modified.ipynb'
        with open(modified_notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"Saved modified notebook to {modified_notebook_path}")
        
        # Create a backup of the original notebook
        backup_path = notebook_abs_path + '.bak'
        import shutil
        shutil.copy2(notebook_abs_path, backup_path)
        print(f"Created backup at {backup_path}")
        
        # Use jupyter nbconvert to execute the notebook
        import subprocess
        import sys
        
        print("Using jupyter nbconvert to execute notebook")
        
        try:
            # Change to the notebook directory to ensure correct context
            original_dir = os.getcwd()
            os.chdir(notebook_dir)
            
            # Run jupyter nbconvert with execute flag
            cmd = ['jupyter', 'nbconvert', '--to', 'notebook', '--execute', 
                  '--output', os.path.basename(notebook_abs_path),
                  os.path.basename(modified_notebook_path)]
            
            print(f"Running command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            # Change back to original directory
            os.chdir(original_dir)
            
            # Check execution result
            print(f"nbconvert stdout: {result.stdout}")
            print(f"nbconvert stderr: {result.stderr}")
            
            if result.returncode != 0:
                print(f"nbconvert execution failed with return code {result.returncode}")
                # Restore from backup
                shutil.copy2(backup_path, notebook_abs_path)
                return False
                
        except Exception as e:
            print(f"Failed to execute notebook via nbconvert: {str(e)}")
            # Restore from backup
            shutil.copy2(backup_path, notebook_abs_path)
            return False
        finally:
            # Clean up the temporary notebook
            if os.path.exists(modified_notebook_path):
                os.remove(modified_notebook_path)
            # Change back to original directory if needed
            if os.getcwd() != original_dir:
                os.chdir(original_dir)
        
        # Clean up backup if everything succeeded
        if os.path.exists(backup_path):
            os.remove(backup_path)
            print("Removed backup file")
            
        print(f"Successfully executed notebook: {notebook_path}")
        return True
        
    except Exception as e:
        print(f"Error executing notebook: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
# import os
# import nbformat
# from nbconvert.preprocessors import ExecutePreprocessor
# from typing import Dict, Optional

# def run_notebook(notebook_path: str, parameters: Dict[str, any]) -> bool:
#     """
#     Execute a Jupyter notebook with specified parameters and handle notebook dependencies.
    
#     Args:
#         notebook_path (str): Path to the notebook to execute
#         parameters (Dict[str, any]): Dictionary of parameters to inject into the first cell
        
#     Returns:
#         bool: True if execution was successful, False otherwise
        
#     Raises:
#         FileNotFoundError: If notebook_path or dependent notebooks don't exist
#         ValueError: If notebook format is invalid
#     """
#     try:
#         # Validate inputs
#         if not os.path.exists(notebook_path):
#             raise FileNotFoundError(f"Notebook not found: {notebook_path}")
#         if not isinstance(parameters, dict):
#             raise ValueError("Parameters must be provided as a dictionary")

#         # Get the absolute paths
#         base_dir = os.getcwd()
#         notebook_abs_path = os.path.abspath(notebook_path)
#         notebook_dir = os.path.dirname(notebook_abs_path)

#         # Read the notebook with proper error handling
#         try:
#             with open(notebook_abs_path, 'r', encoding='utf-8') as f:
#                 nb = nbformat.read(f, as_version=4)
#         except Exception as e:
#             raise ValueError(f"Failed to read notebook: {str(e)}")

#         # Track modified cells for logging
#         modified_cells = []
        
#         # Modify cells with %run commands
#         for idx, cell in enumerate(nb.cells):
#             if cell.cell_type == 'code' and '%run' in cell.source:
#                 new_source_lines = []
#                 for line in cell.source.split('\n'):
#                     if '%run' in line:
#                         # Handle different notebook dependencies
#                         if 'general_functions' in line:
#                             new_path = os.path.join(base_dir, 'general_functions', 'generalFunctions.ipynb')
#                             if not os.path.exists(new_path):
#                                 raise FileNotFoundError(f"Required dependency not found: {new_path}")
#                             new_source_lines.append(f'%run "{new_path}"')
#                             modified_cells.append(f"Cell {idx}: Updated general_functions path")
#                         elif 'Assortment Replacement Function' in line:
#                             new_path = os.path.join(notebook_dir, 'Assortment Replacement Function.ipynb')
#                             if not os.path.exists(new_path):
#                                 raise FileNotFoundError(f"Required dependency not found: {new_path}")
#                             new_source_lines.append(f'%run "{new_path}"')
#                             modified_cells.append(f"Cell {idx}: Updated Assortment Replacement path")
#                         else:
#                             new_source_lines.append(line)
#                     else:
#                         new_source_lines.append(line)
#                 cell.source = '\n'.join(new_source_lines)

#         # Set parameters in first cell with type checking
#         if len(nb.cells) == 0:
#             raise ValueError("Notebook contains no cells")
            
#         param_cell = nb.cells[0]
#         param_lines = []
#         for key, value in parameters.items():
#             if not isinstance(key, str):
#                 raise ValueError(f"Parameter key must be string, got {type(key)}")
#             param_lines.append(f"{key} = {repr(value)}")
#         param_cell.source = "\n".join(param_lines)
#         modified_cells.append("Cell 0: Injected parameters")

#         # Execute notebook with proper kernel specification and error handling
#         ep = ExecutePreprocessor(timeout=3000, kernel_name='python3')
#         try:
#             # Add error handling for cell execution
#             try:
#                 ep.preprocess(nb, {'metadata': {'path': notebook_dir}})
#             except Exception as e:
#                 print(f"Execution failed. Notebook state:", nb)
#                 print(type(nb))
#                 print(type(ep))
#                 print(f"Error type: {type(e)}")
#                 print(f"Error message: {str(e)}")
#                 raise
#             # Check for execution errors in cells
#             for cell in nb.cells:
#                 if cell.cell_type == 'code' and hasattr(cell, 'outputs'):
#                     for output in cell.outputs:
#                         if output.output_type == 'error':
#                             error_name = output.get('ename', 'Unknown error')
#                             error_value = output.get('evalue', 'No error message')
#                             traceback = output.get('traceback', [])
#                             raise Exception(f"{error_name}: {error_value}\n{''.join(traceback)}")
                            
#         except Exception as e:
#             print(f"Notebook execution failed. Error details:\n{str(e)}")
#             if hasattr(e, '__traceback__'):
#                 import traceback
#                 print("Full traceback:")
#                 traceback.print_exc()
#             return False
        
#         # Save executed notebook with backup
#         backup_path = notebook_abs_path + '.bak'
#         if os.path.exists(notebook_abs_path):
#             os.rename(notebook_abs_path, backup_path)
            
#         try:
#             with open(notebook_abs_path, 'w', encoding='utf-8') as f:
#                 nbformat.write(nb, f)
#         except Exception as e:
#             # Restore from backup if save fails
#             if os.path.exists(backup_path):
#                 os.rename(backup_path, notebook_abs_path)
#             raise IOError(f"Failed to save notebook: {str(e)}")
            
#         # Clean up backup
#         if os.path.exists(backup_path):
#             os.remove(backup_path)

#         print(f"Successfully executed notebook with modifications:\n" + "\n".join(modified_cells))
#         return True

#     except Exception as e:
#         error_msg = f"Error executing notebook: {str(e)}"
#         print(error_msg)  # Log the error
#         if 'flash' in globals():  # Only call flash if it exists
#             flash(error_msg, "error")
#         return False
# def run_notebook(notebook_path, parameters):
#     try:
#         # Get the absolute paths
#         base_dir = os.getcwd()
#         notebook_abs_path = os.path.abspath(notebook_path)
#         notebook_dir = os.path.dirname(notebook_abs_path)
#         print(notebook_abs_path)
#         print(notebook_dir)
#         # Read the notebook
#         with open(notebook_abs_path) as f:
#             print(f)
#             nb = nbformat.read(f, as_version=4)
        
#         # Modify the cell that's causing issues
#         for cell in nb.cells:
#             if cell.cell_type == 'code' and '%run' in cell.source:
#                 # Update the paths to use absolute paths
#                 new_source_lines = []
#                 for line in cell.source.split('\n'):
#                     if '%run' in line:
#                         if 'general_functions' in line:
#                             new_path = os.path.join(base_dir, 'general_functions', 'generalFunctions.ipynb')
#                             print(new_path)
#                             new_source_lines.append(f'%run "{new_path}"')
#                             print(new_source_lines)
#                         elif 'Assortment Replacement Function' in line:
#                             new_path = os.path.join(notebook_dir, 'Assortment Replacement Function.ipynb')
#                             print(new_path)
#                             new_source_lines.append(f'%run "{new_path}"')
#                             print(new_source_lines)
#                         else:
#                             new_source_lines.append(line)
#                     else:
#                         new_source_lines.append(line)
#                 cell.source = '\n'.join(new_source_lines)

#         # Set parameters in first cell
#         param_cell = nb.cells[0]
#         param_code = "\n".join([f"{key} = {repr(value)}" for key, value in parameters.items()])
#         param_cell.source = param_code

#         # Execute notebook with the correct working directory
#         ep = ExecutePreprocessor(timeout=3000, kernel_name='python3')
#         ep.preprocess(nb, {'metadata': {'path': notebook_dir}})
#         print(ep)

#         # Save executed notebook
#         with open(notebook_abs_path, 'w') as f:
#             nbformat.write(nb, f)
            
#         return True
#     except Exception as e:
#         flash(f"Error executing notebook: {str(e)}", "error")
#         return False
    
# def run_notebook(notebook_path, parameters):
#     try:
#         notebook_path = os.path.join(os.getcwd(), notebook_path)
#         with open(notebook_path) as f:
#             nb = nbformat.read(f, as_version=4)

#         # Set parameters in first cell
#         param_cell = nb.cells[0]
#         param_code = "\n".join([f"{key} = {repr(value)}" for key, value in parameters.items()])
#         param_cell.source = param_code

#         # Execute notebook
#         ep = ExecutePreprocessor(timeout=3000, kernel_name='python3')
#         ep.preprocess(nb, {'metadata': {'path': '/'}})

#         # Save executed notebook
#         with open(notebook_path, 'w') as f:
#             nbformat.write(nb, f)
            
#         return True
#     except Exception as e:
#         flash(f"Error executing notebook: {str(e)}", "error")
#         return False

@app.route("/", methods=['GET', 'POST'])
def homepage():
    form = UploadFile()
    if form.validate_on_submit():
        file = form.file.data
        choice = form.dropdown.data
        process_type = form.section.data
        filename = secure_filename(file.filename)
        if '.' not in filename or filename.rsplit('.', 1)[1].strip().lower() not in ALLOWED_EXTENSIONS:
            flash("Invalid file format.", "error")
        else:
            file_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], filename)
            file_path = os.path.join(os.getcwd(), filename)
            file.save(file_path)
            
            # Get parameters based on selected option
            parameters = {'f_path': file_path}
            
            if choice == 'Pricing CBC':
                parameters.update({
                    'market': form.market.data,
                    'currency': form.currency.data,
                    'pricingPlus': form.pricingPlus.data,
                    'pricingMinus': form.pricingMinus.data
                })
            if choice == 'Innovation CBC':
                parameters['market'] = form.innovationMarket.data
            

            # Process based on section type and choice
            success = True
            if choice in ['Assortment', 'PPA']:
                if process_type in ['Both', 'Extract']:
                    #notebook_path = f'{choice}\\{choice} Extracting Data.ipynb'
                    notebook_path = os.path.join(choice, f'{choice} Extracting Data.ipynb')
                    success = run_notebook(notebook_path, parameters)
                    print(success)
                    if success:
                        flash(f"{choice} data extraction completed successfully!", "success")
                    
                if process_type in ['Both', 'Duplicate'] and success:
                    #notebook_path = f'{choice}\\{choice} Duplicate.ipynb'
                    notebook_path = os.path.join(choice, f'{choice} Duplicate.ipynb')
                    success = run_notebook(notebook_path, parameters)
                    if success:
                        flash(f"{choice} duplication completed successfully!", "success")

            if not success:
                flash("An error occurred during processing.", "error")

        return redirect(url_for('homepage'))
    
    return render_template('index.html', form=form)

if __name__ == "__main__":
    #os.makedirs(os.path.join(os.getcwd(), 'static/files'), exist_ok=True)
    app.run(debug=True, port=5001)


    
# def run_notebook(notebook_path: str, parameters: dict) -> bool:
#     # [Keeping the run_notebook function as is since it works for all cases]
#     # This is a placeholder; use your preferred version of run_notebook from the original code
#     try:
#         print(f"Starting notebook execution: {notebook_path}")
#         if not os.path.exists(notebook_path):
#             print(f"Notebook not found: {notebook_path}")
#             return False
        
#         base_dir = os.getcwd()
#         notebook_abs_path = os.path.abspath(notebook_path)
#         notebook_dir = os.path.dirname(notebook_abs_path)
        
#         with open(notebook_abs_path, 'r', encoding='utf-8') as f:
#             nb = nbformat.read(f, as_version=4)
        
#         for idx, cell in enumerate(nb.cells):
#             if cell.cell_type == 'code' and '%run' in cell.source:
#                 new_source_lines = []
#                 for line in cell.source.split('\n'):
#                     if '%run' in line:
#                         if 'general_functions' in line:
#                             dep_path = os.path.join(base_dir, 'general_functions', 'generalFunctions.ipynb')
#                             if not os.path.exists(dep_path):
#                                 print(f"Dependency not found: {dep_path}")
#                                 return False
#                             new_source_lines.append(f'%run "{dep_path}"')
#                         elif 'Assortment Replacement Function' in line:
#                             dep_path = os.path.join(notebook_dir, 'Assortment Replacement Function.ipynb')
#                             if not os.path.exists(dep_path):
#                                 print(f"Dependency not found: {dep_path}")
#                                 return False
#                             new_source_lines.append(f'%run "{dep_path}"')
#                         else:
#                             new_source_lines.append(line)
#                     else:
#                         new_source_lines.append(line)
#                 cell.source = '\n'.join(new_source_lines)
        
#         if len(nb.cells) == 0:
#             print("Notebook contains no cells")
#             return False
            
#         param_cell = nb.cells[0]
#         param_lines = [f"{key} = {repr(value)}" for key, value in parameters.items()]
#         param_cell.source = "\n".join(param_lines)
        
#         modified_notebook_path = notebook_abs_path + '.modified.ipynb'
#         with open(modified_notebook_path, 'w', encoding='utf-8') as f:
#             nbformat.write(nb, f)
        
#         import shutil
#         backup_path = notebook_abs_path + '.bak'
#         shutil.copy2(notebook_abs_path, backup_path)
        
#         import subprocess
#         original_dir = os.getcwd()
#         os.chdir(notebook_dir)
        
#         cmd = ['jupyter', 'nbconvert', '--to', 'notebook', '--execute', 
#                '--output', os.path.basename(notebook_abs_path),
#                os.path.basename(modified_notebook_path)]
        
#         result = subprocess.run(cmd, capture_output=True, text=True)
#         os.chdir(original_dir)
        
#         if result.returncode != 0:
#             print(f"nbconvert execution failed: {result.stderr}")
#             shutil.copy2(backup_path, notebook_abs_path)
#             return False
        
#         if os.path.exists(modified_notebook_path):
#             os.remove(modified_notebook_path)
#         if os.path.exists(backup_path):
#             os.remove(backup_path)
        
#         print(f"Successfully executed notebook: {notebook_path}")
#         return True
#     except Exception as e:
#         print(f"Error executing notebook: {str(e)}")
#         return False



# def homepage():
#     form = UploadFile()
#     if form.validate_on_submit():
#         file = form.file.data
#         choice = form.dropdown.data
#         process_type = form.section.data
#         filename = secure_filename(file.filename)
#         if '.' not in filename or filename.rsplit('.', 1)[1].strip().lower() not in ALLOWED_EXTENSIONS:
#             flash("Invalid file format.", "error")
#         else:
#             file_path = os.path.join(os.getcwd(), filename)
#             file.save(file_path)
            
#             parameters = {'f_path': file_path}
            
#             # Process all options the same way
#             success = True
#             if choice in ['Pricing CBC', 'Innovation CBC', 'Assortment', 'PPA', 'Financials']:
#                 if process_type in ['Both', 'Extract']:
#                     notebook_path = os.path.join(choice, f'{choice} Extracting Data.ipynb')
#                     success = run_notebook(notebook_path, parameters)
#                     if success:
#                         flash(f"{choice} data extraction completed successfully!", "success")
                    
#                 if process_type in ['Both', 'Duplicate'] and success:
#                     notebook_path = os.path.join(choice, f'{choice} Duplicate.ipynb')
#                     success = run_notebook(notebook_path, parameters)
#                     if success:
#                         flash(f"{choice} duplication completed successfully!", "success")

#             if not success:
#                 flash("An error occurred during processing.", "error")

#         return redirect(url_for('homepage'))
    
#     return render_template('new_index.html', form=form)