# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: user.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'user.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nuser.proto\x12\x04user\"&\n\x15GetUserByEmailRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\"`\n\x16GetUserByEmailResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0f\n\x07surname\x18\x04 \x01(\t\x12\x0c\n\x04role\x18\x05 \x01(\t\"%\n\x12GetUserByIdRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"]\n\x13GetUserByIdResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0f\n\x07surname\x18\x04 \x01(\t\x12\x0c\n\x04role\x18\x05 \x01(\t2\xa2\x01\n\x0fgRPCUserService\x12K\n\x0eGetUserByEmail\x12\x1b.user.GetUserByEmailRequest\x1a\x1c.user.GetUserByEmailResponse\x12\x42\n\x0bGetUserById\x12\x18.user.GetUserByIdRequest\x1a\x19.user.GetUserByIdResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_GETUSERBYEMAILREQUEST']._serialized_start=20
  _globals['_GETUSERBYEMAILREQUEST']._serialized_end=58
  _globals['_GETUSERBYEMAILRESPONSE']._serialized_start=60
  _globals['_GETUSERBYEMAILRESPONSE']._serialized_end=156
  _globals['_GETUSERBYIDREQUEST']._serialized_start=158
  _globals['_GETUSERBYIDREQUEST']._serialized_end=195
  _globals['_GETUSERBYIDRESPONSE']._serialized_start=197
  _globals['_GETUSERBYIDRESPONSE']._serialized_end=290
  _globals['_GRPCUSERSERVICE']._serialized_start=293
  _globals['_GRPCUSERSERVICE']._serialized_end=455
# @@protoc_insertion_point(module_scope)
