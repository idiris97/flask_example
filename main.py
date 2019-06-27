from app import app
from posts.blueprint import pos
import view

app.register_blueprint(pos, url_prefix='/blog')

if __name__ == '__main__':
    app.run()