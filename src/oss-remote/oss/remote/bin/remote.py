from pydantic import BaseModel, Field
from typing import Optional
from oss.core.argumentparser import ArgumentParser
from oss.remote.app import RemoteApp
from oss.remote.remotes.type import RemoteType


class LaunchArguments(BaseModel):
    model_config = {
        "extra": "ignore",  # Prevent unwanted extra fields from being added to this class
    }

    worker_config: Optional[str] = Field(
        examples=[],
        description="Filepath to the .env worker configuration file",
    )

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


# The default entrypoint for this application
def cli() -> None:
    # Retrieve the launch arguments for this application
    launch_arguments: LaunchArguments = ArgumentParser.parse_arguments(launch_argument_model=LaunchArguments)
    if not launch_arguments.remote_type:
        exit(1)

    # Get the remote type from the launch arguments. Then start the app passing the remote type
    remote_type: RemoteType = RemoteType[str(launch_arguments.remote_type).upper()]  # type: ignore
    remote_app: RemoteApp = RemoteApp(remote=remote_type)
    remote_app.run()


# The app was not started via the CLI-entrypoint
# Call the CLI function so we have a consistent way of starting the application
if __name__ == "__main__":
    cli()
