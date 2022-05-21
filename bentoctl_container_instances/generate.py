# from bentoctl.utils.operator_helpers.generate import Generate, TERRAFORM_VALUES_FILE_NAME
# from bentoctl.utils.operator_helpers.values import DeploymentValues
#
# class AzDeploymentValues(DeploymentValues):
#     @staticmethod
#     def parse_image_tag(image_tag: str):
#         registry_url, project_id, tag = image_tag.split("/")
#         repository, version = tag.split(":")
#
#         return registry_url, repository, version
# class AzGenerate(Generate):
#     @staticmethod
#     def generate_terraform_values(name: str, spec: dict, destination_dir: str):
#
#         params = DeploymentValues(name, spec, "terraform")
#         values_file = os.path.join(destination_dir, TERRAFORM_VALUES_FILE_NAME)
#         params.to_params_file(values_file)
#
#         return values_file
#
