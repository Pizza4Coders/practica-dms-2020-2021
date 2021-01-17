# DMS 2020-2021 Client application

This application serves as the control console for the different services of the appliance.

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

`dms2021client` package contains a program, which shows a different main menu depends on the rights a user has, which allows to:

  - `Create users`: Allows to create users and add them to the authentication service. This option will be only available, if the user has the right `AdminUsers`.

  - `Modify rights`: Allows to modify the rights of a user of the authentication service. This option will be only available, if the user has the right `AdminRights`.

  - `Manage sensors`: Allows to choose a sensor of the sensor service. This option will be only available, if the user has the rights `AdminSensors`. In this option, a user can do this actions:
    - `Modify rules of a sensor`: Allows to create, delete or execute a new rule. Also, it's possible to view all the rules that a sensor has. This option will be only available, if the user has the right `AdminRules`.
    - `Get monitoring values of a sensor`: Allows to get the latest monitoring values of a sensor. This option will be only available, if the user has the right `ViewReports`.

  - `Log out`: Allows to log out of the application.

It's also possible to`go back` in every window. If the window is the main menu, the application ends.

# Client architecture

## SOLID Principles
- **Single responsibility:** The code is divided in different packages and classes trying to ensure that each one is responsible of one functionality.
- **Open/Close:** The menus are designed in a way that each one extends from the `OrderedMenu` without modifying his behavior.
- **Liskov substitution:** The subclasses extend the base class functionality, but didn't replace his base behavior.
- **Interface segregation:** The `OrderedMenu` abstract class has the some methods common to all the menus without forcing subclasses implementing methods they wouldn't use.
- **Dependency inversion:** The concretions depends on the abstraction `OrderedMenu`, by this way created new menus is very easy.

## Model-view-controller
We use MVC to split the code on these three parts:
- **Model:** The part that is responsible of working with the data. This is inside the data folder. There, we have the part that stores the configuration and the communication with the authentication service and sensor service.
- **View:** The part of the code that will interact with the user. This is inside the presentation folder.
- **Controller:** The part of the code that manages the logic of the client with a manager class which allows the communication between the Model and the View.

## Design patterns
- **Template Method:** The menus are coded in a way the `OrderedMenu` is the abstract class used for creating menus and finally each menu extends `OrderedMenu` overriding some methods. Here, occurs an inversion of the normal order of calls in the inheritance because the `OrderedMenu` class calls implemented methods of subclasses.

## Code structure
- bin/: Here we have the starting point of our program.
- dms2021client/: The main package.
  - data/
    - config/: Gets the neccessary information to make contact with the authentication and sensor service.
    - rest/: Here we have the communication with the auth service and the sensor service.
        - exc/: Exceptions used in the two next classes. We have this exceptions: BadRequestError, ConflictError, InvalidCredentialsError, NotFoundError, UnauthorizedError)
        - AuthService: Communication with the authentication service.
        - SensorsService: Communication with the sensor service.
  - logic/: Here we have the manager.
    - ClientManager: Gets the configuration data of the client and allows to log in. Also, calls some methods of MainMenu class of the presentation package.
  - presentation/:
      - OrderedMenu: It's an (`Abstract Class`) with the base structure of a menu.
    This folders contains the classes which defines all the menus (`Concrete Classes`)
      - MainMenu: Shows the main menu (the options will be different depends on the rights a user has). It has a method to create the user.
      - sensor_menus/:
          - RulesMenu: Defines the menu (depends on the rights) for modifying rules or viewing reports.
          - SensorsMenu: Defines the menu for choosing a sensor.
          - AddRulesMenu: Defines a menu with the type of a rule to add.
      - user_menus/:
          - ModifyRightsMenu: Defines a menu for adding or deleting rights to a user.
          - GrantRevokeMenu: Defines a menu with the rights of a user has or not depends on the action selected: grant or revoke.
    



