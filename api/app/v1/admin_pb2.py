# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: admin.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x61\x64min.proto\x12\x10\x61\x64min.service.v1\"C\n\x07\x41\x63\x63ount\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05phone\x18\x03 \x01(\t\x12\x0e\n\x06remark\x18\x04 \x01(\t\"%\n\x14GetAccountByPhoneReq\x12\r\n\x05phone\x18\x01 \x01(\t\"j\n\x16GetAccountByPhoneReply\x12$\n\x03\x65rr\x18\x01 \x01(\x0e\x32\x17.admin.service.v1.Error\x12*\n\x07\x61\x63\x63ount\x18\x02 \x01(\x0b\x32\x19.admin.service.v1.Account\"!\n\x12GetAccountByUIDReq\x12\x0b\n\x03uid\x18\x01 \x01(\t\"h\n\x14GetAccountByUIDReply\x12$\n\x03\x65rr\x18\x01 \x01(\x0e\x32\x17.admin.service.v1.Error\x12*\n\x07\x61\x63\x63ount\x18\x02 \x01(\x0b\x32\x19.admin.service.v1.Account\"$\n\x15ListCompaniesByUidReq\x12\x0b\n\x03uid\x18\x01 \x03(\t\"\x12\n\x10ListCompaniesReq\"m\n\rCompanyConfig\x12<\n\talgConfig\x18\x01 \x01(\x0b\x32).admin.service.v1.CompanyConfig.AlgConfig\x1a\x1e\n\tAlgConfig\x12\x11\n\tinventory\x18\x01 \x01(\t\"w\n\x07\x43ompany\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07modules\x18\x03 \x03(\t\x12\x0f\n\x07\x65xpired\x18\x04 \x01(\x03\x12/\n\x06\x63onfig\x18\x05 \x01(\x0b\x32\x1f.admin.service.v1.CompanyConfig\"h\n\x12ListCompaniesReply\x12$\n\x03\x65rr\x18\x01 \x01(\x0e\x32\x17.admin.service.v1.Error\x12,\n\tcompanies\x18\x02 \x03(\x0b\x32\x19.admin.service.v1.Company*8\n\x05\x45rror\x12\x06\n\x02OK\x10\x00\x12\x15\n\x11\x41\x43\x43OUNT_NOT_EXIST\x10\x01\x12\x10\n\x0cSERVER_FAULT\x10\x14\x32\x98\x03\n\x05\x41\x64min\x12g\n\x11GetAccountByPhone\x12&.admin.service.v1.GetAccountByPhoneReq\x1a(.admin.service.v1.GetAccountByPhoneReply\"\x00\x12\x61\n\x0fGetAccountByUID\x12$.admin.service.v1.GetAccountByUIDReq\x1a&.admin.service.v1.GetAccountByUIDReply\"\x00\x12[\n\rListCompanies\x12\".admin.service.v1.ListCompaniesReq\x1a$.admin.service.v1.ListCompaniesReply\"\x00\x12\x66\n\x13ListCompaniesByUIDs\x12\'.admin.service.v1.ListCompaniesByUidReq\x1a$.admin.service.v1.ListCompaniesReply\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'admin_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ERROR._serialized_start=786
  _ERROR._serialized_end=842
  _ACCOUNT._serialized_start=33
  _ACCOUNT._serialized_end=100
  _GETACCOUNTBYPHONEREQ._serialized_start=102
  _GETACCOUNTBYPHONEREQ._serialized_end=139
  _GETACCOUNTBYPHONEREPLY._serialized_start=141
  _GETACCOUNTBYPHONEREPLY._serialized_end=247
  _GETACCOUNTBYUIDREQ._serialized_start=249
  _GETACCOUNTBYUIDREQ._serialized_end=282
  _GETACCOUNTBYUIDREPLY._serialized_start=284
  _GETACCOUNTBYUIDREPLY._serialized_end=388
  _LISTCOMPANIESBYUIDREQ._serialized_start=390
  _LISTCOMPANIESBYUIDREQ._serialized_end=426
  _LISTCOMPANIESREQ._serialized_start=428
  _LISTCOMPANIESREQ._serialized_end=446
  _COMPANYCONFIG._serialized_start=448
  _COMPANYCONFIG._serialized_end=557
  _COMPANYCONFIG_ALGCONFIG._serialized_start=527
  _COMPANYCONFIG_ALGCONFIG._serialized_end=557
  _COMPANY._serialized_start=559
  _COMPANY._serialized_end=678
  _LISTCOMPANIESREPLY._serialized_start=680
  _LISTCOMPANIESREPLY._serialized_end=784
  _ADMIN._serialized_start=845
  _ADMIN._serialized_end=1253
# @@protoc_insertion_point(module_scope)