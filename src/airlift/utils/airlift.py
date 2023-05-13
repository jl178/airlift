import yaml
from airlift.utils.file import FileUtils


class AirliftUtils:
    @staticmethod
    def create_config_file(
        default_file_path: str, override_file_path: str, final_file_path: str
    ):
        """
        Merges two YAML files and dumps the results to a separate location.
        Args:
            default_file_path: The first YAML file path
            override_file_path: The second YAML file path
            final_file_path: The final file path for the merged YAML
        """
        final_data = FileUtils.merge_yaml(
            original_data=default_file_path, override_data=override_file_path
        )
        with open(final_file_path, "w+") as file:
            yaml.dump(final_data, file, default_flow_style=False, sort_keys=False)
