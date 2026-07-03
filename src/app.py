import os
from flask import Flask

def create_app(test_config=None) -> Flask:
    """Flask application factory."""
    # Project root is one level up from src/
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static"),
    )

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from src.routes import views, analyze
    app.register_blueprint(views.bp)
    app.register_blueprint(analyze.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)