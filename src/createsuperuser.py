from asyncio import run as aiorun
import typer

from api.v1.users.schemas import UserCreateIn
from services import get_user_service, get_role_service
from repository.schemas import Roles


def main(email: str = typer.Argument("admin"), password: str = typer.Argument("adminadmin")):
    async def createsuperuser():
        user = UserCreateIn(
            email=email,
            password=password,
            first_name='Superuser',
            last_name='Superuser'
        )
        user_service, role_service = get_user_service(), get_role_service()
        user = await user_service.create(user)
        await role_service.set(user.id, Roles.ADMIN)
        print(f"Created {user.first_name} {user.last_name}")
    aiorun(createsuperuser())


if __name__ == "__main__":
    typer.run(main)
