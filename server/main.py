from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        from route.code_executor import home_bp
        app.register_blueprint(home_bp)
        from route.shutdown import home_bp
        app.register_blueprint(home_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)