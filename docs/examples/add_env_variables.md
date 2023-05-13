## Introduction

This guide will show you how to mount environment variables to Airflow. This is helpful when you don't use a cloud secret backend and instead manager your credentials in the UI/via env variables.

### Start

This guide will create the `foo` and `bar` connections in Airflow using Helm overrides. These connections are mounted automatically to the Airflow service during the `start` command.

#### Config File

Create a helm overrides file `helm_values.yaml` under `$HOME/.config/airlift/` with the following contents:

```yaml
env:
  - name: "AIRFLOW_CONN_FOO"
    value: "MY_SECRET_VALUE"
  - name: "AIRFLOW_CONN_BAR"
    value: "MY_SECOND_SECRET_VALUE"
```

Then, run the CLI with:

```bash
airlift start -hf $HOME/.config/airlift/helm_values.yaml -d /my/path/to/dags
```

***NOTE: You are storing credentials in plain text locally when you use this method. It is instead recommended to use a backend secret manager to manage your secrets for Airflow.***
