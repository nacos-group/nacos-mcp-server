from . import server
import asyncio
import argparse


def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='Nacos Server')
    parser.add_argument('--host', default='localhost', help='Host to connect to Nacos Server')
    parser.add_argument('--port', default='8848', help='Port to connect to Nacos Server')
    parser.add_argument('--access_token', default='', help='AccessToken to connect to Nacos Server if auth enabled')

    args = parser.parse_args()
    asyncio.run(server.main(args.host, args.port, args.access_token))


# Optionally expose other important items at package level
__all__ = ["main", "server"]