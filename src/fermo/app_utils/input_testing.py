from flask import (
    flash,
    redirect,
    current_app,  # allows to access the config elements
    request,
    url_for
)
from werkzeug.utils import secure_filename
import os


def allowed_file(filename):
    ''' Returns boolean for valid filenames and allowed extensions

    Parameters
    ----------
    filename : 'str'

    Notes
    -----
    Check for dot in filename and allowed extensions as specified in the
    config file
    '''
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in \
        current_app.config.get('ALLOWED_EXTENSION')


def check_file(inputID, file_format):
    '''

    Parameters
    ----------
    inputID: 'str'
    file_format: 'str'

    Notes
    -----
    Checks if the file was succesfully transmitted via request, if a filename
    provided, and if it has the right format.
    inputID must be taken from the corresponding html file.
    '''
    if inputID not in request.files:
        flash('Something went wrong, please try again')
        return redirect(request.url)
    file = request.files[inputID]
    if file.filename == '':
        flash('No file was loaded. Please upload a session-file.')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if filename.endswith(file_format):
            try:
                file.save(os.path.join(current_app.config.get(
                    'UPLOAD_FOLDER'), filename))
            except FileNotFoundError:
                print("file or folder didn't exist, \
                        so the uploaded file couldn't be saved")
            return redirect(url_for('views.inspect_uploaded_file',
                                    filename=filename))
        else:
            flash(f"File must be a {file_format}-file!")
            return redirect(request.url)
    else:
        print('something went wrong with the file upload of element:', inputID)
