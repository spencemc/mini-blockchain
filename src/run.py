import sys
from flask import Flask
from app.views import start_server

def main():
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    start_server(port)

if __name__ == '__main__':
    main()