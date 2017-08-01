#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:xieshengsen


def file_db_handle(conn_params):
    db_path = '%s/%s' % (conn_params['path'], conn_params['name'])
    return db_path


def db_handler(conn_parms):
    if conn_parms['engine'] == 'file_storage':
        return file_db_handle(conn_parms)