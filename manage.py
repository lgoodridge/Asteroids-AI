"""
Script for running management commands for the Asteroids Game / AI.

Usage: python manage.py [--help]
"""

import click

from ai.experiment import merge_experiments
from settings import get_settings, load_settings_from_cli


class TransparentGroup(click.Group):
    """
    A Click Group class that passes all provided
    arguments to its subcommands without processing them.
    """

    def invoke(self, ctx):
        ctx.obj = tuple(ctx.args)
        super(TransparentGroup, self).invoke(ctx)


@click.group(cls=TransparentGroup)
@click.pass_context
def manage(ctx):
    args = ctx.obj


@manage.command(
    short_help="Merges experiments into a new experiment",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
@click.argument("parent_dirs", nargs=-1)
@click.argument("output_dir")
@click.pass_context
def merge(ctx, parent_dirs, output_dir):
    """
    Merges the best brains of the parent experment directories
    into a new directory, and initializes (but does not run)
    that experiment:

    \b
    The settings passed to this command will be used to initialize
    and perform the initial evaluation of the merged experiment.

    \b
    Arguments:
      parent_dirs - Directories of parent experiments to merge.
      output_dir  - Directory to place the merged experiment into.
    """
    # Remove all options from the directory arguments
    parent_dirs = [x for x in list(parent_dirs) if not x.startswith("--")]
    if output_dir.startswith("--"):
        output_dir = parent_dirs.pop() if len(parent_dirs) > 0 else ""

    # Load settings from cli, then actually merge the experiments
    load_settings_from_cli()
    merge_experiments(parent_dirs, output_dir)


@manage.command("settings", short_help="View configurable settings")
@click.pass_context
def view_settings(ctx):
    """
    View the configurable settings for the other commands.
    """
    settings = get_settings()
    click.echo(settings.cli_configure_settings.get_help(ctx))


if __name__ == "__main__":
    manage()
