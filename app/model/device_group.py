from sqlalchemy import Column, ForeignKeyConstraint
from sqlalchemy import String, Integer, LargeBinary

from app.model import Base
from app.config import UUID_LEN


class DeviceGroup(Base):

    group_id = Column(Integer, primary_key=True, nullable=False)
    group_name = Column(String(20), nullable=False, unique=True)
    tenant_id = Column(Integer, nullable=False)

    @classmethod
    def get_id(cls):
        return DeviceGroup.group_id

    def __repr__(self):
        return "<DeviceGroup(group_name='%s')>" % \
            self.group_name_name

    FIELDS = {
        'group_name': str,
    }

    FIELDS.update(Base.FIELDS)
