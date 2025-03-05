import os
import cherrypy
import argparse

# Default upload/download directory
DEFAULT_UPLOAD_DIR = "files"
DEFAULT_DOWNLOAD_DIR = "files"

def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Minimal HTTP File Transfer Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Server host address")
    parser.add_argument("--port", type=int, default=8080, help="Server port number")
    parser.add_argument("--upload-dir", type=str, default=DEFAULT_UPLOAD_DIR, help="Directory to store uploaded files")
    return parser.parse_args()

class FileUploadApp:
    """CherryPy application for file uploads."""
    
    def __init__(self, upload_dir):
        self.upload_dir = upload_dir
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)
    
    @cherrypy.expose
    def index(self):
        """Displays the file upload form."""
        return """
        <html>
        <head><title>File Upload</title></head>
        <body>
            <h2>Upload Files</h2>
            <form action="upload" method="post" enctype="multipart/form-data">
                <input type="file" name="files" multiple><br><br>
                <input type="submit" value="Upload">
            </form>
        </body>
        </html>
        """
    
    @cherrypy.expose
    def upload(self, files):
        """Handles file uploads and saves them to the specified directory."""
        uploaded_files = files if isinstance(files, list) else [files]
        
        for file in uploaded_files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, 'wb') as f:
                while chunk := file.file.read(8192):
                    f.write(chunk)
        
        return f"Successfully uploaded {len(uploaded_files)} file(s)!"

if __name__ == '__main__':
    args = parse_arguments()
    
    # Update CherryPy configuration
    cherrypy.config.update({
        'server.socket_host': args.host,
        'server.socket_port': args.port,
        'server.max_request_body_size': 1024 * 1024 * 1024 * 1024,  # Set high limit for large files
        'server.socket_timeout': 60,
    })
    
    # Start the CherryPy server with the configured upload directory
    cherrypy.quickstart(FileUploadApp(args.upload_dir))
