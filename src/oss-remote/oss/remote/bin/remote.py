"""Launcher with argument parsing for a remote worker"""

from typing import Optional

from oss.core.bin.argumentparser import ArgumentParser
from oss.core.log import Log
from oss.remote.app import RemoteApp
from oss.remote.remotes.type import RemoteType
from pydantic import BaseModel, Field, ValidationError, field_validator

# Activate module wide logging
logger = Log.get_logger_function()(__name__)


class LaunchArguments(BaseModel):
    """
    Represents the arguments necessary for launching a remote worker.

    This class encapsulates all the configurations required to set up the worker,
    including paths to configuration files and broker details.

    Attributes:
        worker_config (Optional[str]): Filepath to the .env worker configuration file.
        broker_host (str): Hostname, FQDN or IP address of the message broker.
        broker_port (int): Port number of the message broker.
        remote_type (str): The type of remote this worker needs to handle.
    """

    model_config = {
        "extra": "ignore",  # Prevent unwanted extra fields from being added to this class
    }

    worker_config: Optional[str] = Field(
        examples=[],
        description="Filepath to the .env worker configuration file",
        default=None,
    )

    broker_host: str = Field(
        examples=["localhost", "127.0.0.1", "broker.example"],
        description="Hostname, FQDN or IP address of the message broker",
        default="localhost",
    )

    broker_port: int = Field(
        examples=[5671, 5672],
        description="Port number of the message broker",
        default=5672,
    )

    remote_type: str = Field(
        examples=["keypad", "buttonpad"],
        description="The type of remote this worker needs to handle",
    )

    @field_validator("worker_config")
    @classmethod
    def validate_worker_config(cls, worker_config: str) -> str:
        """
        Validates the worker configuration string ensuring it is a non-empty .env file.

        Args:
            worker_config (str): The configuration string for the worker.
        Returns:
            str: The validated worker configuration string.
        Raises:
            ValueError: If the worker_config is empty.
            ValueError: If the worker_config does not end with ".env".
        """
        if worker_config == "":
            raise ValueError("Worker config cannot be empty")
        if not worker_config.endswith(".env"):
            raise ValueError("Worker config must be a .env file")
        return worker_config

    @field_validator("broker_host")
    @classmethod
    def validate_broker_host(cls, broker_host: str) -> str:
        """
        Validates the 'broker_host' field, ensuring it is not an empty string.

        Args:
            broker_host (str): The host address of the broker which must be a non-empty string.
        Returns:
            str: The validated 'broker_host' string.
        Raises:
            ValueError: If 'broker_host' is an empty string.
        """
        if broker_host == "":
            raise ValueError("Broker host cannot be empty")
        return broker_host

    @field_validator("broker_port")
    @classmethod
    def validate_broker_port(cls, broker_port: int) -> int:
        """
        Validates the 'broker_port' field to ensure it falls within the acceptable range of port numbers.

        Args:
            broker_port (int): The port number to be validated. Must be between 1 and 65535.
        Returns:
            int: The validated port number.
        Raises:
            ValueError: If the provided port number is not between 1 and 65535.
        """
        if broker_port < 1 or broker_port > 65535:
            raise ValueError("Broker port must be between 1 and 65535")
        return broker_port

    @field_validator("remote_type")
    @classmethod
    def supported_remote_types(cls, remote_type: str) -> str:
        """
        Validates the 'remote_type' field to ensure its value is in the RemoteType enum.
        Args:
            remote_type (str): The type of the remote being validated.
        Returns:
            str: The validated remote_type.
        Raises:
            ValueError: If the provided remote_type is unsupported.
        """
        try:
            if not RemoteType[remote_type.upper()]:
                raise ValueError(f"Unsupported remote_type '{remote_type}'")
        except KeyError:
            raise ValueError(f"Unsupported remote_type '{remote_type}'")
        return remote_type


# The default entrypoint for this application
def cli() -> None:
    """
    Entrypoint for the application. Parses the launch arguments, initializes the RemoteApp with the appropriate
    RemoteType, and starts the application.

    Raises:
        ValidationError: If the launch arguments fail validation.
    Args:
    Returns:
        None
    """
    try:
        # Retrieve the launch arguments for this application
        launch_arguments: LaunchArguments = ArgumentParser.parse_arguments(launch_argument_model=LaunchArguments)

        # Get the remote type from the launch arguments. Then start the app passing the remote type
        remote_type: RemoteType = RemoteType[str(launch_arguments.remote_type).upper()]  # type: ignore
        remote_app: RemoteApp = RemoteApp(remote=remote_type)
        remote_app.run()
    except ValidationError:
        logger.critical("There was an error while validating the launch arguments.")


# The app was not started via the CLI-entrypoint
# Call the CLI function so we have a consistent way of starting the application
if __name__ == "__main__":
    cli()
