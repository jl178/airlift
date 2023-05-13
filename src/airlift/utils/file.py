import hiyapyco
import jinja2
import yaml
import json
import os
import shutil


class FileUtils:
    @staticmethod
    def merge_yaml(
        original_data,
        override_data=None,
    ):
        """
        Merges two YAML files together and returns the data
        Args:
            original_data (): The original data file path
            override_data (): The override data file path

        Returns:

        """
        if override_data is not None:
            return json.loads(
                json.dumps(
                    hiyapyco.load(
                        [original_data, override_data], method=hiyapyco.METHOD_MERGE
                    )
                )
            )

        else:
            return original_data

    @staticmethod
    def yaml_to_dict(file_path: str) -> dict:
        """
        Converts a YAML file to a dictionary
        Args:
            file_path: The path to the YAML file

        Returns: A dictionary containing the YAML data

        """
        with open(file_path, "r") as file:
            dictionary = yaml.full_load(file)
        return dictionary if dictionary is not None else {}

    @staticmethod
    def render_jinja(file_path, **kwargs) -> str:
        """
        Renders a jinja template.
        Args:
            file_path (): The path to the template file
            **kwargs: The key value parameters to render the template with

        Returns: The string contents of the rendered template

        """
        split_path = file_path.split("/")
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("/".join(split_path[:-1]))
        )
        template = env.get_template(split_path[len(split_path) - 1])
        rendered_template = template.render(**kwargs)
        return rendered_template

    @staticmethod
    def write_file(file_path, data):
        """
        Writes the contents of data to the file path
        Args:
            file_path (): The file path to write to
            data (): The data to write to the file
        """
        file = open(file_path, "w+")
        file.truncate()
        file.write(data)
        file.close()

    @staticmethod
    def read_file(file_path) -> str:
        """
        Reads a file and returns the contents
        Args:
            file_path (): The file path to read from

        Returns: The contents of the file

        """
        file = open(file_path, "r")
        data = file.read()
        file.close()
        return data

    @staticmethod
    def remove_file(file_path: str):
        """
        Removes a file
        Args:
            file_path: The file to remove

        Returns: None

        """
        try:
            os.remove(file_path)
        except FileNotFoundError:
            return  # File does not exist already

    @staticmethod
    def copy_file(source_path: str, target_path: str) -> None:
        """
        Copies a file
        Args:
            source_path: The source file path
            target_path: The target file path
        """
        shutil.copy(source_path, target_path)
