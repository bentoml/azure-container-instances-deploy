OPERATOR_NAME = "azure-container-instances"

OPERATOR_MODULE = "bentoctl_container_instances"

# BentoML deployment tool use Cerberus to validate the input. The following is an example of the schema validation.
OPERATOR_SCHEMA = {
    "resource_group_name": {
        "type": "string",
        "help_message": "Resource group into which the resources have to be created.",
        "required": True,
    },
    "location": {
        "type": "string",
        "help_message": "Azure region or location that you want to deploy to. By default it will use the same one as your resource group",
    },
    "acr_sku": {
        "type": "string",
        "help_message": "The SKU of the container registry.",
        "allowed": ["Basic", "Classic", "Premium", "Standard"],
        "default": "Standard",
    },
    "port": {
        "type": "integer",
        "help_message": "The port you want the endpoint to use.",
        "default": 5000,
        "coerce": int,
    },
    "memory": {
        "type": "integer",
        "help_message": "The amount of memory to allocate to the container in gigabytes.",
        "default": 2,
        "coerce": int,
    },
    "cpu_count": {
        "type": "integer",
        "help_message": "The number of CPU cores to allocate to the container.",
        "default": 1,
        "coerce": int,
    },
    "gpu": {
        "type": "dict",
        "help_message": "The number of CPU cores to allocate to the container.",
        "schema": {
            "count": {
                "type": "integer",
                "help_message": "The number of GPUs to allocate to the container",
                "coerce": int,
            },
            "type": {
                "type": "string",
                "help_message": "GPU type that should be allocated. Possible types are K80, P100, V100",
                "allowed": ["K80", "P100", "V100"],
            },
        },
    },
    "environment_variables": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {
                    "type": "string",
                    "help_message": "Name for environment variable",
                },
                "value": {
                    "type": "string",
                    "help_message": "Value for the environment variables",
                },
            },
        },
    },
}
