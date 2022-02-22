import sys
import json

from .utils import run_shell_command
from .azure import generate_resource_names


def describe(deployment_name, deployment_spec):
    _, aci_name = generate_resource_names(deployment_name)

    out, err = run_shell_command(
        [
            "az",
            "container",
            "show",
            "--name",
            aci_name,
            "--resource-group",
            deployment_spec["resource_group_name"],
        ]
    )

    description = {}
    description["state"] = out["instanceView"]["state"]
    description["IPAddress"] = out["ipAddress"]

    return description
