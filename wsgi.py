from learning_app import create_app, models, db, forms
app2 = create_app()

if __name__ == '__main__':
    app2.run(debug=True)