## Introduction

This guide will show you how to start airlift using Airflow version `2.5.1` on an ARM machine. Depending on what `requirements.txt` you have, Airflow version `2.5.1` can have some packaging issues (due to `gcc` not being available for use) in the base Docker image. This can require some patching for ARM machines.

### Start

To begin, create a Dockerfile with the following content:

```yaml
FROM apache/airflow:2.5.1-python3.10
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
          build-essential libleveldb-dev libopenmpi-dev openssh-server openssh-client libsasl2-dev
USER airflow
# DBT Shared repo Authentication 
ARG GIT_USER
ARG GIT_PW
USER root
ENV DBT_VENV_PATH="/usr/dbt_venv"
ENV PIP_USER=false
RUN apt-get update \
    && apt-get install -y  python3-venv && apt-get install -y git
RUN python3 -m venv "${DBT_VENV_PATH}"
RUN ${DBT_VENV_PATH}/bin/pip install dbt-snowflake
ENV PIP_USER=true
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

#### GIT_USER  
From Github home page as shown below

<img width="708" alt="Screenshot 2024-07-23 at 12 46 39 PM" src="https://github.com/user-attachments/assets/115a4259-1d06-4ee1-b2ec-ca27ecaf669d">

#### GIT_PW ### 
Github PAT (Personal Access Token) , [Generate PAT from Github](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic:~:text=your%20organization.%22-,Creating%20a%20personal%20access%20token%20(classic),-Note%3A%20Organization%20owners/).



Finally, start the `airlift` service with the new image:

```bash
airlift start -d /my/dag/path --image airflow-arm:2.5.1
```

Now, the base image for Airflow will be 2.5.1 and should run smoothly on an ARM machine (Like the M1/M2 Mac)
