  
import os
from flask_admin import Admin
from .models import db, User, Ingredient, Chat, ChatParticipant, Cocktail, CocktailIngredient, Comment, Dish, DishIngredient, Favorite, Pairing, Post, Message, Notification, Follow
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Ingredient, db.session))
    admin.add_view(ModelView(Cocktail, db.session))
    admin.add_view(ModelView(Dish, db.session))
    admin.add_view(ModelView(CocktailIngredient, db.session))
    admin.add_view(ModelView(DishIngredient, db.session))
    admin.add_view(ModelView(Favorite, db.session))
    admin.add_view(ModelView(Pairing, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(ModelView(Chat, db.session))
    admin.add_view(ModelView(ChatParticipant, db.session))
    admin.add_view(ModelView(Message, db.session))
    admin.add_view(ModelView(Notification, db.session))
    admin.add_view(ModelView(Follow, db.session))
    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))