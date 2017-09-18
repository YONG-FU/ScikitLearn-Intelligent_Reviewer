from werkzeug.serving import make_ssl_devcert

# Generate an SSL key and store it
make_ssl_devcert("certificate", host="0.0.0.0")