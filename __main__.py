from app import application, db

if __name__ == "__main__":
    with application.app_context():
        db.create_all()
    application.run()
