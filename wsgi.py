import os

from main import app
'''
This code is taken from web, I am not using it yet!
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)