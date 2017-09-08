
# -*- coding: utf-8 -*-
from .device_group import DeviceGroup
from app.model import Base

from sqlalchemy import Column, ForeignKeyConstraint, ForeignKey
from sqlalchemy import String, Integer, LargeBinary


class Device(Base):

    device_id = Column(Integer, primary_key=True, nullable=False)
    device_ext_id = Column(String(60), nullable=False)
    device_int_id = Column(String(60), nullable=False)
    device_msisdn = Column(String(20), nullable=False, unique=True)
    device_group_id = Column(Integer, ForeignKey(DeviceGroup.group_id), nullable=False)
    device_state = Column(String(20), nullable=False)


    @classmethod
    def get_id(cls):
        return Device.tenant_id

    def __repr__(self):
        return "<Device(device_ext_id='%s', device_int_id='%s', device_msisdn='%s')>" % \
            self.device_ext_id, self.device_int_id, self.device_msisdn

    @classmethod
    def find_device_by_msisdn(cls, session, key):
        return session.query(cls).filter(cls.device_msisdn == key).one()

    @classmethod
    def find_device_and_update_state(cls, session, key, args):
        device_db = session.query(cls).filter(cls.device_msisdn == key).one()
        device_db.device_state = args
        session.commit()

    FIELDS = {
        'device_ext_id': str,
        'device_int_id': str,
        'device_msisdn': str
    }

    FIELDS.update(Base.FIELDS)
