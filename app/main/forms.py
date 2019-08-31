from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, \
    SelectField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from app.models import User



def expert_users():
    return User.query.filter_by(expert=True)


def get_pk(obj):
    return str(obj)


class AskQuestionForm(FlaskForm):
    question = TextAreaField('Question')
    experts = QuerySelectField(
        query_factory=expert_users,
        allow_blank=True,
        get_pk=get_pk,
        get_label='username')
    submit = SubmitField('Ask')


class AnswerQuestionForm(FlaskForm):
    question = TextAreaField('Question')
    answer = TextAreaField('Answer')
    submit = SubmitField('Answer')

