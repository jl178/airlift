## Introduction

This guide will show you how to set up AWS Secrets Manager as the connections backend for Airflow.
Use this guide in combination with `mount_aws_credentials.md` so Airflow can authenticate to Secrets Manager with your local credentials

### Files

Create a helm overrides file `helm_values.yaml` under `$HOME/.config/airlift/` with the following contents:

```yaml
config:
  secrets:
    backend: airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
```

### Start

To start the airflow service with this file, run:

```bash
airlift start -d /my/dag/path -hf $HOME/.config/airlift/helm_values.yaml
```

Now, all connections will be sourced from AWS Secrets Manager with the prefix `airflow/connections`.
