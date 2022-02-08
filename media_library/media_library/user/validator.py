from typing import Optional

from sqlalchemy.orm import Session

from media_library.user.model import User


async def verify_email_exist(email: str, db_session: Session) -> Optional[User]:
    return db_session.query(User).filter(User.email == email).first()
