from sqlalchemy import Column
from sqlalchemy import String, Integer, LargeBinary
from sqlalchemy.dialects.postgresql import JSONB

from app.model import Base
from app.config import UUID_LEN
from app.utils import alchemy