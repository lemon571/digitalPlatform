from .students import students_bp
from .groups import groups_bp

def register_routes(app):
    app.register_blueprint(students_bp)
    app.register_blueprint(groups_bp)
