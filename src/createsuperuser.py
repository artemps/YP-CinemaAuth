from asyncio import run as aiorun
import typer

from api.v1.users.schemas import UserCreateIn
from services import get_user_service, get_security_service
from repository.schemas import Roles


def main(login: str = typer.Argument("admin"), password: str = typer.Argument("adminadmin")):
    async def createsuperuser():
        user = UserCreateIn(
            login=login,
            password=password,
            first_name='Superuser',
            last_name='Superuser'
        )
        user_service = get_user_service()
        user = await user_service.create(user, get_security_service())
        user = await user_service.repository.set_user_role(user.id, Roles.ADMIN)
        print(f"Created {user.first_name} {user.last_name}")
    aiorun(createsuperuser())


if __name__ == "__main__":
    typer.run(main)
