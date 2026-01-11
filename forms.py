from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

# Registration Form
class RegistrationForm(FlaskForm):
    """
    Form for new user registration
    """
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')


# Login Form
class LoginForm(FlaskForm):
    """
    Form for user login
    """
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    submit = SubmitField('Login')


# Post Form - Used for both creating and editing posts
class PostForm(FlaskForm):
    """
    Form for creating and editing blog posts
    """
    title = StringField('Title', 
                       validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Content', 
                           validators=[DataRequired(), Length(min=20)])
    category = SelectField('Category', 
                          choices=[
                              ('Technology', 'Technology'),
                              ('Lifestyle', 'Lifestyle'),
                              ('Travel', 'Travel'),
                              ('Food', 'Food'),
                              ('Health', 'Health'),
                              ('Business', 'Business'),
                              ('Entertainment', 'Entertainment'),
                              ('Other', 'Other')
                          ],
                          validators=[DataRequired()])
    submit = SubmitField('Publish Post')


# Comment Form
class CommentForm(FlaskForm):
    """
    Form for adding comments to posts
    """
    content = TextAreaField('Add a Comment', 
                           validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Post Comment')


# Profile Form
class ProfileForm(FlaskForm):
    """
    Form for updating user profile
    """
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio', 
                       validators=[Length(max=500)])
    submit = SubmitField('Update Profile')