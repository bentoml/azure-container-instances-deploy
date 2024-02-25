## ⚠️ BentoCTL project has been deprecated

Plese see the latest BentoML documentation on OCI-container based deployment workflow: https://docs.bentoml.com/

## Azure Container Instance deployment

Azure Container Instances is a great deployment strategy for deploying ML models endpoints that you know will get a consistant traffic or want to take advantage of accelerators like GPUs. You can also add autoscaling capabilities on top of this. Using [BentoML](https://github.com/bentoml/BentoML) and [bentoctl](https://github.com/bentoml/bentoctl), you can use with your favourite ML frameworks and easily manage your infrastructure via terraform.

> **Note:** This operator is compatible with BentoML version 1.0.0 and above. For older versions, please switch to the branch `pre-v1.0` and follow the instructions in the README.md. 

## Table of Contents

   * [Quickstart](#quickstart)
   * [Configuration Options](#configuration-options)

## Quickstart

This quickstart will walk you through deploying a bento into Azure Container Instances. Make sure to go through the [prerequisites](#prerequisites) section and follow the instructions to set everything up.

### Prerequisites

1. Azure CLI - An active Azure account configured on the machine with Azure CLI installed and configured
    - Install instruction: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli (Version >= 2.6.0)
    - Configure Azure account instruction: https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli
2. Terraform - Terraform is a tool for building, configuring, and managing infrastructure. Installation instruction: www.terraform.io/downloads
3. Docker - Install instruction: https://docs.docker.com/install
4. A working bento - for this guide, we will use the iris-classifier bento from the BentoML [quickstart guide](https://docs.bentoml.org/en/latest/quickstart.html#quickstart).

### Steps
1. Install bentoctl via pip
    ```bash
    pip install bentoctl
    ```

2. Install the operator

    Bentoctl will install the official Azure Container Instances operator and its dependencies. The Operator contains the Terraform templates and sets up the registries reqired to deploy to Azure.

    ```bash
    bentoctl operator install azure-container-instances
    ```

3. Initialize deployment with bentoctl

    Follow the interactive guide to initialize the deployment project.

    ```bash
    $ bentoctl init
    
    Bentoctl Interactive Deployment Config Builder

    Welcome! You are now in interactive mode.

    This mode will help you set up the deployment_config.yaml file required for
    deployment. Fill out the appropriate values for the fields.

    (deployment config will be saved to: ./deployment_config.yaml)

    api_version: v1
    name: quickstart
    operator: azure-container-instances
    template: terraform
    spec:
      resource_group: testbentoml
      acr_name: betnomltest
      cpu: 1
      memory: 1
      bentoml_port: '3000'
        
    filename for deployment_config [deployment_config.yaml]:
    deployment config generated to: deployment_config.yaml
    ✨ generated template files.
      - ./main.tf
      - ./bentoctl.tfvars
    ```
    This will also run the `bentoctl generate` command for you and will generate the `main.tf` terraform file, which specifies the resources to be created and the `bentoctl.tfvars` file which contains the values for the variables used in the `main.tf` file.

4. Build and push docker image into container registry specified.

    ```bash
    bentoctl build -b iris_classifier:latest -f deployment_config.yaml
    ```
    The iris-classifier service is now built and pushed into the container registry and the required terraform files have been created. Now we can use terraform to perform the deployment.
    
5. Apply Deployment with Terraform

   1. Initialize terraform project. This installs the Azure provider and sets up the terraform folders.
        ```bash
        terraform init
        ```

   2. Apply terraform project to create Azure Container Instances deployment

        ```bash
        terraform apply -var-file=bentoctl.tfvars -auto-approve
        ```

6. Test deployed endpoint

    The `iris_classifier` uses the `/classify` endpoint for receiving requests so the full URL for the classifier will be in the form `{EndpointUrl}/classify`.

    ```bash
    URL=$(terraform output -json | jq -r .ip_address.value)/classify
    curl -i \
      --header "Content-Type: application/json" \
      --request POST \
      --data '[5.1, 3.5, 1.4, 0.2]' \
      $URL
    ```

7. Delete deployment
    Use the `bentoctl destroy` command to remove the registry and the deployment

    ```bash
    bentoctl destroy -f deployment_config.yaml
    ```

## Configuration Options

* `resrouce_group`: Resource group into which the resources have to be created.
* `acr_name`: The name of Azure Container Registry to use to store images.
* `memory`: The memory (in GBs) you want each instance to have.
* `cpu_count`: The number of CPU cores you want for your instance.
* `bentoml_port`: The port you want the endpoint to use. By default it is 5000
