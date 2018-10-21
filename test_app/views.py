#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
Application APIs
"""
from flask import Blueprint, jsonify, request
from flask import current_app as app

from lib.errors import BadRequestException, ObjectNotFoundException
from test_app.controllers import AddressController

address_api = Blueprint('address_api', __name__, url_prefix='/address')


@address_api.route('/', methods=['POST'], strict_slashes=False)
def update_vrf_common_data():
    address_controller = AddressController(logger=app.logger)

    input_file = request.files.get('file')
    if not input_file:
        raise BadRequestException(error_message='no_file_attached')

    try:
        result = address_controller.get_address(input_file)
    except ValueError as e:
        raise BadRequestException(error_message=e.message)
    except RuntimeError as e:
        raise ObjectNotFoundException(error_message=e.message)

    return jsonify({'success': True, 'result': result})
