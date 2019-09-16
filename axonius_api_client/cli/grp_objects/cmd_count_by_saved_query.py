# -*- coding: utf-8 -*-
"""Command line interface for Axonius API Client."""
from __future__ import absolute_import, division, print_function, unicode_literals

import click

from .. import context


@click.command("count-by-saved-query", context_settings=context.CONTEXT_SETTINGS)
@context.connect_options
@context.export_options
@click.option(
    "--name",
    "-n",
    help="Name of saved query to get count of assets from.",
    required=True,
    show_envvar=True,
    show_default=True,
)
@context.pass_context
@click.pass_context
def cmd(
    clickctx,
    ctx,
    url,
    key,
    secret,
    export_format,
    export_file,
    export_path,
    export_overwrite,
    name,
):
    """Get all objects matching a query."""
    client = ctx.start_client(url=url, key=key, secret=secret)

    api = getattr(client, clickctx.parent.command.name)

    with context.exc_wrap(wraperror=ctx.wraperror):
        raw_data = api.count_by_saved_query(name=name)

    formatters = {"json": context.to_json}

    ctx.handle_export(
        raw_data=raw_data,
        formatters=formatters,
        export_format=export_format,
        export_file=export_file,
        export_path=export_path,
        export_overwrite=export_overwrite,
    )
