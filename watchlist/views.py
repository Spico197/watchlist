import os
import sys

from flask import flash, redirect, render_template, request, url_for
from flask_login import (UserMixin, current_user, login_required, login_user,
                         logout_user)
from werkzeug.security import check_password_hash, generate_password_hash

from watchlist import app, db
from watchlist.models import Movie, User


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input')
            return redirect(url_for('hello'))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created')
        return redirect(url_for('hello'))
    # user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/user/<name>')
def user_page(name):
    return 'User page: ' + name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='spico'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test Page'

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def movie_edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input')
            return redirect(url_for('movie_edit', movie_id=movie_id))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated')
        return redirect(url_for('hello'))
    return render_template('movie_edit.html', movie=movie)

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted')
    return redirect(url_for('hello'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Invalid input')
            return redirect(url_for('login'))
        user = User.query.first()
        if username == user.username and user.valid_password(password):
            login_user(user)
            flash('Login success')
            return redirect(url_for('hello'))
        flash('Invalid username or password')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Good Bye')
    return redirect(url_for('hello'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('Settings updated')
        return redirect(url_for('hello'))
    return render_template('settings.html')
