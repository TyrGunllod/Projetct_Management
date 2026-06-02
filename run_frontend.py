"""
Standalone frontend server for local testing.
Run: python run_frontend.py
Serves all 5 frontend tabs on http://localhost:3000
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 3000
FRONTEND_DIR = Path(__file__).parent / "frontend"

os.chdir(FRONTEND_DIR)


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "":
            self.path = "/dashboard/index.html"
        return super().do_GET()

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    print(f"\n  Gestão de Projetos — Frontend Standalone")
    print(f"  Servindo em: http://localhost:{PORT}")
    print(f"\n  Abas disponíveis:")
    print(f"    http://localhost:{PORT}/dashboard/index.html")
    print(f"    http://localhost:{PORT}/projeto/index.html")
    print(f"    http://localhost:{PORT}/tarefas/index.html")
    print(f"    http://localhost:{PORT}/recursos/index.html")
    print(f"    http://localhost:{PORT}/cronograma/index.html")
    print(f"\n  Pressione Ctrl+C para parar\n")

    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Servidor encerrado.")
