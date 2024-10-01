import pickle
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse


# Placeholder model class to avoid using sklearn
class SimpleModel:
    def predict(self, x):
        # Simple prediction logic (replace with actual model logic)
        return [X[0] * 0.5 for X in x]


# Load the trained model (for illustration only)
# Replace this with actual model instantiation if needed
model = SimpleModel()


class ElectricityPricePredictionHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'r') as file:
                self.wfile.write(file.read().encode())
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        if self.path == '/predict':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form_data = urlparse.parse_qs(post_data.decode('utf-8'))

            try:
                consumption = float(form_data['consumption'][0])
                prediction = model.predict([[consumption]])
                prediction_text = f"Predicted Electricity Price: ${prediction[0]:.2f}"
            except (ValueError, KeyError):
                prediction_text = "Invalid input. Please enter a valid number."

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            response = f"""
            <html>
            <body>
                <h1>{prediction_text}</h1>
                <a href="/">Go back</a>
            </body>
            </html>
            """
            self.wfile.write(response.encode())
        else:
            self.send_error(404, "File Not Found")


def run(server_class=HTTPServer, handler_class=ElectricityPricePredictionHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server at http://127.0.0.1:{port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
