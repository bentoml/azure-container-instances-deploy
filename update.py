import sys
import os

from bentoml.saved_bundle import load_bento_service_metadata

from utils import (
    get_configuration_value,
    run_shell_command,
    build_docker_image,
    push_docker_image_to_repository,
)
from azure import generate_resource_names, get_docker_login_info, generate_aci_template


def update(bento_bundle_path, deployment_name, config_json):
    bento_metadata = load_bento_service_metadata(bento_bundle_path)
    azure_config = get_configuration_value(config_json)

    acr_name, aci_name = generate_resource_names(deployment_name)

    # build and push docker
    run_shell_command(
        [
            "az",
            "acr",
            "login",
            "--name",
            acr_name,
            "--resource-group",
            azure_config["resource_group_name"],
        ]
    )
    docker_image_tag = (
        f"{acr_name}.azurecr.io/{bento_metadata.name}:{bento_metadata.version}".lower()
    )
    print(f"Build and push image {docker_image_tag}")
    build_docker_image(context_path=bento_bundle_path, image_tag=docker_image_tag)
    push_docker_image_to_repository(docker_image_tag)
    docker_username, docker_password = get_docker_login_info(
        azure_config['resource_group_name'], acr_name
    )

    print("Updating ACI template")
    template_file_path = generate_aci_template(
        acr_name=acr_name,
        aci_name=aci_name,
        docker_image_tag=docker_image_tag,
        docker_username=docker_username,
        docker_password=docker_password,
        config_json=config_json,
    )

    print("Updating the Container Instance")
    run_shell_command(
        [
            "az",
            "container",
            "create",
            "-g",
            azure_config["resource_group_name"],
            "-f",
            template_file_path,
        ]
    )


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise Exception(
            "Please provide bento_bundle_path deployment_name and configuration json"
        )
    bento_bundle_path = sys.argv[1]
    deployment_name = sys.argv[2]
    config_json = sys.argv[3] if sys.argv[3] else "azure_config.json"

    update(bento_bundle_path, deployment_name, config_json)
    print("Updation successful!")
