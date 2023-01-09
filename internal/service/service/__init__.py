from . import service


__all__ = [
    'new_service',
    'AdminService'
]

new_service = service.new_service
AdminService = service.AdminService
