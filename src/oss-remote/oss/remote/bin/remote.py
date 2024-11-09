import argparse
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional
from oss.remote.app import RemoteApp


class LaunchArguments(BaseModel):
    model_config = {
        "extra": "ignore",  # Prevent unwanted extra fields from being added to this class
    }

    broker_host: Optional[str] = Field(
        examples=["localhost", "127.0.0.1", "broker.example"],
        description="Hostname, FQDN or IP address of the message broker",
        default="localhost",
    )

    broker_port: Optional[int] = Field(
        examples=[5671, 5672],
        description="Portnumber of the message broker",
        default=5672,
    )

    remote_type: Optional[str] = Field(
        examples=["keypad", "buttonpad"],
        description="The type of remote this worker needs to handle",
    )


class ArgumentParser:
    @staticmethod
    def load_dotenv_files() -> None:
        # First load the supplied .env file. This way any "default" or packaged env variables can being overwritten.
        # every argument can be loaded via the environment variables
        load_dotenv()

    @staticmethod
    def parse_environment_variables() -> LaunchArguments:
        pass

    @staticmethod
    def parse_commandline_arguments() -> LaunchArguments:
        argument_parser: argparse.ArgumentParser = argparse.ArgumentParser()
        argument_parser.prog = "oss_worker"
        argument_parser.version = "v1.0"

        for field_name, field_metadata in LaunchArguments.model_fields.items():
            argument_name = f"--{field_name}"  # Use --field_name format
            default = field_metadata.default if field_metadata.default is not None else argparse.SUPPRESS
            field_type = [
                variable_type for variable_type in field_metadata.annotation.__args__ if variable_type is not type(None)
            ][0]

            help_text = field_metadata.description or ""

            # Add argument based on field type and constraints
            if field_type == bool:  # Boolean needs to be handled differently
                argument_parser.add_argument(argument_name, action="store_true", help=help_text)
            else:
                argument_parser.add_argument(argument_name, type=field_type, default=default, help=help_text)

        argument_parser.parse_args()

    @staticmethod
    def parse_arguments() -> LaunchArguments:
        # Load the dotenv files to overwrite default environment variables
        ArgumentParser.load_dotenv_files()

        # Parse the environment variables
        ArgumentParser.parse_environment_variables()

        # Parse commandline arguments to overwrite environment variables
        ArgumentParser.parse_commandline_arguments()


# The default entrypoint for this application
def cli():
    launch_arguments: LaunchArguments = ArgumentParser.parse_arguments()
    remote_app: RemoteApp = RemoteApp(remote=launch_arguments.remote_type)


# The app was not started via the CLI-entrypoint
if __name__ == "__main__":
    cli()
