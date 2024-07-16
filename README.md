# parat

## ./run

The `./run` script contains several useful commands to manage this project. For instance, you can use it to format your source code or run the linter by executing `./run format` or `./run lint` respectively.

Most of the functionality of the `./run` script is only available when the application container is running.

## Visual Studio Code

### Setting Up Python

Until the venv of the container can be used within Virtual Studio Code, the first thing you need to do is to setup your Python environment by executing "Show All Commands" (Ctrl+Shift+p by default) and select "Python: Select Interpreter".

### Configuration

The configuration for Visual Studio Code resides in `.vscode/settings.json`, please make sure to understand Virtual Studio Code's [settings precedence](https://code.visualstudio.com/docs/getstarted/settings#_settings-precedence).

### Extensions

#### General Information

parat provides a bunch of recommended extensions. The review and / or install them, go to the extension tab and search for `@recommended` and check out the collapsible `Workspace Recommendation` accordion.

#### djlint

djLint is configured as the default Jinja formatter and linter. Make sure to install the `monosans.djlint` extension from the list of `@recommended` extensions. In addition, you need to make sure to configure `"djlint.pythonPath"`. This extension functions independently from the run script.

#### Black

Black is configured as the default formatter. Make sure to install the `ms-python.black-formatter` extension from the list of `@recommended` extensions. This extension functions independently from the run script. 

#### Flake8

Flake8 is configured as the default linter. Make sure to install the `ms-python.flake8` extension from the list of `@recommended` extensions. This extension functions independently from the run script.
## Wagtail

When Wagtail was selected during setup, the following extensions are enabled by default and must be configured accordingly.

### wagtail-transfer

Per default, staging and production instances are linked and `WAGTAILTRANSFER_SECRET_KEY` and `WAGTAILTRANSFER_STAGE_KEY` must be set for both instances. `WAGTAILTRANSFER_SECRET_KEY` is the secret of
the current stage, whilst `WAGTAILTRANSFER_STAGE_KEY` is the secret key of the stage that is linked to the current stage.


## Blogging Solution - PUPUT 

### Resources

Project Page: https://github.com/APSL/puput/ and https://puput.readthedocs.io/en/latest/

### Implementation Detail

- `PUPUT_USERNAME_FIELD` and `PUPUT_USERNAME_REGEX` were overridden since Wagtail has routing issues when there are "." in URLs. (see: https://github.com/APSL/puput/issues/198, https://github.com/APSL/puput/issues/122 and https://github.com/wagtail/wagtail/issues/3653)
- Original Puput templates were copied to `./parat/templates/puput`. The blog and all its elements can be styled and adjusted by changing the templates. They also serve as a starting point understand templating capabilities of puput.
