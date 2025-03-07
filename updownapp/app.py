import os
import cherrypy
import argparse
import zipfile
import io
import hashlib
import time
import signal
import sys

# Default data directory
DEFAULT_DATA_DIR = "data"

class FileTransferApp:
    """CherryPy application for HTTP file transfer."""
    
    def __init__(self, data_dir, enable_upload=True, enable_download=True, password_hash=None):
        self.data_dir = os.path.abspath(data_dir)  # Ensure data_dir is an absolute path
        self.enable_upload = enable_upload
        self.enable_download = enable_download
        self.password_hash = password_hash  # Store the hashed password
        
        # Create the data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def check_auth(self):
        """Check if the user is authenticated."""
        if not self.password_hash:
            return True  # No password set, allow access
        
        # Check if the session contains the authenticated flag
        if cherrypy.session.get("authenticated"):
            return True
        return False
    
    def require_auth(self):
        """Redirect to the login page if the user is not authenticated."""
        if not self.check_auth():
            raise cherrypy.HTTPRedirect("/login")
    
    @cherrypy.expose
    def index(self):
        """Displays the main page with upload form (if enabled) and file list (if enabled)."""
        self.require_auth()  # Ensure the user is authenticated
        
        html = """<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>File Transfer</title>
        </head>
        <body>
        <h2>File Transfer</h2>
        """

        # Add upload form if upload is enabled
        if self.enable_upload:
            html += """
            <h3>Upload Files</h3>
            <form id="uploadForm" action="upload" method="post" enctype="multipart/form-data">
                <input type="file" name="files" multiple><br><br>
                <input type="submit" value="Upload" id="uploadButton">
            </form>
            <div id="progress" style="display: none;">
                <progress id="progressBar" value="0" max="100"></progress>
                <span id="status">Uploading...</span>
            </div>
            <button id="stopUploadButton" style="display: none;" onclick="stopUpload()">Stop Upload</button>
            <script>
                let xhr = null;  // Declare xhr outside of the form submission handler for access in stopUpload

                document.getElementById("uploadForm").onsubmit = function(event) {
                    event.preventDefault();  // Prevent the default form submission
                    const formData = new FormData(this);

                    // Check if any files with non-empty names are selected
                    const files = formData.getAll("files");
                    const hasFiles = files.some(file => file.name && file.name.trim() !== "");

                    document.getElementById("progress").style.display = "block";

                    if (!hasFiles) {
                        document.getElementById("status").textContent = "Please select at least one file to upload.";
                        return;
                    }

                    // Disable the upload button and show the progress bar
                    document.getElementById("uploadButton").disabled = true;
                    document.getElementById("stopUploadButton").style.display = "inline-block";

                    // Create a new XMLHttpRequest to handle the upload
                    xhr = new XMLHttpRequest();

                    // Track upload progress
                    xhr.upload.onprogress = function(event) {
                        if (event.lengthComputable) {
                            const percentComplete = (event.loaded / event.total) * 100;
                            document.getElementById("progressBar").value = percentComplete;
                            document.getElementById("status").textContent = `Uploading: ${Math.round(percentComplete)}%`;
                        }
                    };

                    // Handle upload completion
                    xhr.onload = function() {
                        if (xhr.status === 200) {
                            document.getElementById("status").textContent = "Upload complete! Refreshing file list...";
                            setTimeout(() => {
                                window.location.href = window.location.href;  // Redirect to self
                            }, 1000);  // Wait 1 second before redirecting
                        } else {
                            document.getElementById("status").textContent = "Upload failed. Please try again.";
                        }
                    };

                    // Send the form data
                    xhr.open("POST", "upload", true);
                    xhr.send(formData);
                };

                // Function to stop the upload
                function stopUpload() {
                    if (xhr) {
                        xhr.abort();  // Stop the upload
                        document.getElementById("status").textContent = "Upload stopped.";
                        document.getElementById("uploadButton").disabled = false;  // Re-enable the upload button
                        document.getElementById("stopUploadButton").style.display = "none";  // Hide the stop button
                    }
                }
            </script>
            <hr>
            """

        # Add file list if download is enabled
        if self.enable_download:
            files = os.listdir(self.data_dir)
            if files:
                html += """
                <h3>Download Files</h3>
                <form id="downloadForm" action="download_selected" method="post">
                    <ul>
                """
                for file in files:
                    html += f'<li><input type="checkbox" name="files" value="{file}"> <a href="/download_file/{file}">{file}</a></li>'
                html += """
                    </ul>
                    <br>
                    <input type="submit" value="Download Selected">
                    <button type="button" onclick="toggleSelectAll()">Select All</button>
                </form>
                <script>
                    function toggleSelectAll() {
                        // Get all checkboxes
                        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
                        // Check if any checkbox is unchecked
                        const anyUnchecked = Array.from(checkboxes).some(checkbox => !checkbox.checked);
                        // Toggle all checkboxes based on the state of the first checkbox
                        checkboxes.forEach(checkbox => checkbox.checked = anyUnchecked);
                    }
                </script>
                """
            else:
                html += "<p>No files available for download.</p>"

        html += """
        </body>
        </html>
        """
        return html
    
    @cherrypy.expose
    def login(self, password=None):
        """Handles user login."""
        if cherrypy.request.method == "POST":
            if self.password_hash and self.verify_password(password):
                cherrypy.session["authenticated"] = True
                cherrypy.session["login_time"] = time.time()
                raise cherrypy.HTTPRedirect("/")
            else:
                return "Invalid password. <a href='/login'>Try again</a>."
        
        # Show the login form
        return """
        <html>
        <head><title>Login</title></head>
        <body>
            <h2>Login</h2>
            <form method="post">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
                <input type="submit" value="Login">
            </form>
        </body>
        </html>
        """
    
    def verify_password(self, password):
        """Verify the provided password against the stored hash."""
        if not password:
            return False
        # Hash the provided password and compare it to the stored hash
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash
    
    @cherrypy.expose
    def upload(self, files):
        """Handles file uploads and saves them to the data directory."""
        self.require_auth()  # Ensure the user is authenticated
        
        if not self.enable_upload:
            raise cherrypy.HTTPError(403, "Upload functionality is disabled.")
        
        # Check if files are selected
        if not files:
            return "No files selected for upload."
        
        uploaded_files = files if isinstance(files, list) else [files]
        
        # Filter out files with empty names
        uploaded_files = [file for file in uploaded_files if file.filename and file.filename.strip()]
        
        if not uploaded_files:
            return "No valid files selected for upload."
        
        for file in uploaded_files:
            print(file.filename)
            file_path = os.path.join(self.data_dir, file.filename.encode(file.headers.encodings[0]).decode('utf-8'))
            with open(file_path, 'wb') as f:
                while chunk := file.file.read(8192):
                    f.write(chunk)
        
        return f"Successfully uploaded {len(uploaded_files)} file(s)!"

    @cherrypy.expose
    def download_file(self, filename):
        """Handles single file downloads."""
        self.require_auth()  # Ensure the user is authenticated
        
        if not self.enable_download:
            raise cherrypy.HTTPError(403, "Download functionality is disabled.")
        
        file_path = os.path.join(self.data_dir, filename)
        if os.path.exists(file_path):
            # Convert the relative path to an absolute path
            absolute_path = os.path.abspath(file_path)
            return cherrypy.lib.static.serve_file(absolute_path, "application/x-download", "attachment", filename)
        else:
            raise cherrypy.HTTPError(404, "File not found.")

    @cherrypy.expose
    def download_selected(self, *files, **kwargs):
        """Handles downloading selected files as a ZIP archive.""" 
        self.require_auth()  # Ensure the user is authenticated
        
        if not self.enable_download:
            raise cherrypy.HTTPError(403, "Download functionality is disabled.")
        
        # Get the list of selected files
        selected_files = kwargs.get("files", [])
        if isinstance(selected_files, str):
            # Direct download of a single file
            return self.download_file(selected_files)
        
        if not selected_files:
            return "No files selected for download."

        # Create a ZIP file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in selected_files:
                file_path = os.path.join(self.data_dir, file)
                if os.path.exists(file_path):
                    zip_file.write(file_path, arcname=file)

        # Prepare the ZIP file for download
        zip_buffer.seek(0)
        cherrypy.response.headers['Content-Type'] = 'application/zip'
        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename="selected_files.zip"'
        return zip_buffer.getvalue()

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Minimal HTTP File Transfer Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Server host address")
    parser.add_argument("--port", type=int, default=8080, help="Server port number")
    parser.add_argument("--data-dir", type=str, default=DEFAULT_DATA_DIR, help="Directory to store and serve files")
    parser.add_argument("--disable-upload", action="store_true", help="Disable file upload functionality")
    parser.add_argument("--disable-download", action="store_true", help="Disable file download functionality")
    parser.add_argument("--ssl-cert", type=str, help="Path to SSL certificate file (for HTTPS)")
    parser.add_argument("--ssl-key", type=str, help="Path to SSL private key file (for HTTPS)")
    parser.add_argument("--passwordfile", type=str, help="Path to file containing the password")
    return parser.parse_args()

