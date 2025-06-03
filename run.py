from app import create_app

Flask_app = create_app() # Creates the basic Flask app that I have defined in my app directory.

if __name__ == '__main__':
    Flask_app.run(debug=True) # Executes the flask app with debugger on for my easier journey while creating this app.
    
#Code ends here