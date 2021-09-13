from app import app
import os
from waitress import serve

if __name__ == '__main__':
	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
	port = int(os.environ.get('PORT', 5000))
	serve(app, host="0.0.0.0", port=port)
	# app.run(host="0.0.0.0", port=port)