from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.account.forms import ProfileForm, PasswordForm
from app.account import bp

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    
    if form.validate_on_submit():
        try:
            # 更新用户信息
            if form.first_name.data:
                current_user.first_name = form.first_name.data
            if form.last_name.data:
                current_user.last_name = form.last_name.data
            if form.email.data:
                current_user.email = form.email.data
            if form.password.data:
                current_user.password_hash = generate_password_hash(form.password.data)
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('account.profile'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile. Please try again.', 'error')
    
    # 预填充表单数据
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.email.data = current_user.email
    
    return render_template('account/profile.html', 
                         title='Profile',
                         form=form)

@bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    password_form = PasswordForm()
    if password_form.validate_on_submit():
        if check_password_hash(current_user.password_hash, password_form.current_password.data):
            current_user.password_hash = generate_password_hash(password_form.new_password.data)
            db.session.commit()
            flash('密码已更新！', 'success')
        else:
            flash('当前密码错误！', 'danger')
    return redirect(url_for('account.profile'))
