from sqlalchemy import Column
from sqlalchemy import String, Integer, LargeBinary
from sqlalchemy.dialects.postgresql import JSONB

from app.model import Base
from app.config import UUID_LEN
from app.utils import alc
from sqlalchemy import Column, ForeignKeyConstraint
from sqlalchemy import String, Integer, LargeBinary

from app.model import Base


class Devices(Base):

    device_id = Column(Integer, primary_key=True, nullable=False)
    device_ext_id = Column(String(20), nullable=False)
    device_int_id = Column(String(20), nullable=False)
    device_msisdn = Column(String(20), nullable=False)
    device_group_id = Column(Integer, nullable=False)
    device_state = Column(String(20), nullable=False)

    ForeignKeyConstraint(['device_group_id'], ['DeviceGroup.group_id'])

    @classmethod
    def get_id(cls):
        return Devices.tenant_id

    def __repr__(self):
        return "<Device(device_ext_id='%s', device_int_id='%s', device_msisdn='%s')>" % \
            self.device_ext_id, self.device_int_id, self.device_msisdn

    FIELDS = {
        'device_ext_id': str,
        'device_int_id': str,
        'device_msisdn': str
    }

    FIELDS.update(Base.FIELDS)
