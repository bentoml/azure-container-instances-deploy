# BentoML deployment tool use Cerberus to validate the input.
OPERATOR_SCHEMA = {
    "resource_group": {
        "type": "string",
        "required": True,
        "help_message": "Resource group into which the resources have to be created.",
    },
    "acr_name": {
        "type": "string",
        "required": True,
        "help_message": "The name of Azure Container Registry to use to store images.",
    },
    "cpu": {
        "default": 1,
        "help_message": "The required number of CPU cores of the containers.",
    },
    "memory": {
        "default": 1,
        "help_message": "The required memory of the containers in GB.",
    },
    "bentoml_port": {
        "type": "string",
        "default": "3000",
        "help_message": "Public port to expose bentoml service.",
    },
}
