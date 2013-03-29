import sae
from routes import app
application = sae.create_wsgi_app(app)
