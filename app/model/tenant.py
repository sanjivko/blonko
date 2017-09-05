from sqlalchemy import Column
from sqlalchemy import String, Integer, LargeBinary

from app.model import Base
from app.utils import alchemy
from app.config import UUID_LEN


class Tenant(Base):

    tenant_id = Column(Integer, primary_key=True, nullable=False)
    tenant_name = Column(String(20), nullable=False,  unique=True)

    # intentionally assigned for user related service such as resetting password: kind of internal user secret key
    sid = Column(String(UUID_LEN), nullable=False)

    @classmethod
    def get_id(cls):
        return Tenant.tenant_id

    def __repr__(self):
        return "<Tenant(tenant_name='%s')>" % \
            self.tenant_name

    FIELDS = {
        'tenant_name': str,
    }

    FIELDS.update(Base.FIELDS)
