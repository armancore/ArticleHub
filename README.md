# 📝 ArticleHub - Blog/Article Publishing Platform

A full-stack web application built with Flask, allowing users to create, read, update, and delete blog posts with user authentication and commenting features.

![ArticleHub Banner](https://via.placeholder.com/800x200/0d6efd/ffffff?text=ArticleHub+-+Share+Your+Stories)

## 🎯 Project Overview

**Course:** Web Technology (BIT233)  
**Institution:** Texas College of Management & IT  
**Program:** Bachelor of Information Technology (BIT)  
**Academic Year:** Second Year / Third Semester  
**Project Type:** Blog/Article Publishing Platform

## ✨ Features

### Core Features

- ✅ User Registration and Authentication
- ✅ User Login/Logout with Session Management
- ✅ Password Hashing for Security
- ✅ Create, Read, Update, Delete (CRUD) Blog Posts
- ✅ Comment System on Posts
- ✅ User Profile Pages
- ✅ User Dashboard
- ✅ Search Functionality
- ✅ Category-based Post Filtering
- ✅ Responsive Design (Mobile, Tablet, Desktop)
- ✅ Form Validation (Client-side and Server-side)
- ✅ Pagination (6 posts per page)
- ✅ Flash Messages for User Feedback

### Security Features

- 🔒 Password Hashing using Werkzeug
- 🔒 CSRF Protection using Flask-WTF
- 🔒 Login Required Decorators for Protected Routes
- 🔒 Users can only edit/delete their own posts and comments

## 🛠️ Technology Stack

### Frontend

- **HTML5** - Semantic markup
- **CSS3** - Custom styling
- **Bootstrap 5** - Responsive framework
- **JavaScript** - Client-side interactivity
- **Bootstrap Icons** - Icon library

### Backend

- **Python 3.8+** - Programming language
- **Flask 2.3.0** - Web framework
- **Flask-SQLAlchemy** - ORM for database
- **Flask-Login** - User session management
- **Flask-WTF** - Form handling and validation
- **Jinja2** - Template engine

### Database

- **SQLite** - Lightweight database

## 📁 Project Structure

```
ArticleHub/
│
├── app.py                 # Main Flask application
├── models.py             # Database models (User, Post, Comment)
├── forms.py              # Flask-WTF forms
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
├── README.md            # Project documentation
│
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Homepage
│   ├── register.html    # Registration page
│   ├── login.html       # Login page
│   ├── dashboard.html   # User dashboard
│   ├── create_post.html # Create post page
│   ├── edit_post.html   # Edit post page
│   ├── post_detail.html # Post detail page
│   ├── profile.html     # User profile page
│   ├── edit_profile.html # Edit profile page
│   ├── search.html      # Search results page
│   └── about.html       # About page
│
├── static/              # Static files
│   ├── css/
│   │   └── style.css    # Custom CSS
│   └── js/
│       └── main.js      # Custom JavaScript
│
└── instance/            # Database folder (auto-created)
    └── blog.db          # SQLite database
```

## 🗄️ Database Schema

### Users Table

| Column        | Type     | Constraints            |
| ------------- | -------- | ---------------------- |
| id            | Integer  | Primary Key            |
| username      | String   | Unique, Not Null       |
| email         | String   | Unique, Not Null       |
| password_hash | String   | Not Null               |
| bio           | Text     | Default: 'No bio yet.' |
| created_at    | DateTime | Default: Now           |

### Posts Table

| Column     | Type     | Constraints                  |
| ---------- | -------- | ---------------------------- |
| id         | Integer  | Primary Key                  |
| title      | String   | Not Null                     |
| content    | Text     | Not Null                     |
| category   | String   | Not Null                     |
| author_id  | Integer  | Foreign Key → users.id       |
| created_at | DateTime | Default: Now                 |
| updated_at | DateTime | Default: Now, On Update: Now |

### Comments Table

| Column     | Type     | Constraints            |
| ---------- | -------- | ---------------------- |
| id         | Integer  | Primary Key            |
| content    | Text     | Not Null               |
| post_id    | Integer  | Foreign Key → posts.id |
| user_id    | Integer  | Foreign Key → users.id |
| created_at | DateTime | Default: Now           |

### Database Relationships

- **One-to-Many:** User → Posts (One user can have many posts)
- **One-to-Many:** User → Comments (One user can have many comments)
- **One-to-Many:** Post → Comments (One post can have many comments)

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/articlehub.git
cd articlehub
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database

The database will be created automatically when you first run the application.

### Step 5: Run the Application

```bash
python app.py
```

### Step 6: Access the Application

Open your web browser and navigate to:

```
http://127.0.0.1:5000
```

## 📖 Usage Guide

### For New Users

1. **Register an Account**

   - Click "Register" in the navigation bar
   - Fill in username, email, and password
   - Click "Sign Up"

2. **Login**

   - Click "Login" in the navigation bar
   - Enter your email and password
   - Click "Login"

3. **Create a Post**

   - After logging in, click "New Post"
   - Enter title, select category, and write content
   - Click "Publish Post"

4. **View Posts**

   - Browse all posts on the homepage
   - Filter by category using the category buttons
   - Click "Read More" to view full post

5. **Comment on Posts**

   - Open any post detail page
   - Scroll to comments section
   - Type your comment and click "Post Comment"

6. **Edit Profile**
   - Click "Profile" in navigation
   - Click "Edit Profile"
   - Update your information
   - Click "Update Profile"

### For Existing Users

1. **Manage Your Posts**

   - Go to "Dashboard" to see all your posts
   - Click "Edit" to modify a post
   - Click "Delete" to remove a post

2. **Search Posts**

   - Use the search bar on homepage
   - Enter keywords
   - Click "Search"

3. **View Other Users**
   - Click on any username
   - View their profile and posts

## 🎨 Available Categories

- Technology
- Lifestyle
- Travel
- Food
- Health
- Business
- Entertainment
- Other
