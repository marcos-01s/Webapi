from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017'
app.config['SECRET_KEY'] = 'your_secret_key'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user):
        self.id = str(user['_id'])
        self.username = user['username']
        self.password = user['password']

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        return User(user)
    return None

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        user = mongo.db.users.find_one({'username': data['username']})
        if user and bcrypt.check_password_hash(user['password'], data['password']):
            user_obj = User(user)
            login_user(user_obj)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = {'username': data['username'], 'password': hashed_password}
        mongo.db.users.insert_one(new_user)
        return jsonify({'success': True})
    return render_template('register.html')

@app.route('/admin', methods=['GET'])
@login_required
def admin():
    users = mongo.db.users.find()
    return render_template('admin.html', users=users)

@app.route('/admin/users', methods=['GET'])
@login_required
def get_users():
    users = mongo.db.users.find()
    return jsonify([{'id': str(user['_id']), 'username': user['username']} for user in users])

@app.route('/admin/users/<id>', methods=['PUT'])
@login_required
def update_user(id):
    data = request.json
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        mongo.db.users.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'username': data['username']}}
        )
        if 'password' in data:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            mongo.db.users.update_one(
                {'_id': ObjectId(id)},
                {'$set': {'password': hashed_password}}
            )
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'User not found'})

@app.route('/admin/users/<id>', methods=['DELETE'])
@login_required
def delete_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        mongo.db.users.delete_one({'_id': ObjectId(id)})
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'User not found'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(debug=True)
