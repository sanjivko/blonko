import re
import falcon

from sqlalchemy.orm.exc import NoResultFound
from cerberus import Validator, ValidationError

from app import log
from app.api.common import BaseResource
from app.utils.hooks import auth_required
from app.utils.auth import encrypt_token, hash_password, verify_password, uuid
from app.model import Tenant
from app.errors import AppError, InvalidParameterError, UserNotExistsError, PasswordNotMatch

LOG = log.get_logger()

FIELDS = {
    'tenant_name': {
        'type': 'string',
        'required': True,
        'minlength': 4,
        'maxlength': 20
    },
}

def validate_tenant_create(req, res, resource, params):
    schema = {
        'tenant_name': FIELDS['tenant_name'],
    }

    v = Validator(schema)
    try:
        if not v.validate(req.context['data']):
            raise InvalidParameterError(v.errors)
    except ValidationError:
        raise InvalidParameterError('Invalid Request %s' % req.context)


class Collection(BaseResource):
    """
    Handle for endpoint: /v1/tenants
    """
    @falcon.before(validate_tenant_create)
    def on_post(self, req, res):
        session = req.context['session']
        user_req = req.context['data']
        if user_req:
            tenant = Tenant()
            tenant.tenant_name = user_req['tenant_name']
            sid = uuid()
            session.add(tenant)
            self.on_success(res, None)
        else:
            raise InvalidParameterError(req.context['data'])

    @falcon.before(auth_required)
    def on_get(self, req, res):
        session = req.context['session']
        tenant_dbs = session.query(Tenant).all()
        if tenant_dbs:
            obj = [tenant.to_dict() for tenant in tenant_dbs]
            self.on_success(res, obj)
        else:
            raise AppError()

    @falcon.before(auth_required)
    def on_put(self, req, res):
        pass
