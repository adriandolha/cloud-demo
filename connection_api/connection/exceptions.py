class ResourceNotFoundException(Exception):
    def __init__(self, resource_id):
        super().__init__(f'Resource {resource_id} not found.')
