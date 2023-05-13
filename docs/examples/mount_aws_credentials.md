## Introduction

This guide will show you how to mount AWS credentials Airflow. This is helpful when you need to have your Airflow DAGs authenticate & use AWS services.

### Start

Your AWS credentials file should be located at: `$HOME/.aws/`. To mount it & start the Airflow service, run:

#### CLI

```bash
airlift start -d /my/dag/path -m hostPath=$HOME/.aws/,containerPath=/home/airflow/.aws/,name=aws 
```

With this command, it will mount your local path `$HOME/.aws/` to the Airflow container under path `/home/airflow/.aws/`.

#### Config File

If you prefer to use a config file instead of saving this command, you can create a `config.yaml` file under `$HOME/.config/airlift/config.yaml` with the following contents:

```yaml
dag_path: /my/dag/path
extra_volume_mounts:
  - hostPath=$HOME/.aws/,containerPath=/home/airflow/.aws/,name=aws 
```

Then, run the CLI with:

```bash
airlift start -c $HOME/.config/airlift/config.yaml
```
