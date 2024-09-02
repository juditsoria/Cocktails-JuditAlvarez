from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Enum, Integer, String, Date
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Encrypted
    registration_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    profile_info = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))

    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "registration_date": self.registration_date,
            "profile_info": self.profile_info,
            "avatar_url": self.avatar_url
        }
class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Ingredient {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
class Cocktail(db.Model):
    __tablename__ = 'cocktails'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    preparation_steps = db.Column(db.Text, nullable=False)
    flavor_profile = db.Column(db.Enum('sweet', 'sour', 'bitter', 'salty', 'umami',name='cocktail_enum'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('cocktails', lazy=True))

    def __repr__(self):
        return f'<Cocktail {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "preparation_steps": self.preparation_steps,
            "flavor_profile": self.flavor_profile,
            "user_id": self.user_id,
            "creation_date": self.creation_date
        }
class Dish(db.Model):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    preparation_steps = db.Column(db.Text, nullable=False)
    flavor_profile = db.Column(db.Enum('sweet', 'sour', 'bitter', 'salty', 'umami',  name='flavor_profile_enum'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('dishes', lazy=True))

    def __repr__(self):
        return f'<Dish {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "preparation_steps": self.preparation_steps,
            "flavor_profile": self.flavor_profile,
            "user_id": self.user_id,
            "creation_date": self.creation_date
        }
class CocktailIngredient(db.Model):
    __tablename__ = 'cocktail_ingredients'

    cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktails.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    quantity = db.Column(db.String(50))
    unit = db.Column(db.String(20))

    cocktail = db.relationship('Cocktail', backref=db.backref('cocktail_ingredients', lazy=True))
    ingredient = db.relationship('Ingredient', backref=db.backref('cocktail_ingredients', lazy=True))

    def __repr__(self):
        return f'<CocktailIngredient Cocktail: {self.cocktail_id}, Ingredient: {self.ingredient_id}>'

    def serialize(self):
        return {
            "cocktail_id": self.cocktail_id,
            "ingredient_id": self.ingredient_id,
            "quantity": self.quantity,
            "unit": self.unit
        }
class DishIngredient(db.Model):
    __tablename__ = 'dish_ingredients'

    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    quantity = db.Column(db.String(50))
    unit = db.Column(db.String(20))

    dish = db.relationship('Dish', backref=db.backref('dish_ingredients', lazy=True))
    ingredient = db.relationship('Ingredient', backref=db.backref('dish_ingredients', lazy=True))

    def __repr__(self):
        return f'<DishIngredient Dish: {self.dish_id}, Ingredient: {self.ingredient_id}>'

    def serialize(self):
        return {
            "dish_id": self.dish_id,
            "ingredient_id": self.ingredient_id,
            "quantity": self.quantity,
            "unit": self.unit
        }
class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktails.id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'))
    saved_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('favorites', lazy=True))
    cocktail = db.relationship('Cocktail', backref=db.backref('favorites', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('favorites', lazy=True))

    def __repr__(self):
        return f'<Favorite User: {self.user_id}, Cocktail: {self.cocktail_id}, Dish: {self.dish_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "cocktail_id": self.cocktail_id,
            "dish_id": self.dish_id,
            "saved_date": self.saved_date
        }
class Pairing(db.Model):
    __tablename__ = 'pairings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cocktail_id = db.Column(db.Integer, db.ForeignKey('cocktails.id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'))
    saved_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('pairings', lazy=True))
    cocktail = db.relationship('Cocktail', backref=db.backref('pairings', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('pairings', lazy=True))

    def __repr__(self):
        return f'<Pairing User: {self.user_id}, Cocktail: {self.cocktail_id}, Dish: {self.dish_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "cocktail_id": self.cocktail_id,
            "dish_id": self.dish_id,
            "saved_date": self.saved_date
        }
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Post User: {self.user_id}, Content: {self.content[:20]}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "creation_date": self.creation_date
        }
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    post = db.relationship('Post', backref=db.backref('comments', lazy=True))
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f'<Comment User: {self.user_id}, Post: {self.post_id}, Content: {self.content[:20]}>'

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "content": self.content,
            "creation_date": self.creation_date
        }
class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    is_group = db.Column(db.Boolean, default=False)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Chat {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_group": self.is_group,
            "creation_date": self.creation_date
        }
class ChatParticipant(db.Model):
    __tablename__ = 'chat_participants'

    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    chat = db.relationship('Chat', backref=db.backref('chat_participants', lazy=True))
    user = db.relationship('User', backref=db.backref('chat_participants', lazy=True))

    def __repr__(self):
        return f'<ChatParticipant Chat: {self.chat_id}, User: {self.user_id}>'

    def serialize(self):
        return {
            "chat_id": self.chat_id,
            "user_id": self.user_id
        }
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text, nullable=False)
    sent_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    chat = db.relationship('Chat', backref=db.backref('messages', lazy=True))
    user = db.relationship('User', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return f'<Message Chat: {self.chat_id}, User: {self.user_id}, Content: {self.content[:20]}>'

    def serialize(self):
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "user_id": self.user_id,
            "content": self.content,
            "sent_date": self.sent_date
        }
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.Enum('comment', 'message', 'new_follower', 'other',  name='notification_enum'), nullable=False)
    content = db.Column(db.Text)
    read = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('notifications', lazy=True))

    def __repr__(self):
        return f'<Notification User: {self.user_id}, Type: {self.type}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "content": self.content,
            "read": self.read,
            "date": self.date
        }
class Follow(db.Model):
    __tablename__ = 'follows'

    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    follower = db.relationship('User', foreign_keys=[follower_id], backref=db.backref('follows', lazy=True))
    followed = db.relationship('User', foreign_keys=[followed_id], backref=db.backref('followers', lazy=True))

    def __repr__(self):
        return f'<Follow Follower: {self.follower_id}, Following: {self.followed_id}>'

    def serialize(self):
        return {
            "follower_id": self.follower_id,
            "followed_id": self.followed_id,
            "date": self.date
        }















