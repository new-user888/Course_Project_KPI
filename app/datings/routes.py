from app.datings import main
from flask import request, render_template, redirect, url_for, flash
from app.datings.models import Invitation
from flask_login import current_user, login_required
from app.auth.models import User
from app import db


@main.route('/')
def index():
    return redirect(url_for('main.main_page'))


@main.route('/main')
def main_page():
    return render_template('main_page.html')


@main.route('/my_profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(current_user.id)

    try:
        if request.method == 'POST':
            user.user_bio = request.form['about_you']
            if len(user.user_bio) > 100:
                raise AttributeError("Error: user bio info is too long")

            user.user_private = request.form['private']
            if len(user.user_private) > 100:
                raise AttributeError("Error: user private info is too long")

            db.session.commit()
            flash('Successfully changed info')
            return render_template('my_profile.html', user=user)

    except AttributeError as ae:
        flash(str(ae))

    return render_template('my_profile.html', user=user)


@main.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    invitations = Invitation.query.filter_by(receiver_id=current_user.id, state='pending').all()
    if request.method == 'POST':

        invitation_id = request.form.get('invitation_id')
        action = request.form.get('action')

        if invitation_id and action in ['accept', 'decline']:
            invitation = Invitation.query.get(invitation_id)
            if invitation:
                if action == 'accept':
                    invitation.state = 'accepted'

                elif action == 'decline':
                    invitation.state = 'declined'
                db.session.commit()

                return redirect(url_for('main.messages'))

    return render_template('messages.html', invitations=invitations)


@main.route('/search')
@login_required
def search_profiles():
    key = request.args.get('k')
    all_users = User.query.all()

    if not key:
        return render_template('search_profiles.html', users=all_users)

    users_to_display = []
    for user in all_users:
        if key in user.user_name or key in user.user_bio:
            users_to_display.append(user)

    return render_template('search_profiles.html', users=users_to_display)


@main.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_profile(user_id):
    if user_id == current_user.id:
        return redirect(url_for('main.profile'))

    user_to_display = User.query.filter_by(id=user_id).first()
    invitation_to_cur_user = Invitation.query.filter_by(sender_id=current_user.id, receiver_id=user_id).first()

    if request.method == 'POST' and not invitation_to_cur_user:
        invitation_to_cur_user = Invitation.create_invitation(sender_id=current_user.id, receiver_id=user_id, state='pending')

    return render_template('user_profile.html', user=user_to_display, invitation=invitation_to_cur_user)


@main.route('/friends')
@login_required
def friends():
    invitations_to_cur_user = Invitation.query.filter_by(receiver_id=current_user.id, state='accepted').all()
    invitations_to_other_user = Invitation.query.filter_by(sender_id=current_user.id, state='accepted').all()
    for invitation in invitations_to_other_user:
        invitation.sender_id, invitation.receiver_id = invitation.receiver_id, invitation.sender_id

    for inv_cur in invitations_to_cur_user:
        for inv_oth in invitations_to_other_user:
            if inv_cur.sender_id == inv_oth.sender_id:
                invitations_to_cur_user.remove(inv_cur)
                break

    inv_union = invitations_to_cur_user + invitations_to_other_user
    return render_template('friends.html', invitations=inv_union)
