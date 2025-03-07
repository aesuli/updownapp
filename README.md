# UpDownApp

UpDownApp is a minimal HTTP file transfer server built using CherryPy. 
It allows users to upload and download files through a simple web interface. 
The application supports optional password protection, SSL for secure communication, and customizable data storage directories.

I implemented a first version of this application when I needed to transfer files from an old iPhone to a Linux desktop.
Writing a minimal CherryPy application was for me the quickest thing, also not requiring to install dedicates services on the desktop or apps on the iPhone (which was almost impossible due to its age).
I found myself using it from time to time, especially when I need to transfer lots of file or large files to/from a old/limited-access device which yet offers a browser.

## Features

- **File Upload**: Users can upload multiple files to the server.
- **File Download**: Users can download individual files or multiple files as a ZIP archive.
- **Password Protection**: Optional password-based authentication to restrict access.
- **SSL Support**: Secure communication using HTTPS with provided SSL certificate and key.
- **Customizable Data Directory**: Specify the directory where files are stored.

## Installation

You can install UpDownApp using `pip`:

```bash
pip install updownapp
```

Alternatively, you can install it directly from the source:

```bash
git clone https://github.com/aesuli/updownapp.git
cd updownapp
pip install .
```

## Usage

Once installed, you can start the server using the `updownapp` command:

```bash
updownapp [OPTIONS]
```

Options:

`--host`: The host address to bind the server to (default: `0.0.0.0`).

`--port`: The port number to listen on (default: `8080`).

`--data-dir`: The directory to store and serve files (default: `./data`).

`--disable-upload`: Disable file upload functionality.

`--disable-download`: Disable file download functionality.

`--ssl-cert`: Path to the SSL certificate file (for HTTPS).

`--ssl-key`: Path to the SSL private key file (for HTTPS).

`--passwordfile`: Path to a file containing the password for authentication.

### Examples

Start the server with default settings:

```bash
updownapp
```

Start the server on a specific host and port:

```bash
updownapp --host 127.0.0.1 --port 8000
```
Enable password protection by specifying a password file:

```bash
updownapp --passwordfile /path/to/password.txt
```
The password file should contain a single line with the plaintext password.

Enable HTTPS by providing SSL certificate and key files:

```bash
updownapp --ssl-cert /path/to/cert.pem --ssl-key /path/to/key.pem
```

## License

UpDownApp is released under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

Built using the fantastic [CherryPy - A minimalist Python web framework](https://cherrypy.dev/).