'''
def create_user():
    """Create a default user in the database."""
    if not User.query.filter_by(username='mauruice').first():
        user = User(username='maurice')
        user.set_password('cluckcluck')
        db.session.add(user)
        db.session.commit()

# Perform initial setup within the application context
with app.app_context():
    db.create_all()
    create_user() # Call the function to create the user
    # Any other one-time initialization code can go here
'''