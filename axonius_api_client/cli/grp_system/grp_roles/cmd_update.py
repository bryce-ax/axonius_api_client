# -*- coding: utf-8 -*-
"""Command line interface for Axonius API Client."""
from ...context import CONTEXT_SETTINGS, click
from ...options import AUTH, add_options
from .grp_common import EXPORT, PERMS, ROLE_NAME, handle_export

OPTIONS = [*AUTH, EXPORT, ROLE_NAME, *PERMS]


@click.command(name="update", context_settings=CONTEXT_SETTINGS)
@add_options(OPTIONS)
@click.pass_context
def cmd(ctx, url, key, secret, export_format, name, **kwargs):
    """Update a roles permissions."""
    client = ctx.obj.start_client(url=url, key=key, secret=secret)

    with ctx.obj.exc_wrap(wraperror=ctx.obj.wraperror):
        data = client.system.roles.update(name=name, **kwargs)
        ctx.obj.echo_ok(f"Updated role {name!r}")

    handle_export(ctx=ctx, data=data, export_format=export_format, **kwargs)
