## Introduction

This guide will show you how to start airlift using Airflow version with `2.5.1` on an ARM machine. This image also has the authentication to github which is a pre-requisite to run the DBT models using cosmos with depeendecy on the shared repo. Depending on what `requirements.txt` you have, Airflow version `2.5.1` can have some packaging issues (due to `gcc` not being available for use) in the base Docker image. This can require some patching for ARM machines.

### Start

To begin, create a Dockerfile with the following content:

```yaml
FROM apache/airflow:2.5.1-python3.10
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
          build-essential libleveldb-dev libopenmpi-dev openssh-server openssh-client libsasl2-dev git gettext-base
# DBT Shared repo Authentication
ARG GIT_USER
ARG GIT_PW
ENV DBT_VENV_PATH="/usr/local/airflow/dbt_venv"
ENV PIP_USER=false
RUN python3 -m venv "${DBT_VENV_PATH}"
RUN ${DBT_VENV_PATH}/bin/pip install dbt-snowflake==1.6.4
ENV PIP_USER=true
USER airflow
RUN source ${DBT_VENV_PATH}/bin/activate && \
    git config --global credential.helper store && \
    ( [ -n "${GIT_USER:-}" ] && [ -n "${GIT_PW:-}" ] && \
      echo "https://${GIT_USER:-}:${GIT_PW:-}@git.zoominfo.com" >> ~/.git-credentials || \
      echo "No GIT credentials provided" )
```

Next, build the docker image:

```bash
docker build ./ --build-arg GIT_USER=giridhar-vemula --build-arg GIT_PW=ghp_XXXXXXXXXX -t airflow-arm:2.5.1
```
Get the credentials as below.

#### GIT_PW ### 
Github PAT (Personal Access Token) , [Generate PAT from Github](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic:~:text=your%20organization.%22-,Creating%20a%20personal%20access%20token%20(classic),-Note%3A%20Organization%20owners/).
Select repo and read:org scopes while creating the Personal Access Token.


Now, the base image for Airflow will be 2.5.1 and should run smoothly on an ARM machine (Like the M1/M2 Mac)
