from app import db
from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Question
from werkzeug.urls import url_parse
from app.main import bp
from app.main.forms import AskQuestionForm, AnswerQuestionForm


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    questions = Question.query.filter(Question.answer != None).all()
    return render_template(
        'index.html', questions=questions)


@bp.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    form = AskQuestionForm()
    if form.validate_on_submit():
        question_asked = form.question.data
        asker_id = current_user.id
        expert = form.experts.data.id
        question = Question(
            question=question_asked,
            asked_by_id=asker_id,
            expert_id=expert
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('ask.html', form=form)


@bp.route('/unanswered')
@login_required
def unanswered():
    if not current_user.expert:
        return redirect(url_for('main.index'))
    unanswered_questions = Question.query\
        .filter_by(expert_id=current_user.id)\
        .filter(Question.answer == None)\
        .all()
    return render_template(
        'unanswered.html', unanswered_questions=unanswered_questions)


@bp.route('/answer/<int:question_id>', methods=['GET', 'POST'])
@login_required
def answer(question_id):
    if not current_user.expert:
        return redirect(url_for('main.index'))
    question = Question.query.get_or_404(question_id)
    form = AnswerQuestionForm()
    if form.validate_on_submit():
        question.answer = form.answer.data
        db.session.commit()
        return redirect(url_for('main.unanswered'))
    return render_template(
        'answer.html', form=form, question=question)


@bp.route('/question/<int:question_id>')
@login_required
def question(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question.html', question=question)


@bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if not current_user.admin:
        return redirect(url_for('main.index'))
    users = User.query.all()
    return render_template('users.html', users=users)


@bp.route('/promote/<int:user_id>', methods=['GET', 'POST'])
@login_required
def promote(user_id):
    if not current_user.admin:
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(user_id)
    if user.expert:
        user.expert = False
    else:
        user.expert = True
    db.session.commit()
    return redirect(url_for('main.users'))
    return render_template('users.html', user=user)

