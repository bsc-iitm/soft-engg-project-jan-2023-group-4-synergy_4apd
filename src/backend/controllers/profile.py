from flask import render_template, request, redirect
from flask_security import login_required, current_user
from backend import app
from backend.database import db
from backend.forms import ProfileForm

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(request.form)

    if request.method == 'GET':
        form.name.data = current_user.name
        form.designation.data = current_user.designation
        form.bio.data = current_user.bio
        form.phone.data = current_user.phone

    if request.method == 'POST' and form.validate():
        current_user.name = form.name.data
        current_user.designation = form.designation.data
        current_user.bio = form.bio.data
        current_user.phone = form.phone.data

        db.session.commit()
        return redirect('/')

    return render_template('dialogs/create_update_dialog.html', form=form,
                           form_title='Your profile', primary_button_text='Save')
