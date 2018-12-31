import os
import zipfile
import functools

from flask import *
from werkzeug.utils import secure_filename

import dao
import util

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='secret_key'
    app.config['UPLOAD_FOLDER']='/file'

    # ---------- auth ----------
    def login_required(function):
        @functools.wraps(function)
        def wrapped_function(**kwargs):
            if g.user is None:
                flash("Please log in.")
                return redirect(url_for("index"))
            return function(**kwargs)
        return wrapped_function

    @app.route('/login', methods=['POST'])
    def login():
        username=request.form['username']
        password=request.form['password']
        error=None

        user=dao.get_user_by_username(username)
        passwd_salt=util.get_password_salted(password)
        if user is None:
            error="User does not exist or password is not corrected."
        elif passwd_salt!=user['passwordSalted']:
            error="User does not exist or password is not corrected."

        if error is None:
            session['userId']=user['id']
            message='Login successfully.'

        if error is not None:
            flash(error)
        else:
            flash(message)
        return redirect(url_for('index'))

    @app.before_request
    def login_auto():
        userId=session.get('userId', None)

        if userId is None:
            g.user=None
        else:
            g.user=dao.get_user_by_id(userId)

    # ---------- main ----------
    @app.route('/')
    def index():
        files=dao.get_file_information()
        return render_template('index.html', files=files)

    @app.route('/download', methods=['POST'])
    @login_required
    def download():
        # data=json.loads(request.get_data().decode('utf-8'))
        # ids=data.get('id', None)
        ids=json.loads(request.form['ids']) 
        error=None  

        if ids==None or not isinstance(ids, list) or len(ids)==0:
            error="FileID is requried."

        if error is None:
            if len(ids)==1:
                directory, filename=dao.get_file_path(ids)

                if len(directory)==0:
                    error="File does not exist."
                else:
                    response = make_response(send_from_directory(directory[0], filename[0], as_attachment=True))
                    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename[0].encode().decode('latin-1'))
                    dao.add_download_time(ids)
                    return response
            else:
                dirs, names=dao.get_file_path(ids)

                if len(dirs)!=len(ids):
                    error="Some files do not exist."
                else:
                    with zipfile.ZipFile('/tmp/files.zip', 'w') as f:
                        for d, name in zip(dirs, names):
                            f.write(os.path.join(d, name), name)
                        f.close()
                    response = make_response(send_from_directory('/tmp', 'files.zip', as_attachment=True))
                    response.headers["Content-Disposition"] = "attachment; filename={}".format('files.zip'.encode().decode('latin-1'))
                    dao.add_download_time(ids)
                    return response
        flash(error)
        return redirect(url_for('index'))

    @app.route('/upload', methods=['POST'])
    @login_required
    def upload():
        error=None
        file = request.files['file']

        if file is None:
            error='No file part.'
        elif file.filename == '':
            error='No selected file.'

        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        dao.upload_file(app.config['UPLOAD_FOLDER'], filename)
        message='Upload successfully.'

        if error is not None:
            flash(error)
        else:
            flash(message)
        return redirect(url_for('index'))

    @app.route('/remove', methods=['POST'])
    @login_required
    def remove():
        ids=json.loads(request.form['ids']) 
        error=None  

        if ids==None or not isinstance(ids, list) or len(ids)==0:
            error="FileID is requried."

        if error is None:
            directory, filename=dao.get_file_path(ids)

            if len(directory)==0:
                error="File does not exist."
            else:
                dao.remove_file(ids)
                message='Remove successfully.'

        if error is not None:
            flash(error)
        else:
            flash(message)
        return redirect(url_for('index'))
    return app

app=create_app()

if __name__=='__main__':
    app.run('0.0.0.0', port='80', debug=True)
