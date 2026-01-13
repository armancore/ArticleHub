# 📝 ArticleHub - Blog/Article Publishing Platform

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)

**A full-stack blog platform built with Flask, featuring user authentication, CRUD operations, and advanced search capabilities.**

[Live Demo](https://arman45678.pythonanywhere.com/) • [Report Bug](https://github.com/Arman-techiee/ArticleHub/issues) • [Request Feature](https://github.com/Arman-techiee/ArticleHub/issues)

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Screenshots](#-screenshots)
- [Database Schema](#-database-schema)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [API Routes](#-api-routes)
- [Bonus Features](#-bonus-features)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [Contact](#-contact)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Project Overview

### Course Information

- **Course:** Web Technology (BIT233)
- **Institution:** Texas College of Management & IT
- **Program:** Bachelor of Information Technology (BIT)
- **Academic Year:** Second Year / Third Semester
- **Project Type:** Full-Stack Blog/Article Publishing Platform

### Description

ArticleHub is a modern, responsive blog platform that allows users to create, share, and discuss articles across multiple categories. Built with Flask and SQLAlchemy, it demonstrates proficiency in full-stack web development, including user authentication, database design, and responsive UI/UX.

---

## ✨ Features

### Core Features

#### User Management

- ✅ **User Registration** - Create new accounts with validation
- ✅ **User Login/Logout** - Secure authentication with session management
- ✅ **Password Hashing** - Secure password storage using Werkzeug
- ✅ **User Profiles** - Customizable profile pages with bio
- ✅ **Edit Profile** - Update username, email, and bio

#### Blog Post Management (CRUD Operations)

- ✅ **Create Posts** - Write and publish articles with categories
- ✅ **Read Posts** - Browse all posts with pagination (6 per page)
- ✅ **Update Posts** - Edit your own articles
- ✅ **Delete Posts** - Remove your own articles
- ✅ **Post Categories** - 8 categories (Technology, Lifestyle, Travel, Food, Health, Business, Entertainment, Other)

#### Comment System

- ✅ **Add Comments** - Comment on any post
- ✅ **View Comments** - See all comments on posts
- ✅ **Delete Comments** - Remove your own comments

#### Search & Filter

- ✅ **Advanced Search** - Search by keyword, category, author, date range
- ✅ **Category Filter** - Filter posts by category on homepage
- ✅ **Sort Options** - Sort by newest, oldest, or most popular (by comments)
- ✅ **Search Results Count** - Display number of matching results

#### User Experience

- ✅ **Responsive Design** - Mobile, tablet, and desktop support
- ✅ **User Dashboard** - Personal dashboard showing user's posts
- ✅ **Flash Messages** - User feedback for all actions
- ✅ **Pagination** - Efficient browsing with 6 posts per page
- ✅ **Error Pages** - Custom 404 and 500 error pages

### Security Features

- 🔒 **Password Hashing** - Werkzeug security for password encryption
- 🔒 **CSRF Protection** - Flask-WTF CSRF tokens on all forms
- 🔒 **Login Required** - Protected routes for authenticated users
- 🔒 **Authorization** - Users can only edit/delete their own content
- 🔒 **Form Validation** - Server-side and client-side validation
- 🔒 **SQL Injection Prevention** - SQLAlchemy ORM protection

---

## 🛠️ Technology Stack

### Frontend

| Technology      | Version | Purpose                   |
| --------------- | ------- | ------------------------- |
| HTML5           | -       | Semantic markup structure |
| CSS3            | -       | Custom styling            |
| Bootstrap       | 5.3     | Responsive framework      |
| JavaScript      | ES6+    | Client-side interactivity |
| Bootstrap Icons | 1.10    | Icon library              |

### Backend

| Technology       | Version | Purpose                         |
| ---------------- | ------- | ------------------------------- |
| Python           | 3.8+    | Programming language            |
| Flask            | 3.0.0   | Web framework                   |
| Flask-SQLAlchemy | 3.0.5   | ORM for database operations     |
| Flask-Login      | 0.6.3   | User session management         |
| Flask-WTF        | 1.2.1   | Form handling & CSRF protection |
| WTForms          | 3.1.1   | Form validation                 |
| Werkzeug         | 3.0.1   | Security utilities              |

### Database

| Technology | Purpose                         |
| ---------- | ------------------------------- |
| SQLite     | Lightweight relational database |
| SQLAlchemy | Python ORM                      |

### Development Tools

| Tool           | Purpose                      |
| -------------- | ---------------------------- |
| Git            | Version control              |
| GitHub         | Code hosting & collaboration |
| VS Code        | Code editor                  |
| PythonAnywhere | Deployment platform          |

---

## 📸 Screenshots

### Homepage

![Homepage](https://via.placeholder.com/800x500/0d6efd/ffffff?text=Homepage+-+Browse+All+Posts)

_Browse all blog posts with category filters and pagination_

### Post Detail Page

![Post Detail](https://via.placeholder.com/800x500/198754/ffffff?text=Post+Detail+-+Read+%26+Comment)

_Read full articles and engage in discussions through comments_

### User Dashboard

![Dashboard](https://via.placeholder.com/800x500/ffc107/000000?text=Dashboard+-+Manage+Your+Posts)

_Manage all your posts in one place - edit or delete with ease_

### Advanced Search

![Advanced Search](https://via.placeholder.com/800x500/dc3545/ffffff?text=Advanced+Search+-+Find+Posts+Fast)

_Powerful search with filters: keyword, category, author, date range, and sorting_

### User Profile

![User Profile](https://via.placeholder.com/800x500/6f42c1/ffffff?text=User+Profile+-+View+Author+Info)

_View user profiles and all their published articles_

### Registration Page

![Registration](https://via.placeholder.com/800x500/fd7e14/ffffff?text=Registration+-+Create+Account)

_Secure user registration with form validation_

### Mobile Responsive

![Mobile View](https://via.placeholder.com/400x700/20c997/ffffff?text=Mobile+Responsive+Design)

_Fully responsive design works on all devices_

---

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
│      USER       │          │      POST       │          │    COMMENT      │
├─────────────────┤          ├─────────────────┤          ├─────────────────┤
│ id (PK)         │──┐       │ id (PK)         │──┐       │ id (PK)         │
│ username        │  │       │ title           │  │       │ content         │
│ email           │  │       │ content         │  │       │ created_at      │
│ password_hash   │  │       │ category        │  │       │ post_id (FK)    │──┐
│ bio             │  │       │ created_at      │  │       │ user_id (FK)    │──│─┐
│ created_at      │  │       │ updated_at      │  │       └─────────────────┘  │ │
└─────────────────┘  │       │ author_id (FK)  │──│──────────────────────────┘ │
                     │       └─────────────────┘  │                            │
                     │                            │                            │
                     └────────────────────────────┘────────────────────────────┘

Relationships:
• User → Posts (One-to-Many): One user can create many posts
• User → Comments (One-to-Many): One user can write many comments
• Post → Comments (One-to-Many): One post can have many comments
```

### Database Tables

#### Users Table

| Column          | Type        | Constraints            | Description                |
| --------------- | ----------- | ---------------------- | -------------------------- |
| `id`            | Integer     | PRIMARY KEY            | Unique user identifier     |
| `username`      | String(80)  | UNIQUE, NOT NULL       | User's display name        |
| `email`         | String(120) | UNIQUE, NOT NULL       | User's email address       |
| `password_hash` | String(200) | NOT NULL               | Hashed password            |
| `bio`           | Text        | DEFAULT: 'No bio yet.' | User biography             |
| `created_at`    | DateTime    | DEFAULT: NOW           | Account creation timestamp |

#### Posts Table

| Column       | Type        | Constraints             | Description             |
| ------------ | ----------- | ----------------------- | ----------------------- |
| `id`         | Integer     | PRIMARY KEY             | Unique post identifier  |
| `title`      | String(200) | NOT NULL                | Post title              |
| `content`    | Text        | NOT NULL                | Post content/body       |
| `category`   | String(50)  | NOT NULL                | Post category           |
| `author_id`  | Integer     | FOREIGN KEY → users.id  | Post author             |
| `created_at` | DateTime    | DEFAULT: NOW            | Post creation timestamp |
| `updated_at` | DateTime    | DEFAULT: NOW, ON UPDATE | Last update timestamp   |

#### Comments Table

| Column       | Type     | Constraints            | Description               |
| ------------ | -------- | ---------------------- | ------------------------- |
| `id`         | Integer  | PRIMARY KEY            | Unique comment identifier |
| `content`    | Text     | NOT NULL               | Comment text              |
| `post_id`    | Integer  | FOREIGN KEY → posts.id | Associated post           |
| `user_id`    | Integer  | FOREIGN KEY → users.id | Comment author            |
| `created_at` | DateTime | DEFAULT: NOW           | Comment timestamp         |

---

## 🚀 Installation & Setup

### Prerequisites

Ensure you have the following installed:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **pip** - Python package manager (comes with Python)
- **Git** - [Download](https://git-scm.com/downloads)
- **Virtual Environment** (recommended)

### Step-by-Step Installation

#### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Arman-techiee/ArticleHub.git

# Navigate to project directory
cd ArticleHub
```

#### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

#### 4. Initialize Database

The database will be created automatically when you first run the application.

```bash
# (Optional) Add sample data
python add_sample_data.py
```

This will create:

- 3 sample users
- 5 sample posts
- Sample login credentials displayed in terminal

#### 5. Run the Application

```bash
# Start Flask development server
python app.py
```

#### 6. Access the Application

Open your web browser and navigate to:

```
http://127.0.0.1:5000
```

---

## 📖 Usage Guide

### For New Users

#### 1. Register an Account

1. Click **"Register"** in the navigation bar
2. Fill in:
   - Username (3-80 characters)
   - Email address (valid format)
   - Password (minimum 6 characters)
   - Confirm password
3. Click **"Sign Up"**
4. You'll be redirected to login page

#### 2. Login

1. Click **"Login"** in the navigation bar
2. Enter your email and password
3. Click **"Login"**
4. You'll be redirected to homepage

#### 3. Create a Post

1. After logging in, click **"New Post"** in navigation
2. Fill in:
   - **Title** (5-200 characters)
   - **Category** (select from dropdown)
   - **Content** (minimum 20 characters)
3. Click **"Publish Post"**
4. Your post appears in your dashboard

#### 4. Browse Posts

1. **Homepage**: View all posts with pagination
2. **Filter by Category**: Click category buttons at top
3. **Read Post**: Click "Read More" button
4. **View Author**: Click username to see profile

#### 5. Comment on Posts

1. Open any post detail page
2. Scroll to comments section
3. Type your comment (1-500 characters)
4. Click **"Post Comment"**

#### 6. Search Posts

1. Click search icon in navigation
2. Enter search criteria:
   - **Keywords**: Search in titles and content
   - **Category**: Filter by category
   - **Author**: Filter by username
   - **Date Range**: From/to dates
   - **Sort**: Newest, oldest, or most popular
3. Click **"Search"**

#### 7. Edit Profile

1. Click **"Profile"** in navigation
2. Click **"Edit Profile"** button
3. Update your information
4. Click **"Update Profile"**

### For Existing Users

#### Manage Your Posts

1. Go to **"Dashboard"** from navigation
2. View all your posts
3. **Edit**: Click "Edit" button
4. **Delete**: Click "Delete" button (with confirmation)

#### Interact with Community

1. **Comment** on posts you find interesting
2. **View profiles** of other authors
3. **Search** for specific topics
4. **Follow** discussions through comments

---

## 📁 Project Structure

```
ArticleHub/
│
├── app.py                      # Main Flask application
├── models.py                   # Database models (User, Post, Comment)
├── forms.py                    # Flask-WTF forms (Registration, Login, Post, Comment, Profile)
├── requirements.txt            # Python dependencies
├── add_sample_data.py          # Script to add sample data
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html              # Base template (navigation, footer)
│   ├── index.html             # Homepage with post listing
│   ├── register.html          # User registration page
│   ├── login.html             # User login page
│   ├── dashboard.html         # User dashboard (manage posts)
│   ├── create_post.html       # Create new post page
│   ├── edit_post.html         # Edit existing post page
│   ├── post_detail.html       # Single post view with comments
│   ├── profile.html           # User profile page
│   ├── edit_profile.html      # Edit profile page
│   ├── search.html            # Advanced search page
│   ├── about.html             # About page
│   ├── 404.html               # Custom 404 error page
│   └── 500.html               # Custom 500 error page
│
├── static/                     # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css          # Custom CSS styles
│   └── js/
│       └── main.js            # Custom JavaScript
│
└── instance/                   # Instance folder (auto-created)
    └── blog.db                # SQLite database file
```

---

## 🛣️ API Routes

### Public Routes (No Authentication Required)

| Method | Route                    | Description             |
| ------ | ------------------------ | ----------------------- |
| GET    | `/` or `/index`          | Homepage with all posts |
| GET    | `/register`              | User registration page  |
| POST   | `/register`              | Process registration    |
| GET    | `/login`                 | User login page         |
| POST   | `/login`                 | Process login           |
| GET    | `/post/<int:post_id>`    | View single post        |
| GET    | `/profile/<int:user_id>` | View user profile       |
| GET    | `/search`                | Advanced search page    |
| GET    | `/about`                 | About page              |

### Protected Routes (Authentication Required)

| Method | Route                              | Description            |
| ------ | ---------------------------------- | ---------------------- |
| GET    | `/logout`                          | Logout user            |
| GET    | `/dashboard`                       | User dashboard         |
| GET    | `/post/create`                     | Create post page       |
| POST   | `/post/create`                     | Process post creation  |
| GET    | `/post/<int:post_id>/edit`         | Edit post page         |
| POST   | `/post/<int:post_id>/edit`         | Process post update    |
| POST   | `/post/<int:post_id>/delete`       | Delete post            |
| POST   | `/post/<int:post_id>/comment`      | Add comment            |
| POST   | `/comment/<int:comment_id>/delete` | Delete comment         |
| GET    | `/profile/edit`                    | Edit profile page      |
| POST   | `/profile/edit`                    | Process profile update |

---

## 🎁 Bonus Features

### Implemented Advanced Features

#### 1. Advanced Search & Filters (+3 Bonus Marks)

- **Keyword Search**: Search in post titles and content
- **Category Filter**: Filter by specific categories
- **Author Filter**: Find posts by username
- **Date Range Filter**: Filter by publication date
- **Sort Options**:
  - Newest first (default)
  - Oldest first
  - Most popular (by comment count)
- **Result Count**: Display number of matching results
- **Active Filters Display**: Show currently applied filters

**Implementation Highlights:**

- Complex SQLAlchemy queries with multiple filters
- Join operations for author filtering
- Aggregate functions for popularity sorting
- Date parsing and validation
- Clean, intuitive UI with Bootstrap form controls

---

### Browser Compatibility

Tested on:

- ✅ Google Chrome (Latest)
- ✅ Mozilla Firefox (Latest)
- ✅ Microsoft Edge (Latest)
- ✅ Safari (Latest)

---

## 🚀 Deployment

### Deploying to PythonAnywhere

#### 1. Create Account

1. Go to [PythonAnywhere](https://www.pythonanywhere.com/)
2. Sign up for a free account

#### 2. Upload Code

```bash
# Option A: Upload via Git
git clone https://github.com/Arman-techiee/ArticleHub.git

# Option B: Upload ZIP file via web interface
```

#### 3. Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 articlehub-env
pip install -r requirements.txt
```

#### 4. Configure WSGI File

```python
import sys
path = '/home/yourusername/ArticleHub'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

#### 5. Set Up Database

```bash
cd ArticleHub
python add_sample_data.py
```

#### 6. Configure Web App

- Set source directory
- Set working directory
- Reload web app

#### 7. Access Your Site

```
https://yourusername.pythonanywhere.com
```

### Environment Variables (Production)

Create `.env` file:

```env
SECRET_KEY=your-secret-key-here
SQLALCHEMY_DATABASE_URI=sqlite:///blog.db
FLASK_ENV=production
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create Feature Branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit Changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to Branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Write clear commit messages
- Add comments to complex code
- Update documentation for new features
- Test thoroughly before submitting

---

---

## 📞 Contact

**Developer:** Arman Khan

- **GitHub:** [@Arman-techiee](https://github.com/Arman-techiee)
- **Project Link:** [https://github.com/Arman-techiee/ArticleHub](https://github.com/Arman-techiee/ArticleHub)
- **Live Demo:** [https://arman45678.pythonanywhere.com/](https://arman45678.pythonanywhere.com/)

**Institution:** Texas College of Management & IT

- **Course:** Web Technology (BIT233)
- **Instructor:** Mr. Ashish Gautam (PhD Scholar)

---

## 🙏 Acknowledgments

### Technologies & Frameworks

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Bootstrap](https://getbootstrap.com/) - Frontend framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Flask-Login](https://flask-login.readthedocs.io/) - User session management
- [WTForms](https://wtforms.readthedocs.io/) - Form validation

### Resources

- [Flask Documentation](https://flask.palletsprojects.com/en/3.0.x/)
- [W3Schools](https://www.w3schools.com/) - HTML/CSS/JavaScript reference
- [MDN Web Docs](https://developer.mozilla.org/) - Web development documentation
- [Bootstrap Icons](https://icons.getbootstrap.com/) - Icon library
- [PythonAnywhere](https://www.pythonanywhere.com/) - Hosting platform

### Inspiration

- Various blog platforms for UI/UX inspiration
- Open source projects on GitHub
- Texas College of Management & IT curriculum

---

## 📊 Project Statistics

- **Total Lines of Code:** ~2,500+
- **Python Files:** 4
- **HTML Templates:** 14
- **Database Tables:** 3
- **Routes:** 20+
- **Features:** 30+
- **Development Time:** 40+ hours
- **GitHub Commits:** 22+

---

## 🎓 Learning Outcomes Achieved

1. ✅ **Understand Web Technologies** - Mastered HTML, CSS, JavaScript, and Flask
2. ✅ **Database Design** - Created normalized database schema with relationships
3. ✅ **User Authentication** - Implemented secure login system with password hashing
4. ✅ **CRUD Operations** - Built complete Create, Read, Update, Delete functionality
5. ✅ **Responsive Design** - Created mobile-first responsive layouts
6. ✅ **Form Validation** - Implemented both client and server-side validation
7. ✅ **Version Control** - Used Git for version control throughout development
8. ✅ **Deployment** - Successfully deployed application to production

---

## 🔮 Future Enhancements

Potential features for future versions:

### High Priority

- [ ] Admin panel for content moderation
- [ ] User profile pictures and post images
- [ ] Email notifications for comments
- [ ] Rich text editor for post content
- [ ] Post tags and multi-category support

### Medium Priority

- [ ] User followers/following system
- [ ] Post bookmarks/favorites
- [ ] Social media sharing buttons
- [ ] RSS feed for posts
- [ ] Post view counter

### Low Priority

- [ ] Dark mode theme
- [ ] Multi-language support
- [ ] REST API endpoints
- [ ] Mobile app version
- [ ] Real-time notifications

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

Made with ❤️ by [Arman](https://github.com/Arman-techiee)

**Texas College of Management & IT | BIT Second Year**

---

© 2026 ArticleHub. All Rights Reserved.

</div>
