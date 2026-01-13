from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Post, Comment
from forms import RegistrationForm, LoginForm, PostForm, CommentForm, ProfileForm
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = '4302bbe147749caf128d261630e5c67a2e7a9e545ac1d3e86813abe591cd9d5e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


# Create database tables
with app.app_context():
    db.create_all()


# ============ HOME PAGE ROUTE ============
@app.route('/')
@app.route('/index')
def index():
    """
    Homepage - Display all blog posts with pagination
    Supports category filtering
    """
    # Get page number from URL (default is 1)
    page = request.args.get('page', 1, type=int)
    
    # Get category filter from URL
    category = request.args.get('category', None)
    
    # Query posts based on category
    if category:
        posts = Post.query.filter_by(category=category)\
                         .order_by(Post.created_at.desc())\
                         .paginate(page=page, per_page=6, error_out=False)
    else:
        posts = Post.query.order_by(Post.created_at.desc())\
                         .paginate(page=page, per_page=6, error_out=False)
    
    return render_template('index.html', posts=posts, selected_category=category)


# ============ REGISTRATION ROUTE ============
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration page
    """
    # If user is already logged in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    
    # Process form submission
    if form.validate_on_submit():
        # Create new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # Add to database
        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
    
    return render_template('register.html', form=form)


# ============ LOGIN ROUTE ============
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page
    """
    # If user is already logged in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    # Process form submission
    if form.validate_on_submit():
        # Find user by email
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to page user was trying to access, or home
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('login.html', form=form)


# ============ LOGOUT ROUTE ============
@app.route('/logout')
@login_required
def logout():
    """
    Logout current user
    """
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


# ============ USER DASHBOARD ROUTE ============
@app.route('/dashboard')
@login_required
def dashboard():
    """
    User dashboard - Shows user's own posts
    """
    # Get current user's posts
    posts = Post.query.filter_by(author_id=current_user.id)\
                     .order_by(Post.created_at.desc()).all()
    
    return render_template('dashboard.html', posts=posts)


# ============ CREATE POST ROUTE ============
@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """
    Create new blog post
    """
    form = PostForm()
    
    # Process form submission
    if form.validate_on_submit():
        # Create new post
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            author_id=current_user.id
        )
        
        # Add to database
        try:
            db.session.add(post)
            db.session.commit()
            flash('Your post has been published!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
    
    return render_template('create_post.html', form=form)


# ============ EDIT POST ROUTE ============
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """
    Edit existing blog post
    Only the author can edit their own posts
    """
    # Get post or return 404
    post = Post.query.get_or_404(post_id)
    
    # Check if current user is the author
    if post.author_id != current_user.id:
        flash('You can only edit your own posts.', 'danger')
        return redirect(url_for('index'))
    
    form = PostForm()
    
    # Process form submission
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('post_detail', post_id=post.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
    
    # Pre-fill form with existing data
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
    
    return render_template('edit_post.html', form=form, post=post)


# ============ DELETE POST ROUTE ============
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """
    Delete blog post
    Only the author can delete their own posts
    """
    post = Post.query.get_or_404(post_id)
    
    # Check if current user is the author
    if post.author_id != current_user.id:
        flash('You can only delete your own posts.', 'danger')
        return redirect(url_for('index'))
    
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('dashboard'))


# ============ POST DETAIL ROUTE ============
@app.route('/post/<int:post_id>')
def post_detail(post_id):
    """
    View single post with comments
    """
    post = Post.query.get_or_404(post_id)
    
    # Get comments for this post
    comments = Comment.query.filter_by(post_id=post_id)\
                           .order_by(Comment.created_at.desc()).all()
    
    # Comment form (only for logged-in users)
    form = CommentForm() if current_user.is_authenticated else None
    
    return render_template('post_detail.html', post=post, comments=comments, form=form)


# ============ ADD COMMENT ROUTE ============
@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """
    Add comment to a post
    """
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        # Create new comment
        comment = Comment(
            content=form.content.data,
            post_id=post_id,
            user_id=current_user.id
        )
        
        try:
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('post_detail', post_id=post_id))


