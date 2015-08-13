from app import create_app
from flask.ext.script import Manager, Server

app = create_app('development')
manager = Manager(app)
# manager.add_command('runserver', Server(host='0.0.0.0'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run()
    # manager.run(debug=True)