from flask import jsonify, render_template
from server import stats
from server import utils

def init(app):
    @app.route("/stats")
    def app_stats():
        return jsonify(stats.info())

    @app.route("/")
    def frontend():
        return render_template("index.html")

    @app.errorhandler(404)
    def page_404(error):
        return jsonify(utils.dead_response("Method not found"))
