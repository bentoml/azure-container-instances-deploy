import sys

from .utils import run_shell_command
from .azure import generate_resource_names


def delete(deployment_name, deployment_spec):
    acr_name, aci_name = generate_resource_names(deployment_name)

    print("Deleting ACR")
    run_shell_command(
        [
            "az",
            "acr",
            "delete",
            "--name",
            acr_name,
            "--resource-group",
            deployment_spec["resource_group_name"],
            "--yes",
        ]
    )

    print("Deleting Container Instance")
    run_shell_command(
        [
            "az",
            "container",
            "delete",
            "--name",
            aci_name,
            "--resource-group",
            deployment_spec["resource_group_name"],
            "--yes",
        ]
    )
