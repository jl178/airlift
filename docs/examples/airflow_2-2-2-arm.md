## Introduction

This guide will show you how to start airlift using Airflow version `2.2.2` on an ARM machine.

### Start

To begin, copy this Dockerfile to the location containing your `requirements.txt` file:

```yaml
FROM apache/airflow:2.3.2
RUN pip uninstall apache-airflow -y
USER root
RUN apt update
RUN apt install default-libmysqlclient-dev -y
RUN apt install gcc -y
RUN apt install g++ -y
RUN apt install pkg-config -y
RUN apt install libleveldb-dev -y
USER airflow
RUN pip install apache-airflow==2.2.2
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN pip uninstall -y protobuf
RUN pip install protobuf==3.20.1
```

***NOTE: Make sure your `requirements.txt` file follows the constraints noted here: <https://github.com/apache/airflow/tree/constraints-2-2-2-fixed>***

Next, build the docker image:

```bash
docker build ./ -t airflow-arm:2.2.2
```

Finally, start the `airlift` service with the new image:

```bash
airlift start -d /my/dag/path --image airflow-arm:2.2.2 
```

***NOTE: Do not pass in the `requirements.txt` file again. It could cause unexpected issues by upgrading/downgrading packages we overrode during our `docker build` step.***

Now, the base image for Airflow will be 2.2.2 and should run smoothly on an ARM machine (Like the M1/M2 Mac)
