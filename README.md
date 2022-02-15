# Azure Container Instance deployment

Azure Container Instances is a great deployment strategy for deploying ML models endpoints that you know will get a consistant traffic or want to take advantage of accelerators like GPUs. You can also add autoscaling capabilities on top of this.

> Note: For the time being this repos only supports `BentoML <= 0.13`. 
> The Repo is in the process of being migrated to the new BentoML 1.0 release. You can track the progress
> here [#89](https://github.com/bentoml/bentoctl/issues/89). 

## Prerequisites

- An active Azure account configured on the machine with Azure CLI installed and configured
    - Install instruction: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli (Version >= 2.6.0)
    - Configure Azure account instruction: https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli
- Docker is installed and running on the machine.
    - Install instruction: https://docs.docker.com/install
- Install required python packages
    - `$ pip install -r requirements.txt`


## Quickstart
To try this out let us deploy the IrisClassifier demo from the [BentoML quick start guide](https://github.com/bentoml/BentoML/blob/master/guides/quick-start/bentoml-quick-start-guide.ipynb).

1. Build and save Bento Bundle from BentoML quick start guide notebook mentioned above. 

2. Create Azure Container Instance deployment with the deployment tool. Make sure that you copy the [config file](azure_config.json) and make the changes required for your deployment. The reference for the config file is given below.

    Run deploy script in the command line:

    ```bash
    $ BENTO_BUNDLE_PATH=$(bentoml get IrisClassifier:latest --print-location -q)
    $ python deploy.py $BENTO_BUNDLE_PATH iristest azure_config.json

    # Sample output
    Creating Azure ACR iristest0acr
    Build and push image iristest0acr.azurecr.io/irisclassifier:20210803234622_65f4f4
    Generating ACI template
    Creating the Container Instance
    Deployment successful!
    ```



    Get Container Instance deployment information and status

    ```bash
    $ python describe.py iristest azure_config.json

    # Sample output
    {
      "state": "Running",
      "IPAddress": {
        "dnsNameLabel": "iristest-aci",
        "fqdn": "iristest-aci.eastus.azurecontainer.io",
        "ip": "20.81.69.156",
        "ports": [
          {
            "port": 5000,
            "protocol": "TCP"
          }
        ],
        "type": "Public"
      }
    }
    ```

3. Make sample request against deployed service

    ```bash
    $ curl -i \
      --header "Content-Type: application/json" \
      --request POST \
      --data '[[5.1, 3.5, 1.4, 0.2]]' \
        http://iristest-aci.eastus.azurecontainer.io:5000/predict

    # Sample output
    HTTP/1.1 200 OK
    Content-Type: application/json
    X-Request-Id: 3ca3526e-4278-4812-9d30-a448f43e878d
    Content-Length: 3
    Date: Wed, 04 Aug 2021 19:08:43 GMT
    Server: Python/3.8 aiohttp/3.7.4.post0

    [0]%
    ```

4. Delete container instance deployment

    ```bash
    python delete.py iristest azure_config.json
    
    # sample output
    Deleting ACR
    Deleting Container Instance
    ```
    
## Deployment operations

### Create a deployment

Use command line
```bash
$ python deploy.py <Bento_bundle_path> <Deployment_name> <Config_JSON default is azure_config.json>
```

Example:
```bash
$ MY_BUNDLE_PATH=${bentoml get IrisClassifier:latest --print-location -q)
$ python deploy.py $MY_BUNDLE_PATH my_first_deployment azure_config.json
```

Use Python API
```python
from deploy import deploy_to_azure

deploy(BENTO_BUNDLE_PATH, DEPLOYMENT_NAME, CONFIG_JSON)
```


#### Available configuration options for Azure Function deployments

You can have a config file to specify the specifics for your deployment. There is a sample config provide [here](azure_config.json)
```
{
    "resource_group_name": "bentoml",
    "location": "location",
    "acr_sku": "Standard",
    "port": 5000,
    "memory": 2,
    "cpu_count": 1,
    "gpu": {"count": 1, "type": "k80"},
    "environment_vars": {
      "var": "value", 
      "another_var": "value"
    }
}
```

* `resource_group_name`: All Azure resources are created inside a resource group. If you already have a resource group that you would like to use for the deployment, put its name here. If you don't have one, you can easily create it with `az group create --name <rg_name> --location <location>"`
* `location`: Azure region or location that you want to deploy to. By default it will use the same one as your resource group
* `acr_sku`: The SKU of the container registry.  Allowed values: Basic, Classic, Premium, Standard. Default is `Standard`
* `port`: The port you want the endpoint to use. By default it is 5000
* `memory`: The memory (in GBs) you want each instance to have.
* `cpu_count`: The number of CPU cores you want for your instance.
* `gpu`: Optional field which specifies the GPU you want the instance to have. Takes a dict with `count` and `type` specified. Possible types are K80, P100, V100. eg. `"gpu": {"count": 1, "type": "K80"}`
* `environment_vars`: Optional field to specify any additional environment variable you want to pass to the container instance. eg `"environment_vars": {"BENTOML_ENABLE_MICROBATCH": "", "BENTOML_MB_MAX_LATENCY": "100"}`

### Update a deployment

Use command line
```bash
$ python update.py <Bento_bundle_path> <Deployment_name> <Config_JSON>
```

Use Python API
```python
from update import update_azure
update(BENTO_BUNDLE_PATH, DEPLOYMENT_NAME, CONFIG_JSON)
```

Do note that there are some limitation to which all features of the container instance you can update without first deleting and recreating the instance first. Some properties like CPU, memeory or GPU resources will require you to delete and then redeploy but updating images works just fine. If you want more info check out the [official docs](https://docs.microsoft.com/en-us/azure/container-instances/container-instances-update#limitations)

### Get deployment's status and information

Use command line
```bash
$ python describe.py <Deployment_name> <Config_JSON>
```


Use Python API
```python
from describe import describe_azure
describe(DEPLOYMENT_NAME)
```

### Delete deployment

Use command line
```bash
$ python delete.py <Deployment_name> <Config_JSON>
```

Use Python API
```python
from  delete import delete_azure
delete(DEPLOYMENT_NAME)
```
