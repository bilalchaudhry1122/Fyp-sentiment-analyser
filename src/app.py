import os
from flask import Flask

def create_app(test_config=None) -> Flask:
    """Flask application factory."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Simple default config
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    from src.routes import views, analyze
    app.register_blueprint(views.bp)
    app.register_blueprint(analyze.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
