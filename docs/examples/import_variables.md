
## Introduction

This guide will show you how to import variables when starting the Airflow service.

### Files

To begin create a `variables.json` file:

```bash
touch $HOME/variables.json
```

Now, add your variables with the following structure:

```json
{
  "my_cool_variable": [
    "test",
    "test2"
  ],
  "my_other_cool_variable": {
    "test3": "test1",
    "test4": "test5"
  }
}
```

### Start

To start the airflow service with this file, run:

#### CLI

```bash
airlift start -d /my/dag/path -V $HOME/variables.json
```

#### Config File

If you prefer to use a config file instead of saving this command, you can create a `config.yaml` file under `$HOME/.config/airlift/config.yaml` with the following contents:

```yaml
dag_path: /my/dag/path
variables_file: /absolute/path/to/variables.json
```

Then, run the CLI with:

```bash
airlift start -c $HOME/.config/airlift/config.yaml
```
