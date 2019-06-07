from dataclasses import dataclass


@dataclass
class AuthoringClient:
    "Details about the client used to create/edit a project."
    name: str
    platform: str
    version: str
