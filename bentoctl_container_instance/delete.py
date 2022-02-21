import sys

from utils import get_configuration_value, run_shell_command
from azure import generate_resource_names


def delete(deployment_name, config_json):
    deployment_config = get_configuration_value(config_json)
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
            deployment_config["resource_group_name"],
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
            deployment_config["resource_group_name"],
            "--yes",
        ]
    )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Please provide deployment_name and configuration json")
    deployment_name = sys.argv[1]
    config_json = sys.argv[2] if sys.argv[2] else "ec2_config.json"

    delete(deployment_name, config_json)
