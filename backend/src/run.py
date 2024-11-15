from app import create_app, register_routes

app = create_app()
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
