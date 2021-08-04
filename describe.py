import sys
import json

from utils import get_configuration_value, run_shell_command
from azure import generate_resource_names


def describe(deployment_name, config_json):
    deployment_config = get_configuration_value(config_json)
    _, aci_name = generate_resource_names(deployment_name)

    out, err = run_shell_command(
        [
            "az",
            "container",
            "show",
            "--name",
            aci_name,
            "--resource-group",
            deployment_config["resource_group_name"],
        ]
    )

    description = {}
    description["state"] = out["instanceView"]["state"]
    description["IPAddress"] = out["ipAddress"]

    return description


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Please provide deployment_name and configuration json")
    deployment_name = sys.argv[1]
    config_json = sys.argv[2] if sys.argv[2] else "ec2_config.json"

    description = describe(deployment_name, config_json)
    print(json.dumps(description, indent=2))
