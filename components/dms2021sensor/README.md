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

# Sensor architecture

## SOLID Principles
- **Single responsibility:** The code is split to allow us to change some parts of the code without affecting others that are unrelated.
- **Open/Close:** Some parts of the code can be extended using inheritance without having to modify existing classes.
- **Liskov substitution:** The subclasses extends the code doing the same as the superclasses (i.e.: on logic/rulerunners).
- **Interface segregation:** We split the code so you don't need to use Rule interfaces if you only want to work with the Logs
- **Dependency inversion:** Class usually depends on abstractions instead of depending on concretions (i.e. if we change the database, the methods should work in the same way)

## Model-view-controller
We use MVC to split the code on these three parts:
- **Model:** The part that is responsible of working with the data. This is inside the data folder. There we have the part that stores the rules and the logs on an internal database, the configuration and the communication with the auth service to check the permissions.
- **View:** The part of the code that will interact with the client. This is inside the presentation folder.
- **Controller:** The part of the code that manages most of the logic of the sensor, such as the background thread that automatically runs the rules and logs the results, and the rule and log managers that allows the communication between the Model and the View.

## Design patterns
- **Factory method:** We use this in the resultsets package of the database, and we create there the Rule and Log objects instead of having to create them directly calling those classes.
- **Facade:** We use this on some parts of the code, such as on the presentation level, so the client only has to interact with a method and we will run code involving multiple classes and at the logic level, so running a method on the manager will interact with multiple classes on the lower levels.
- **Strategy:** We use this at the rule runners so we can work in a different way depending on the type of a rule (i.e. we have to do different things depending if we have to run a command or check if a file exists)

## Code structure
- bin/: Here we have the starting point of our program. There we instance some classes that we need to work (such as the database and the managers) and we add our REST specifications.
- dms2021sensor/: The main package.
  - data/
    - config/: Here we have our config-loaders.
    - db/: The sensor database.
      - exc/: Database related exceptions.
      - results/: The data classes we store.
      - resultsets/: Some operations of the data classes.
    - rest/: Here we have the communication with the auth service.
  - logic/: Here we have our data managers
    - rulerunners/: Here we have the background thread and the code that runs the rules on the system.
      - exc/: Exceptions that can be raised when we try to run the rules.
  - presentation/:
    - rest/: Here we have the code that receives the rest requests and generates its response

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
    - `401 Unauthorized` if the requestor does not meet the security requirements.

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
    - `401 Unauthorized` if the requestor does not meet the security requirements.
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
    - `401 Unauthorized` if the requestor does not meet the security requirements.
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
    - `401 Unauthorized` if the requestor does not meet the security requirements.
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
    - `401 Unauthorized` if the requestor does not meet the security requirements.
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
    - `401 Unauthorized` if the requestor does not meet the security requirements.