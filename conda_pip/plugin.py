# Copyright (C) 2022 Anaconda, Inc
# Copyright (C) 2023 conda
# SPDX-License-Identifier: BSD-3-Clause
from conda import plugins

from .cli import configure_parser, execute
from .main import ensure_target_env_has_externally_managed

@plugins.hookimpl
def conda_subcommands():
    yield plugins.CondaSubcommand(
        name="pip",
        summary="Run pip commands within conda environments in a safer way",
        action=execute,
        configure_parser=configure_parser,
    )


@plugins.hookimpl
def conda_post_commands():
    yield plugins.CondaPostCommand(
        name="conda-pip-ensure-target-env-has-externally-managed",
        action=ensure_target_env_has_externally_managed,
        run_for={"install", "create", "update", "remove"},
    )