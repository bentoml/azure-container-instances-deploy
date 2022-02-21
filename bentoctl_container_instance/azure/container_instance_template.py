"""
https://docs.microsoft.com/en-us/azure/container-instances/container-instances-reference-yaml

Check the reference and make the changes to the template to add other functionalities
"""


ACI_TEMPLATE = """
name: {container_group_name}
apiVersion: '2019-12-01'
properties: # Properties of container group
  containers: # Array of container instances in the group
  - name: {aci_name} # Name of an instance
    properties: # Properties of an instance
      image: {docker_image_tag}  # Container image used to create the instance
      ports: # External-facing ports exposed on the instance, must also be set in group ipAddress property
      - protocol: TCP
        port: {port}
      environmentVariables:
      resources: # Resource requirements of the instance
        requests:
          memoryInGB: {memory}
          cpu: {cpu_count}
          gpu: # only if gpu is required
  restartPolicy: OnFailure
  imageRegistryCredentials: # Credentials to pull a private image
  - server: {acr_name}.azurecr.io
    username: {docker_username}
    password: '{docker_password}'
  ipAddress: # IP address configuration of container group
    ports:
    - protocol: TCP
      port: {port}
    type: Public
    dnsNameLabel: {dns_name}
  osType: Linux
  sku: {acr_sku} # SKU for the container group
"""
