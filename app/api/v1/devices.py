
import falcon

from sqlalchemy.orm.exc import NoResultFound
from cerberus import Validator, ValidationError

from app import log
from app.api.common import BaseResource
from app.utils.hooks import auth_required
from app.model import Device
from app.errors import AppError, InvalidParameterError, DeviceNotExistsError

LOG = log.get_logger()


FIELDS = {
    'device_ext_id': {
        'type': 'string',
        'required': True,
        'minlength': 4,
        'maxlength': 60
    },
    'device_int_id': {
        'type': 'string',
        'required': True,
        'maxlength': 320
    },
    'device_msisdn': {
        'type': 'string',
        'required': True,
        'minlength': 8,
        'maxlength': 64
    },
    'action': {
        'type': 'string',
        'required': True,
        'maxlength': 64
    },
}


def validate_device_create(req, res, resource, params):
    schema = {
        'device_ext_id': FIELDS['device_ext_id'],
        'device_int_id': FIELDS['device_int_id'],
        'device_msisdn': FIELDS['device_msisdn'],
        'action': FIELDS['action']
    }

    v = Validator(schema)
    try:
        if not v.validate(req.context['data']):
            raise InvalidParameterError(v.errors)
    except ValidationError:
        LOG.info(req.context)
        raise InvalidParameterError('Invalid Request %s' % req.context)


class Collection(BaseResource):
    """
    Handle for endpoint: /v1/devices
    """
    @falcon.before(validate_device_create)
    def on_post(self, req, res):
        session = req.context['session']
        device_req = req.context['data']
        LOG.info(req.context)
        if device_req:
            device = Device()
            device.device_ext_id = device_req['device_ext_id']
            device.device_int_id = device_req['device_int_id']
            device.device_msisdn = device_req['device_msisdn']
            action = device_req['action'] if 'action' in device_req else None
            if action == "INIT":
                """
                    For Action INIT create an entry in the Device DB
                """
                LOG.info("action:INIT")
                device.device_group_id = 1
                device.device_state = "INIT"
                session.add(device)
            elif action == "ONBORAD":
                # See if the device exists in the db
                LOG.info("Action = ONBOARD")

            self.on_success(res, None)
        else:
            raise InvalidParameterError(req.context['data'])

    @falcon.before(auth_required)
    def on_get(self, req, res):
        session = req.context['session']
        device_dbs = session.query(Device).all()
        if device_dbs:
            obj = [device_dbs.to_dict() for user in device_dbs]
            self.on_success(res, obj)
        else:
            raise AppError()

    @falcon.before(auth_required)
    def on_put(self, req, res):
        pass


class Item(BaseResource):
    """
    Handle for endpoint: /v1/devices/{key}
    """

    #@falcon.before(auth_required)
    def on_get(self, req, res, key):
        LOG.info(req.path)
        session = req.context['session']
        try:
            device_db = Device.find_device_by_msisdn(session, key)
            LOG.info("Device Id:"+str(device_db.to_dict()))

            self.on_success(res, device_db.to_dict())
        except NoResultFound:
            raise DeviceNotExistsError('Device not found :%s' % key)
