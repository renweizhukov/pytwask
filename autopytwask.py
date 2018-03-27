#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from pytwask import create_app
app = create_app(os.getenv('PYTWASK_ENV', 'dev'))