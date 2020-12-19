# DMS 2020-2021 Client application

This applicationserves as the control console for the different services of the appliance.

## Installation

Run `./install.sh` for an automated installation.

To manually install the service:

```bash
# Install the service itself.
./setup.py install
```

## Configuration

Configuration will be loaded from the default user configuration directory, subpath `dms2021client/config.yml`. This path is thus usually `${HOME}/.config/dms2021client/config.yml` in most Linux distros.

The configuration file is a YAML dictionary with the following configurable parameters:

- `debug`: If set to true, the service will run in debug mode.
- `auth_service`: A dictionary with the configuration needed to connect to the authentication service.
  - `host` and `port`: Host and port used to connect to the service.
- `sensors`: A dictionary with the configuration needed to connect to the different sensor services. Each key identifies a sensor, and their values are themselves dictionaries with the connection information:
  - `host` and `port`: Host and port used to connect to the service.

## Running the service

Just run `dms2021client` as any other program.

## Description

`dms2021client` package contains a programme, which shows a different main menu depends on the rights a user has, which allows to:
    - `Create users`: Allows to create users and add them to the authentication service. This option will be only available, if the user (the future user creator) has the right `AdminUsers`.
    - `Modify rights`: Allows to modify the rights of a user of the authentication service. This option will be only available, if the user (the future modifier) has the right `AdminRights`.
    - `Manage sensors`: Allows to choose a sensor of the sensor service. This option will be only available, if the user (the future manager) has the rights `AdminSensors`, `AdminRules` or `ViewReports`. (We planned to do that because the `AdminSensors` at this moment can only choose what sensor wants). In this option, a user can do this actions:
        - `Modify rules of a sensor`: Allows to create, delete or execute a new rule. Also, it's possible to view all the rules that a sensor has. This option will be only available, if the user has the right `AdminRules`.
        - `Get monitoring values of a sensor`: Allows to get the latest monitoring values of a sensor. This option will be only available, if the user has the right `ViewReports`.
    - `Log out`: Allows to log out of the application.
It's also possible to`go back` in every window. If the window is the main menu, the application ends.

## Architecture



