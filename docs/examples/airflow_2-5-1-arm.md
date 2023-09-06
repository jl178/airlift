## Introduction

This guide will show you how to start airlift using Airflow version `2.5.1` on an ARM machine. Airflow version `2.5.1` has some packaging issues in the base Docker image,
which requires some patching for ARM machines.

### Start

To begin, create a Dockerfile with the following content:

```yaml
FROM apache/airflow:2.5.1-python3.10
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
          build-essential libleveldb-dev libopenmpi-dev openssh-server openssh-client libsasl2-dev
USER airflow
```

Next, build the docker image:

```bash
docker build ./ -t airflow-arm:2.5.1
```

Finally, start the `airlift` service with the new image:

```bash
airlift start -d /my/dag/path --image airflow-arm:2.5.1
```

Now, the base image for Airflow will be 2.5.1 and should run smoothly on an ARM machine (Like the M1/M2 Mac)
