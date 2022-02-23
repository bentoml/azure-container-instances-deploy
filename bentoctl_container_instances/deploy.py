from bentoml.bentos import containerize

from .utils import (
    get_tag_from_path,
    push_docker_image_to_repository,
)
from .azure import generate_resource_names, get_docker_login_info, generate_aci_template


def deploy(bento_path, deployment_name, deployment_spec):
    bento_tag = get_tag_from_path(bento_path)

    _, aci_name = generate_resource_names(deployment_name)

    docker_image_tag = f"{deployment_spec['acr_name']}.azurecr.io/{bento_tag.name}:{bento_tag.version}".lower()
    print(f"Build and push image {docker_image_tag}")
    containerize(bento_tag, docker_image_tag=docker_image_tag)
    docker_username, docker_password = get_docker_login_info(
        deployment_spec["resource_group_name"], deployment_spec["acr_name"]
    )
    push_docker_image_to_repository(
        docker_image_tag, username=docker_username, password=docker_password
    )

    print("Generating ACI template")
    template_file_path = generate_aci_template(
        acr_name=deployment_spec["acr_name"],
        aci_name=aci_name,
        docker_image_tag=docker_image_tag,
        docker_username=docker_username,
        docker_password=docker_password,
        deployment_config=deployment_spec,
    )
