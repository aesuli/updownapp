# Minimal File Transfer HTTP Server

A simple file upload server built using CherryPy that allows users to upload multiple files via a web interface.

## Features
- Web-based file upload form
- Supports multiple file uploads
- Configurable host, port, and upload directory
- Simple and lightweight

## Installation

Ensure you have Python installed (version 3.6 or higher recommended). Then, install the required dependencies:

```sh
pip install cherrypy
```

## Usage

Run the server with default settings:

```sh
python file_upload_server.py
```

Or specify custom settings:

```sh
python file_upload_server.py --host 127.0.0.1 --port 9090 --upload-dir my_uploads
```

### Arguments
| Argument      | Description                            | Default Value |
|--------------|--------------------------------|--------------|
| `--host`     | Server host address             | `0.0.0.0`    |
| `--port`     | Server port number              | `8080`       |
| `--upload-dir` | Directory to store uploaded files | `uploads`     |

## How It Works
- The server provides an HTML form at the root (`/`) where users can select and upload files.
- Uploaded files are stored in the specified upload directory.
- The response confirms the number of successfully uploaded files.

## Example
After running the server, open a browser and visit:

```
http://localhost:8080
```

Upload files using the form and they will be saved in the configured directory.

## License
This project is licensed under the [BSD License](LICENSE).

