**This code is in a closed beta state. There may be bugs and major changes before a full release.
Please provide feedback and bugs in the [issues](https://github.com/BC-SECURITY/Empire-Cli/issues) or in our Discord**

Empire-Cli
=============================
The new Empire Cli is a a python command-line application written using [python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit).
It provides many enhancements over the cli built into the server including:
* Support for multiple users at a time
* Custom agent shortcuts
* Enhanced autocomplete
* An interactive agent shell

- [Install and Run](#install-and-run)
- [Configuration](#configuration)
- [Usage](#usage)
	- [Main Menu](#main-menu)
	- [Admin Menu](#admin-menu)
	- [Listener Menu](#listener-menu)
	- [Use Listener Menu](#use-listener-menu)
	- [Stager Menu](#stager-menu)
	- [Use Stager Menu](#use-stager-menu)
	- [Plugin Menu](#plugin-menu)
	- [Use Plugin Menu](#use-plugin-menu)

----------------------------------

##  Install and Run
We recommend the use of [Poetry](https://python-poetry.org/docs/) for installing and running the cli.
In the future, it will most likely be packaged in the main Empire repository.
```shell script
poetry install
poetry run python main.py
```

## Configuration
The Empire-CLI configuration is managed via [config.yaml](./config.yaml).

- servers - The servers block is meant to give the user the ability to set up frequently used Empire servers.
If a server is listed in this block then when connecting to the server they need only type, for example: `connect -c localhost`.
This tells Empire-Cli to use the connection info for the server named localhost from the yaml.
```yaml
servers:
  localhost:
    host: https://localhost
    port: 1337
    socketport: 5000
    username: empireadmin
    password: password123
```
- suppress-self-cert-warning - Suppress the http warnings of connecting to a server that uses a self-signed cert
- shortcuts - Shortcuts defined here allow the user to define their own frequently used modules and assign a command to them.
Let's look at 3 distinct examples. All of which can be found in the default [config.yaml](./config.yaml)
```yaml
shortcuts:
  powershell:
    sherlock:
      module: powershell/privesc/sherlock
```
This first example is the simplest example. It adds a `sherlock` command to the interact menu for Powershell agents. It does not pass any specific parameters.

```yaml
shortcuts:
  powershell:
    keylog:
      module: powershell/collection/keylogger
      params:
        - name: Sleep
          value: 1
```
This next one is slightly more complex in that we are telling the shortcut to set the Sleep parameter to 1.
Note that if there are any other parameters for this module that we don't define, it will use whatever the default value is.

```yaml
    steal_token:
      module: powershell/credentials/tokens
      params:
        - name: ImpersonateUser
          value: true
        - name: ProcessID
          dynamic: true
```
This third one gets a bit more complex. Instead of providing a `value` to the parameter, it is marked as `dynamic`.
This tells the CLI that it expects the user to send the parameters. In other words the user needs to type `steal_token HUBBL3 65120` in order for this to execute.
The parameters are passed in the order they are defined in config.yaml. There are some convenient autofills if the field is named `Listener` or `Agent`.

### Usage

#### Main Menu

#### Admin Menu

#### Listener Menu

#### Use Listener Menu

#### Stager Menu

#### Use Stager Menu

#### Plugin Menu

#### Use Plugin Menu

#### Agent Menu

#### Interact Menu

#### Shell Menu

#### Credential Menu

#### Use Module Menu
