# DMS 2020-2021 Sensor Service

This service provides sensing functionalities to the appliance.

## Installation

Run `./install.sh` for an automated installation.

To manually install the service:

```bash
# Install the service itself.
./setup.py install
```

## Configuration

Configuration will be loaded from the default user configuration directory, subpath `dms2021sensor/config.yml`. This path is thus usually `${HOME}/.config/dms2021sensor/config.yml` in most Linux distros.

The configuration file is a YAML dictionary with the following configurable parameters:

- `db_connection_string` (mandatory): The string used by the ORM to connect to the database.
- `host` (mandatory): The service host.
- `port` (mandatory): The service port.
- `debug`: If set to true, the service will run in debug mode.
- `salt`: A configurable string used to further randomize the password hashing. If changed, existing user passwords will be lost.
- `auth_service`: A dictionary with the configuration needed to connect to the authentication service.
  - `host` and `port`: Host and port used to connect to the service.

## Running the service

Just run `dms2021sensor` as any other program.

## REST API specification

This service exposes a REST API so other services/applications can interact with it.

- `/` [`GET`]

  Status verification
  - Returns:
    - `200 OK` if the service is running.

- `/rules/` [`GET`]

  Gets all configured rules.
  - Security:
    - The requestor must have the `AdminRules` permission.
  - Parameters:
    - `username` [form data] (`str`): The requestor's user name.
  - Returns:
    - `200 OK`. The response content (`application/json`) is a JSON dictionary containing a list of rules with the following data on each element:
      - `rule_name`: The name of the rule
      - `type`: Type of rule. This can be `command` if it runs a command or `file` if it checks for the presence of a file.
      - `data`: If `type` was `command`, the command that runs, or if it was `file`, the path to the file that is checked.
      - `frequency`: Time in seconds between each automatic run of the rule. 0 if the rule does not run automatically.

- `/rule/<rule_name>/` [`GET`]

  Gets info about a rule.
  - Security:
    - The requestor must have the `AdminRules` permission.
  - Parameters:
    - `username` [form data] (`str`): The requestor's user name.
    - `rule_name`: [path] (`str`): The name of the rule.
  - Returns:
    - `200 OK` if the rule exists. The response content is a JSON dictionary with the data in the above response.
    - `400 Bad Request` if the request is malformed (e.g., no rule_name was sent)
    - `404 Not found` if the rule does not exist.
  
- `/rule/` [`POST`]

  Creates a new rule.
  - Security:
    - The requestor must have the `AdminRules` permission.
  - Parameters:
    - `username` [form data] (`str`): The requestor's user name.
    - `rule_name`: [form data] (`str`): The name of the rule
    - `type`: [form data] (`str`): Type of rule. This can be `command` if it runs a command or `file` if it checks for the presence of a file.
    - `data`: [form data] (`str`) If `type` was `command`, the command that runs, or if it was `file`, the path to the file that is checked.
    - `frequency`: [form data] (`int`) Time in seconds between each automatic run of the rule. 0 if the rule does not run automatically.
  - Returns:
    - `200 OK` if the rule was created sucessfully.
    - `400 Bad Request` if the request is malformed.
    - `409 Conflict` if another rule exists with the same name.

- `/rule/<rule_name>/` [`DELETE`]

  Deletes an existing rule.
  - Security:
    - The requestor must have the `AdminRules` permission.
  - Parameters:
    - `username` [form data] (`str`): The requestor's user name.
    - `rule_name` [path] (`str`): The rule name.
  - Returns:
    - `200 OK` if the rule was deleted.
    - `400 Bad Request` if the request is malformed.
    - `404 Not found` if the rule does not exist.

- `/rule/<rule_name>/run/` [`GET`]

  Runs a rule and returns its value.
  - Security:
    - The requestor must have the `AdminRules` and `ViewReports` permissions.
  - Parameters:
    - `username` [form data] (`str`): The requestor's user name.
    - `rule_name` [path] (`str`): The rule name.
  - Returns:
    - `200 OK` if the rule is sucessfully run. The response content is a JSON dictionary containing:
      - `result`: the value that was returned. This will be always an string.
    - `400 Bad Request` if the request is malformed.
    - `404 Not found` if the rule does not exist.
    - `500 Internal Server error` if the rule failed to run.
  
- `/log/` [`GET`]

  Returns the history of rule executions.
  - Security:
    - The requestor must have the `ViewReports` permission.
  - Parameters:
    - `username` [form data] (`str`): The requestor's user name.
  - Returns:
    - `200 OK`. The response content is a dictionary containing a list with the following data on each element:
      - `rule_name`: The name of the rule.
      - `time`: The time of the result.
      - `result`: The result of the rule.