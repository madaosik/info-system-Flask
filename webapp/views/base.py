from flask import redirect, url_for, render_template


def configure(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('base/403.html'), 403

    @app.route('/')
    def home_redir():
        return redirect(url_for('home'))