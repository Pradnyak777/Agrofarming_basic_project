from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

PORT = 8080

class AgroforestryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve the HTML form
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Agroforestry Data Form</title>
        </head>
        <body>
            <h2>Agroforestry Data Collection Form</h2>
            <form action="/" method="post" enctype="multipart/form-data">
                <label for="farmerName">Farmer Name:</label><br>
                <input type="text" id="farmerName" name="farmerName" required><br><br>

                <label for="farmerContact">Farmer Contact Number:</label><br>
                <input type="tel" id="farmerContact" name="farmerContact" pattern="[0-9]{10}" required><br><br>

                <label for="fieldPhoto">Field Photo:</label><br>
                <input type="file" id="fieldPhoto" name="fieldPhoto" required><br><br>

                <label for="location">Plot Location (Latitude, Longitude):</label><br>
                <input type="text" id="location" name="location" placeholder="e.g., 12.3456, 78.9101" required><br><br>

                <label for="treeSpecies">Tree Species and Quantity:</label><br>
                <textarea id="treeSpecies" name="treeSpecies" rows="5" cols="30" placeholder="e.g., Mango-100, Lemon-80" required></textarea><br><br>

                <button type="submit">Submit</button>
            </form>
        </body>
        </html>
        """)

    def do_POST(self):
        # Handle form submission
        content_type, params = cgi.parse_header(self.headers.get("Content-Type"))
        if content_type == "multipart/form-data":
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={"REQUEST_METHOD": "POST"})
            
            # Extract form data
            farmer_name = form.getvalue("farmerName")
            farmer_contact = form.getvalue("farmerContact")
            location = form.getvalue("location")
            tree_species = form.getvalue("treeSpecies")
            
            # Handle file upload
            field_photo = form["fieldPhoto"]
            file_name = field_photo.filename
            with open(file_name, "wb") as f:
                f.write(field_photo.file.read())
            
            # Save data to a text file
            with open("farmer_data.txt", "a") as f:
                f.write(f"Farmer Name: {farmer_name}\n")
                f.write(f"Farmer Contact: {farmer_contact}\n")
                f.write(f"Location: {location}\n")
                f.write(f"Tree Species: {tree_species}\n")
                f.write(f"Field Photo: {file_name}\n")
                f.write("-" * 40 + "\n")

            # Respond with success message
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h2>Form submitted successfully!</h2>")
            self.wfile.write(b"<a href='/'>Go back to the form</a>")

# Run the server
def run():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, AgroforestryHandler)
    print(f"Server running on port {PORT}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()