def read_password_from_file(passwordfile):
    """Read the password from the specified file."""
    if not passwordfile or not os.path.exists(passwordfile):
        return None
    with open(passwordfile, "r") as f:
        return f.read().strip()

def signal_handler(signal, frame):
    """Handles Ctrl+C signal to gracefully shut down the server."""
    print("\nShutting down the server...")
    cherrypy.engine.exit()
    sys.exit(0)

def main():
    args = parse_arguments()
    
    # Read the password from the file
    password = read_password_from_file(args.passwordfile)
    password_hash = None
    if password:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # CherryPy configuration
    config = {
        'global': {
            'server.socket_host': args.host,
            'server.socket_port': args.port,
            'server.max_request_body_size': 0,
            'server.socket_timeout': 60,
            'tools.sessions.on': True,  # Enable sessions
            'tools.sessions.timeout': 10,  # Session timeout in minutes
        }
    }

    # Add SSL configuration if certificate and key are provided
    if args.ssl_cert and args.ssl_key:
        config.update({
            'server.ssl_module': 'builtin',
            'server.ssl_certificate': args.ssl_cert,
            'server.ssl_private_key': args.ssl_key,
        })
        print("HTTPS enabled.")
    else:
        print("HTTPS disabled. Running in HTTP mode.")

    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start the CherryPy server with the configured data directory and options
    app = FileTransferApp(
        data_dir=args.data_dir,
        enable_upload=not args.disable_upload,
        enable_download=not args.disable_download,
        password_hash=password_hash
    )

    cherrypy.quickstart(app,'/', config)

if __name__ == '__main__':
    main()