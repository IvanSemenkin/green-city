from flask import jsonify
from app.api import api_blueprint

@api_blueprint.route('/health')
def health_check():
    return jsonify({"status": "healthy"})
