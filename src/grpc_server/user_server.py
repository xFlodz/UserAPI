import grpc
from concurrent import futures
from src.proto import user_pb2, user_pb2_grpc
from ..services.user_service import get_user_by_email_service, get_user_by_id_service

class gRPCUserService(user_pb2_grpc.gRPCUserServiceServicer):
    def __init__(self, app):
        self.app = app
    def GetUserByEmail(self, request, context):
        with self.app.app_context():
            user = get_user_by_email_service(request.email)
            if user:
                return user_pb2.GetUserByEmailResponse(
                    id=str(user['id']),
                    email=user['email'],
                    name=user['name'],
                    surname=user['surname'],
                    role=user['role']
                )
            return user_pb2.GetUserByEmailResponse()

    def GetUserById(self, request, context):
        with self.app.app_context():
            user = get_user_by_id_service(request.user_id)
            if user:
                return user_pb2.GetUserByIdResponse(
                    id=str(user['id']),
                    email=user['email'],
                    name=user['name'],
                    surname=user['surname'],
                    role=user['role']
                )
            return user_pb2.GetUserByIdResponse()

def run_grpc_server(app):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_gRPCUserServiceServicer_to_server(gRPCUserService(app), server)
    server.add_insecure_port('0.0.0.0:50053')  # Порт для gRPC сервера
    print("User gRPC Server started on port 50053")
    server.start()
    server.wait_for_termination()
