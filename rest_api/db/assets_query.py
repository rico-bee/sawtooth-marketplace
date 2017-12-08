# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

import rethinkdb as r
from rethinkdb.errors import ReqlNonExistenceError

from api.errors import ApiBadRequest


async def fetch_asset_resource(conn, name):
    try:
        return await r.table('assets')\
            .get_all(name, index='name')\
            .max('start_block_num')\
            .do(lambda asset: (asset['description'] == "").branch(
                asset.without('description'), asset))\
            .do(lambda asset: (asset['rules'] == []).branch(
                asset.without('rules'), asset))\
            .without('start_block_num', 'end_block_num', 'delta_id')\
            .run(conn)
    except ReqlNonExistenceError:
        raise ApiBadRequest(
            "Bad Request: "
            "No asset with the name {} exists".format(name))
