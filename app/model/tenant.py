from sqlalchemy import Column
from sqlalchemy import String, Integer, LargeBinary

from app.model import Base
from app.utils import alchemy

class Tenant(Base):
    __tablename__ = "tenant"

    tenant_id = Column(Integer, primary_key=True)
    tenant_name = Column(String(20), nullable=False)

    @classmethod
    def get_id(cls):
        return Tenant.tenant_id

    def __repr__(self):
        return "<Tenant(tenant_name='%s')>" % \
            (self.username)

    FIELDS = {
        'tenant_name': str,
    }
