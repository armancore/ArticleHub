from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Post, Comment
from forms import RegistrationForm, LoginForm, PostForm, CommentForm, ProfileForm
from datetime import datetime, timedelta
from functools import wraps

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


# ============ ADMIN DECORATOR ============
def admin_required(f):
    """Decorator that restricts a route to admin users only."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('login'))
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# Create database tables
with app.app_context():
    db.create_all()

    # ── Auto-create a default admin account if none exists ──
    if not User.query.filter_by(is_admin=True).first():
        admin = User(
            username='admin',
            email='admin@articlehub.com',
            bio='Platform administrator.',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Default admin account created: admin@articlehub.com / admin123")


# ============ HOME PAGE ROUTE ============
@app.route('/')
@app.route('/index')
def index():
    """Homepage - Display all blog posts with pagination"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)

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
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')

    return render_template('register.html', form=form)


# ============ LOGIN ROUTE ============
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html', form=form)


# ============ LOGOUT ROUTE ============
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


# ============ USER DASHBOARD ROUTE ============
@app.route('/dashboard')
@login_required
def dashboard():
    posts = Post.query.filter_by(author_id=current_user.id)\
                     .order_by(Post.created_at.desc()).all()
    return render_template('dashboard.html', posts=posts)


# ============ CREATE POST ROUTE ============
@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            author_id=current_user.id
        )
        try:
            db.session.add(post)
            db.session.commit()
            flash('Your post has been published!', 'success')
            return redirect(url_for('dashboard'))
        except Exception:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')

    return render_template('create_post.html', form=form)


# ============ EDIT POST ROUTE ============
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Allow admins to edit any post
    if post.author_id != current_user.id and not current_user.is_admin:
        flash('You can only edit your own posts.', 'danger')
        return redirect(url_for('index'))

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.updated_at = datetime.utcnow()
        try:
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('post_detail', post_id=post.id))
        except Exception:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category

    return render_template('edit_post.html', form=form, post=post)


# ============ DELETE POST ROUTE ============
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author_id != current_user.id and not current_user.is_admin:
        flash('You can only delete your own posts.', 'danger')
        return redirect(url_for('index'))

    try:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully.', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')

    return redirect(url_for('dashboard'))


# ============ POST DETAIL ROUTE ============
@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id)\
                           .order_by(Comment.created_at.desc()).all()
    form = CommentForm() if current_user.is_authenticated else None
    return render_template('post_detail.html', post=post, comments=comments, form=form)


# ============ ADD COMMENT ROUTE ============
@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            post_id=post_id,
            user_id=current_user.id
        )
        try:
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added!', 'success')
        except Exception:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')

    return redirect(url_for('post_detail', post_id=post_id))


# ============ DELETE COMMENT ROUTE ============
@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post_id

    if comment.user_id != current_user.id and not current_user.is_admin:
        flash('You can only delete your own comments.', 'danger')
        return redirect(url_for('post_detail', post_id=post_id))

    try:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted.', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')

    return redirect(url_for('post_detail', post_id=post_id))


# ============ USER PROFILE ROUTE ============
@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(author_id=user_id)\
                     .order_by(Post.created_at.desc()).all()
    return render_template('profile.html', user=user, posts=posts)


# ============ EDIT PROFILE ROUTE ============
@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if form.username.data != current_user.username:
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already taken.', 'danger')
                return redirect(url_for('edit_profile'))

        if form.email.data != current_user.email:
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already registered.', 'danger')
                return redirect(url_for('edit_profile'))

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        try:
            db.session.commit()
            flash('Profile updated!', 'success')
            return redirect(url_for('profile', user_id=current_user.id))
        except Exception:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio

    return render_template('edit_profile.html', form=form)


# ============ SEARCH ROUTE ============
@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '')
    author = request.args.get('author', '').strip()
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    sort_by = request.args.get('sort', 'newest')

    posts_query = Post.query

    if query:
        posts_query = posts_query.filter(
            (Post.title.contains(query)) | (Post.content.contains(query))
        )
    if category and category != 'All':
        posts_query = posts_query.filter_by(category=category)
    if author:
        posts_query = posts_query.join(User).filter(User.username.contains(author))
    if date_from:
        try:
            posts_query = posts_query.filter(Post.created_at >= datetime.strptime(date_from, '%Y-%m-%d'))
        except ValueError:
            pass
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
            posts_query = posts_query.filter(Post.created_at < date_to_obj)
        except ValueError:
            pass

    if sort_by == 'oldest':
        posts_query = posts_query.order_by(Post.created_at.asc())
    elif sort_by == 'popular':
        from sqlalchemy import func
        posts_query = posts_query.outerjoin(Comment)\
                                 .group_by(Post.id)\
                                 .order_by(func.count(Comment.id).desc())
    else:
        posts_query = posts_query.order_by(Post.created_at.desc())

    posts = posts_query.all()
    return render_template('search.html',
                           posts=posts,
                           query=query,
                           selected_category=category,
                           selected_author=author,
                           date_from=date_from,
                           date_to=date_to,
                           sort_by=sort_by,
                           result_count=len(posts))


# ============ ABOUT PAGE ROUTE ============
@app.route('/about')
def about():
    return render_template('about.html')


# ============ FAVICON ROUTE ============
@app.route('/favicon.ico')
def favicon():
    return '', 204


# ======================================================
# ==================== ADMIN ROUTES ====================
# ======================================================

@app.route('/admin')
@admin_required
def admin_panel():
    """Main admin dashboard — lists all users, posts and comments."""
    users    = User.query.order_by(User.created_at.desc()).all()
    posts    = Post.query.order_by(Post.created_at.desc()).all()
    comments = Comment.query.order_by(Comment.created_at.desc()).all()

    one_week_ago = datetime.utcnow() - timedelta(days=7)
    recent_posts = Post.query.filter(Post.created_at >= one_week_ago).count()

    return render_template(
        'admin.html',
        users=users,
        posts=posts,
        comments=comments,
        total_users=len(users),
        total_posts=len(posts),
        total_comments=len(comments),
        recent_posts=recent_posts,
        now=datetime.utcnow()
    )


@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    """Admin: delete any user (and cascade-delete their posts/comments)."""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot delete your own admin account.", 'danger')
        return redirect(url_for('admin_panel'))
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'User "{user.username}" and all their content have been deleted.', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
    return redirect(url_for('admin_panel'))


@app.route('/admin/delete-post/<int:post_id>', methods=['POST'])
@admin_required
def admin_delete_post(post_id):
    """Admin: delete any post."""
    post = Post.query.get_or_404(post_id)
    try:
        db.session.delete(post)
        db.session.commit()
        flash(f'Post "{post.title}" has been deleted.', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
    return redirect(url_for('admin_panel'))


@app.route('/admin/delete-comment/<int:comment_id>', methods=['POST'])
@admin_required
def admin_delete_comment(comment_id):
    """Admin: delete any comment."""
    comment = Comment.query.get_or_404(comment_id)
    try:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted.', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
    return redirect(url_for('admin_panel'))


@app.route('/admin/delete-all-comments', methods=['POST'])
@admin_required
def admin_delete_all_comments():
    """Admin: nuke every comment in the database."""
    try:
        Comment.query.delete()
        db.session.commit()
        flash('All comments have been deleted.', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
    return redirect(url_for('admin_panel'))


# ============ ERROR HANDLERS ============
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# ============ RUN APPLICATION ============
if __name__ == '__main__':
    app.run(debug=True)