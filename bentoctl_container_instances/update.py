import sys

from .utils import (
    get_tag_from_path,
    run_shell_command,
    build_docker_image,
    push_docker_image_to_repository,
)
from .azure import generate_resource_names, get_docker_login_info, generate_aci_template


def update(bento_path, deployment_name, deployment_spec):
    bento_metadata = get_tag_from_path(bento_path)

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
            deployment_spec["resource_group_name"],
        ]
    )
    docker_image_tag = (
        f"{acr_name}.azurecr.io/{bento_metadata.name}:{bento_metadata.version}".lower()
    )
    print(f"Build and push image {docker_image_tag}")
    build_docker_image(context_path=bento_path, image_tag=docker_image_tag)
    push_docker_image_to_repository(docker_image_tag)
    docker_username, docker_password = get_docker_login_info(
        deployment_spec["resource_group_name"], acr_name
    )

    print("Updating ACI template")
    template_file_path = generate_aci_template(
        acr_name=acr_name,
        aci_name=aci_name,
        docker_image_tag=docker_image_tag,
        docker_username=docker_username,
        docker_password=docker_password,
        deployment_config=config_json,
    )

    print("Updating the Container Instance")
    run_shell_command(
        [
            "az",
            "container",
            "create",
            "-g",
            deployment_spec["resource_group_name"],
            "-f",
            template_file_path,
        ]
    )
