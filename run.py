from webapp import create_app

app = create_app()

if __name__ == "__main__":
    app.run(template_folder='webapp/templates', debug=True)
