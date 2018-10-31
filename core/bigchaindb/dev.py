# Copyright BigchainDB GmbH and BigchainDB contributors
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

import logging
import setproctitle

import bigchaindb

from bigchaindb.start import start
from argparse import Namespace

args = Namespace(config=None, yes=True, skip_initialize_database=False, experimental_parallel_validation=False)
start(args)