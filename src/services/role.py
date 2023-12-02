from uuid import UUID

from repository.database import AbstractRepository  # , RoleRepository


class RoleService:
    def __init__(self, repository: AbstractRepository) -> None:
        self.repository: AbstractRepository = repository

    async def set_role(self, user_id: UUID, role_name: str) -> None:
        pass

    async def delete_role(self, user_id: UUID, role_name: str) -> None:
        pass


def get_role_service(): # -> RoleService:
    return None
    # return RoleService(RoleRepository())