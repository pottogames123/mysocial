import subprocess
import time
from django.core.management.base import BaseCommand
from django.core.management.commands.runserver import Command as RunserverCommand

class Command(BaseCommand):
    help = 'Run Django server with ngrok'

    def handle(self, *args, **options):
        port = options.get('port', 8000)
        self.start_ngrok(port)
        self.run_django_server(port)

    def start_ngrok(self, port):
        command = f"ngrok http {port}"
        ngrok_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            output = ngrok_process.stdout.readline().decode('utf-8').strip()
            if "Forwarding" in output:
                ngrok_url = output.split(" ")[1]
                self.stdout.write(f'ngrok tunnel "http://127.0.0.1:{port}" -> "{ngrok_url}"')
                break

    def run_django_server(self, port):
        RunserverCommand().run_from_argv(['manage.py', 'runserver', str(port)])

    def add_arguments(self, parser):
        parser.add_argument('port', nargs='?', type=int, default=8000, help='Port number to run the server on')
