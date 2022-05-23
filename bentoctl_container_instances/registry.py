from bentoctl.exceptions import BentoctlException
from bentoctl.utils.operator_helpers import run_shell_command

DOCKER_USERNAME = "00000000-0000-0000-0000-000000000000"
ACR_DOMAIN = "{acr_name}.azurecr.io/{repository_name}"


def check_admin_user_ennabled(acr_name: str, resource_group: str):
    out, _ = run_shell_command(
        [
            "az",
            "acr",
            "show",
            "--name",
            acr_name,
            "--resource-group",
            resource_group,
            "--query",
            "adminUserEnabled",
        ]
    )

    if out is False:
        raise BentoctlException(
            f"Azure Container Registry {acr_name} doesnot have Admin Account ennabled. Run `az acr update -n {acr_name} --admin-enabled true` to ennable it. For more information check: https://docs.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli#admin-account"
        )


def get_access_token(acr_name: str):
    access_token, _ = run_shell_command(
        [
            "az",
            "acr",
            "login",
            "--name",
            acr_name,
            "--expose-token",
            "--output",
            "tsv",
            "--query",
            "accessToken",
        ]
    )
    return access_token.strip()


def create_repository(deployment_name, operator_spec):
    """
    Create a repository in Azure Container Registry and return the information
    """
    check_admin_user_ennabled(
        acr_name=operator_spec["acr_name"],
        resource_group=operator_spec["resource_group"],
    )

    repository_url = ACR_DOMAIN.format(
        acr_name=operator_spec["acr_name"], repository_name=deployment_name
    )
    password = get_access_token(operator_spec["acr_name"])
    return repository_url, DOCKER_USERNAME, password


def delete_repository(deployment_name, operator_spec):
    """
    Delete the repository crated in Azure Container Registry
    """
    run_shell_command(
        [
            "az",
            "acr",
            "repository",
            "delete",
            "--name",
            operator_spec["acr_name"],
            "--repository",
            deployment_name,
            "--yes",
        ]
    )
