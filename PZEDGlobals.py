from enum import Enum


class WantDeprecated(Enum):
    NONE = 0  # Do not generate any documentation for deprecated objects
    ALLOW = 1  # Generate documentation for deprecated objects in addition to non-deprecated objects
    EXCLUSIVE = 2  # Only generate documentation for deprecated objects
