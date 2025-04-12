# app/db/init_db.py
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user import create_user
from sqlalchemy import select


logger = logging.getLogger(__name__)

async def create_first_superuser() -> None:
    async with AsyncSessionLocal() as db:
        # Use select() instead of query()
        result = await db.execute(select(User).where(User.email == settings.FIRST_SUPERUSER))
        user = result.scalars().first()
        
        if not user:
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
                full_name="Initial Admin"
            )
            await create_user(db=db, user_create=user_in)
            logger.info("Created first superuser")

# async def create_first_superuser() -> None:
#     async with AsyncSessionLocal() as db:
#         user = await db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
#         if not user:
#             user_in = UserCreate(
#                 email=settings.FIRST_SUPERUSER,
#                 password=settings.FIRST_SUPERUSER_PASSWORD,
#                 is_superuser=True,
#                 full_name="Initial Admin"
#             )
#             await create_user(db=db, user_create=user_in)
#             logger.info("Created first superuser")
