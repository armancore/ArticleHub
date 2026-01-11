from app import app, db
from models import User, Post, Comment
from datetime import datetime, timedelta

with app.app_context():
    # Create sample users
    users_data = [
        {'username': 'alice_writer', 'email': 'alice@example.com', 'password': 'password123', 'bio': 'Passionate about technology and writing.'},
        {'username': 'bob_blogger', 'email': 'bob@example.com', 'password': 'password123', 'bio': 'Travel enthusiast and food lover.'},
        {'username': 'charlie_dev', 'email': 'charlie@example.com', 'password': 'password123', 'bio': 'Full-stack developer sharing knowledge.'}
    ]
    
    users = []
    for user_data in users_data:
        # Check if user exists
        existing = User.query.filter_by(email=user_data['email']).first()
        if not existing:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                bio=user_data['bio']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            users.append(user)
        else:
            users.append(existing)
    
    db.session.commit()
    
    # Create sample posts
    posts_data = [
        {'title': 'Getting Started with Flask', 'content': 'Flask is an amazing micro web framework for Python. It is lightweight, flexible, and perfect for building web applications quickly. In this post, I will share my journey learning Flask and building web applications.', 'category': 'Technology', 'user_idx': 0},
        {'title': 'Top 10 Travel Destinations for 2024', 'content': 'Traveling opens up new horizons and experiences. Here are my top 10 favorite destinations that everyone should visit at least once in their lifetime. From beaches to mountains, there is something for everyone.', 'category': 'Travel', 'user_idx': 1},
        {'title': 'Healthy Eating Made Simple', 'content': 'Eating healthy does not have to be complicated. With a few simple tips and tricks, you can transform your diet and feel better every day. Let me share my favorite healthy recipes and meal planning strategies.', 'category': 'Health', 'user_idx': 2},
        {'title': 'My Favorite Python Libraries', 'content': 'Python has an incredible ecosystem of libraries that make development a breeze. Here are my top picks for web development, data science, and automation. These tools have saved me countless hours of work.', 'category': 'Technology', 'user_idx': 0},
        {'title': 'Best Coffee Shops in Town', 'content': 'Coffee lovers unite! I have explored the best coffee shops in our city and compiled a list of must-visit places. From cozy corners to trendy cafes, these spots serve the best brews.', 'category': 'Food', 'user_idx': 1}
    ]
    
    posts = []
    for i, post_data in enumerate(posts_data):
        post = Post(
            title=post_data['title'],
            content=post_data['content'],
            category=post_data['category'],
            author_id=users[post_data['user_idx']].id,
            created_at=datetime.utcnow() - timedelta(days=len(posts_data)-i)
        )
        db.session.add(post)
        posts.append(post)
    
    db.session.commit()
    
    print("✅ Sample data added successfully!")
    print(f"   {len(users)} users created")
    print(f"   {len(posts)} posts created")
    print("\nSample login credentials:")
    for user_data in users_data:
        print(f"   Email: {user_data['email']} | Password: password123")