# Copyright BigchainDB GmbH and BigchainDB contributors
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

"""This module provides the blueprint for the blocks API endpoints.

For more information please refer to the documentation: http://bigchaindb.com/http-api
"""
from flask import current_app
from flask_restful import Resource, reqparse

from bigchaindb.web.views.base import make_error


class BlockApi(Resource):
    def get(self, block_id):
        """API endpoint to get details about a block.

        Args:
            block_id (str): the id of the block.

        Return:
            A JSON string containing the data about the block.
        """

        pool = current_app.config['bigchain_pool']

        with pool() as bigchain:
            block = bigchain.get_block(block_id=block_id)

        if not block:
            return make_error(404)

        return block


class BlockListApi(Resource):
    def get(self):
        """API endpoint to get the related blocks for a transaction.

        Return:
            A ``list`` of ``block_id``s that contain the given transaction. The
            list may be filtered when provided a status query parameter:
            "valid", "invalid", "undecided".
        """
        parser = reqparse.RequestParser()
        parser.add_argument('transaction_id', type=str, required=True)

        args = parser.parse_args(strict=True)
        tx_id = args['transaction_id']

        pool = current_app.config['bigchain_pool']

        with pool() as bigchain:
            blocks = bigchain.get_block_containing_tx(tx_id)

        return blocks


class BlockListWithParamsApi(Resource):
    def get(self):
        """API endpoint to get the blocks with params.

        Return:
            A ``list`` of ``block_id``s with page params.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('page_size', type=int, required=False, location='args',  default=10)
        parser.add_argument('page', type=int, required=False, location='args', default=1)

        args = parser.parse_args(strict=True)
        page_size = args['page_size']
        page = args['page']

        pool = current_app.config['bigchain_pool']

        with pool() as bigchain:
            blocks = bigchain.get_block_list(page_size,page)

        return blocks

class BlockCount(Resource):
    def get(self):
        """API endpoint to get the blocks count.

        Return:
            A number of block count.
        """

        pool = current_app.config['bigchain_pool']

        with pool() as bigchain:
            count = bigchain.get_block_count()

        return count