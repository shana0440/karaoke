from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class TimestampColumns:
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime,
        nullable=True,
        default=datetime.utcnow,
        server_default=func.now(),
        onupdate=datetime.utcnow,
    )
