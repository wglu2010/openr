#
# Copyright (c) 2014-present, Facebook, Inc.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import click
import zmq

from thrift.protocol.TCompactProtocol import TCompactProtocolFactory
from thrift.protocol.TJSONProtocol import TJSONProtocolFactory

from openr.cli.commands import config
from openr.utils.consts import Consts
from openr.cli.utils import utils


class ConfigContext(object):
    def __init__(self, verbose, zmq_ctx, timeout, config_store_url, json):
        '''
            :param zmq_ctx: the ZMQ context to create zmq sockets
            :para json bool: whether to use JSON proto or Compact for thrift
        '''

        self.verbose = verbose
        self.timeout = timeout
        self.zmq_ctx = zmq_ctx

        self.config_store_url = config_store_url

        self.proto_factory = (TJSONProtocolFactory if json
                              else TCompactProtocolFactory)


class ConfigCli(object):
    def __init__(self):
        self.config.add_command(ConfigPrefixAllocatorCli().config_prefix_allocator,
                                name='prefix-allocator')
        self.config.add_command(ConfigLinkMonitorCli().config_link_monitor,
                                name='link-monitor')
        self.config.add_command(ConfigPrefixManagerCli().config_prefix_manager,
                                name='prefix-manager')
        self.config.add_command(ConfigEraseCli().config_erase, name='erase')
        self.config.add_command(ConfigStoreCli().config_store, name='store')

    @click.group()
    @click.option('--config_store_url', default=None, help='Config Store IPC URL')
    @click.option('--json/--no-json', default=False,
                  help='Use JSON serializer')
    @click.option('--verbose/--no-verbose', default=False,
                  help='Print verbose information')
    @click.pass_context
    def config(ctx, config_store_url, json, verbose):  # noqa: B902
        ''' CLI tool to peek into Config Store module. '''

        config_store_url = config_store_url or "{}_{}".format(
            Consts.CONFIG_STORE_URL_PREFIX,
            utils.get_connected_node_name(
                ctx.obj.hostname,
                ctx.obj.ports_config.get('lm_cmd_port', None) or
                Consts.LINK_MONITOR_CMD_PORT))

        ctx.obj = ConfigContext(
            verbose, zmq.Context(),
            ctx.obj.timeout,
            ctx.obj.ports_config.get('config_store_url', None) or config_store_url,
            json)


class ConfigPrefixAllocatorCli(object):

    @click.command()
    @click.pass_obj
    def config_prefix_allocator(cli_opts):  # noqa: B902
        ''' Dump prefix allocation config '''

        config.ConfigPrefixAllocatorCmd(cli_opts).run()


class ConfigLinkMonitorCli(object):

    @click.command()
    @click.pass_obj
    def config_link_monitor(cli_opts):  # noqa: B902
        ''' Dump link monitor config '''

        config.ConfigLinkMonitorCmd(cli_opts).run()


class ConfigPrefixManagerCli(object):

    @click.command()
    @click.pass_obj
    def config_prefix_manager(cli_opts):  # noqa: B902
        ''' Dump link monitor config '''

        config.ConfigPrefixManagerCmd(cli_opts).run()


class ConfigEraseCli(object):

    @click.command()
    @click.argument('key')
    @click.pass_obj
    def config_erase(cli_opts, key):  # noqa: B902
        ''' Erase a config key '''

        config.ConfigEraseCmd(cli_opts).run(key)


class ConfigStoreCli(object):

    @click.command()
    @click.argument('key')
    @click.argument('file')
    @click.pass_obj
    def config_store(cli_opts, key, file):  # noqa: B902
        ''' Store a config key '''

        config.ConfigStoreCmd(cli_opts).run(key, file)
