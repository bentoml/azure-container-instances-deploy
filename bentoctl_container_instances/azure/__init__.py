import os
import re

from ruamel.yaml import YAML

from ..utils import run_shell_command
from .container_instance_template import ACI_TEMPLATE


def get_docker_login_info(resource_group_name, container_registry_name):
    run_shell_command(
        [
            "az",
            "acr",
            "update",
            "--name",
            container_registry_name,
            "--admin-enabled",
            "true",
        ],
    )
    docker_login_info, err = run_shell_command(
        [
            "az",
            "acr",
            "credential",
            "show",
            "--name",
            container_registry_name,
            "--resource-group",
            resource_group_name,
        ]
    )

    if err.strip() != "":
        print("Error: ", err)
    return docker_login_info["username"], docker_login_info["passwords"][0]["value"]


def generate_resource_names(deployment_name):
    # Generate resource names base on
    # https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/resource-name-rules

    # 5-50, alphanumeric scope global
    container_registry_name = f"{deployment_name[:40]}-acr"
    container_registry_name = re.sub(
        re.compile("[^a-zA-Z0-9]"), "0", container_registry_name
    )

    # 1-63, Lowercase letters, numbers, and hyphens.
    container_instance_name = f"{deployment_name[:59]}-aci".lower()
    container_instance_name = re.sub(
        re.compile("[^a-z0-9]"), "-", container_instance_name
    )

    return (
        container_registry_name,
        container_instance_name,
    )


def generate_aci_template(
    acr_name,
    aci_name,
    docker_image_tag,
    docker_username,
    docker_password,
    deployment_config,
):
    """
    Generate the template YAML file that specifies the properties of the container
    instances. The generated YAML file is stored in the same location as the config
    file location passed.
    """
    template = ACI_TEMPLATE.format(
        container_group_name=aci_name,
        aci_name=aci_name,
        docker_image_tag=docker_image_tag,
        docker_username=docker_username,
        docker_password=docker_password,
        port=deployment_config["port"],
        dns_name=deployment_config.get("dns_name", aci_name),
        memory=deployment_config["memory"],
        cpu_count=deployment_config["cpu_count"],
        acr_sku=deployment_config["acr_sku"],
        acr_name=acr_name
    )

    yaml = YAML()
    yaml.preserve_quotes = True
    template = yaml.load(template)

    if deployment_config.get("environment_vars") is not None:
        env_vars = []
        for var, value in deployment_config["environment_vars"].items():
            env_vars.append({"name": var, "value": value})

        # add the environment variables in the deployment_config
        template["properties"]["containers"][0]["properties"][
            "environmentVariables"
        ] = env_vars

    if deployment_config.get("gpu") is not None:
        # manually adding the gpu configuration from the deployment_config
        template["properties"]["containers"][0]["properties"]["resources"]["requests"][
            "gpu"
        ] = {
            "count": deployment_config["gpu"]["count"],
            "sku": deployment_config["gpu"]["type"],
        }

    template_file_path = os.path.join(config_dir, "aci_template.yaml")
    with open(template_file_path, 'w') as f:
        yaml.dump(template, f)

    return template_file_path
