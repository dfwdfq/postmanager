import os
import json
from dotenv import load_dotenv
from flask import Flask, url_for, redirect, jsonify, request
from markupsafe import escape
from flasgger import Swagger
from model import db, Post
import click
from flask.cli import with_appcontext

load_dotenv()

application = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "instance", "blog.db")}')

db.init_app(application)

SWAGGER_CONFIG_PATH = os.path.join(application.root_path, 'swagger_config.json')
with open(SWAGGER_CONFIG_PATH, 'r') as f:
    swagger_template = json.load(f)
    
swagger = Swagger(application,template=swagger_template)

@application.route("/")
def root():
    return redirect(url_for('flasgger.apidocs'))

@application.route('/posts', methods=['POST'])
def create_post():
    """Создать новый пост
    ---
    tags:
      - Posts
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/PostCreate'
    responses:
      201:
        description: Пост создан
        schema:
          $ref: '#/definitions/PostCreated'
    """
    data = request.json
    post = Post(title=data['title'], content=data['content'])
    db.session.add(post)
    db.session.commit()
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at.isoformat()
    }), 201

@application.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Обновить пост
    ---
    tags:
      - Posts
    parameters:
      - name: post_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            content:
              type: string
          required:
            - title
            - content
    responses:
      200:
        description: Пост обновлен
        schema:
          $ref: '#/definitions/PostCreated'
      404:
        description: Пост не найден
      500:
        description: Ошибка сервера
    """
    try:
        post = Post.query.get_or_404(post_id)
        data = request.json

        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)

        db.session.commit()

        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at.isoformat()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Не удалось обновить пост', 'message': str(e)}), 500

@application.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Удалить пост
    ---
    tags:
      - Posts
    parameters:
      - name: post_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Пост удален
        schema:
          type: object
          properties:
            message:
              type: string
            post_id:
              type: integer
      404:
        description: Пост не найден
      500:
        description: Ошибка сервера
    """
    try:
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Пост удален', 'post_id': post_id}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Не удалось удалить пост', 'message': str(e)}), 500

@application.route('/posts', methods=['GET'])
def get_posts():
    """
    Список всех постов
    ---
    tags:
      - Posts
    responses:
      200:
        description: Список постов
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
      500:
        description: Ошибка сервера
    """
    try:
        posts = Post.query.all()
        return jsonify([{'id': p.id, 'title': p.title} for p in posts]), 200
    except Exception as e:
        return jsonify({'error': 'Не удалось получить посты', 'message': str(e)}), 500

@application.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Детали поста по ID
    ---
    tags:
      - Posts
    parameters:
      - name: post_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Детали поста
        schema:
          $ref: '#/definitions/PostCreated'
      404:
        description: Пост не найден
      500:
        description: Ошибка сервера
    """
    try:
        post = Post.query.get_or_404(post_id)
        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at.isoformat()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Не удалось получить пост', 'message': str(e)}), 500
    
@application.cli.command("init-db")
@with_appcontext
def init_db():
    from model import Post
    db.create_all()
    click.echo(" Database tables created.")
