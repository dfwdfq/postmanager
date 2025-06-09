from app import application

if __name__ == "__main__":
    with application.app_context():
        from model import Post
        db.create_all()
    application.run(debug=True)
