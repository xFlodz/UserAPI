from src import create_app
from threading import Thread
from src.grpc_server.user_server import run_grpc_server

app = create_app()


if __name__ == "__main__":
    grpc_thread = Thread(target=run_grpc_server, args=(app,))
    grpc_thread.daemon = True
    grpc_thread.start()

    app.run(port=5001)