# ============ DELETE COMMENT ROUTE ============
@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """
    Delete comment
    Only the comment author can delete their own comments
    """
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post_id
    
    # Check if current user is the comment author
    if comment.user_id != current_user.id:
        flash('You can only delete your own comments.', 'danger')
        return redirect(url_for('post_detail', post_id=post_id))
    
    try:
        db.session.delete(comment)
        db.session.commit()
        flash('Your comment has been deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('post_detail', post_id=post_id))


# ============ USER PROFILE ROUTE ============
@app.route('/profile/<int:user_id>')
def profile(user_id):
    """
    View user profile and their posts
    """
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(author_id=user_id)\
                     .order_by(Post.created_at.desc()).all()
    
    return render_template('profile.html', user=user, posts=posts)


# ============ EDIT PROFILE ROUTE ============
@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Edit user profile
    """
    form = ProfileForm()
    
    if form.validate_on_submit():
        # Check if username is taken by another user
        if form.username.data != current_user.username:
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Username already taken.', 'danger')
                return redirect(url_for('edit_profile'))
        
        # Check if email is taken by another user
        if form.email.data != current_user.email:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already registered.', 'danger')
                return redirect(url_for('edit_profile'))
        
        # Update user profile
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        
        try:
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('profile', user_id=current_user.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
    
    # Pre-fill form with current data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    
    return render_template('edit_profile.html', form=form)


# ============ SEARCH ROUTE ============
@app.route('/search')
def search():
    """
    Advanced search for posts with multiple filters
    """
    # Get search parameters from URL
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '')
    author = request.args.get('author', '').strip()
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    sort_by = request.args.get('sort', 'newest')
    
    # Start with base query
    posts_query = Post.query
    
    # Filter by keyword (title or content)
    if query:
        posts_query = posts_query.filter(
            (Post.title.contains(query)) | (Post.content.contains(query))
        )
    
    # Filter by category
    if category and category != 'All':
        posts_query = posts_query.filter_by(category=category)
    
    # Filter by author username
    if author:
        posts_query = posts_query.join(User).filter(User.username.contains(author))
    
    # Filter by date range
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            posts_query = posts_query.filter(Post.created_at >= date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            # Add one day to include the entire end date
            from datetime import timedelta
            date_to_obj = date_to_obj + timedelta(days=1)
            posts_query = posts_query.filter(Post.created_at < date_to_obj)
        except ValueError:
            pass
    
    # Apply sorting
    if sort_by == 'oldest':
        posts_query = posts_query.order_by(Post.created_at.asc())
    elif sort_by == 'popular':
        # Sort by number of comments (most popular)
        from sqlalchemy import func
        posts_query = posts_query.outerjoin(Comment)\
                                 .group_by(Post.id)\
                                 .order_by(func.count(Comment.id).desc())
    else:  # newest (default)
        posts_query = posts_query.order_by(Post.created_at.desc())
    
    # Execute query
    posts = posts_query.all()
    
    # Count results
    result_count = len(posts)
    
    return render_template('search.html', 
                         posts=posts, 
                         query=query,
                         selected_category=category,
                         selected_author=author,
                         date_from=date_from,
                         date_to=date_to,
                         sort_by=sort_by,
                         result_count=result_count)


# ============ ABOUT PAGE ROUTE ============
@app.route('/about')
def about():
    """
    About page
    """
    return render_template('about.html')


# ============ FAVICON ROUTE ============
@app.route('/favicon.ico')
def favicon():
    """
    Handle favicon requests to prevent 404 errors
    Returns 204 No Content
    """
    return '', 204


# ============ ERROR HANDLERS ============
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500


# ============ RUN APPLICATION ============
if __name__ == '__main__':
    app.run(debug=True)
