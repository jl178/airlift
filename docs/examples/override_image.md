## Introduction

This guide will show you how to override the default Airflow image used when running the `start` command.

### Start

To start the airflow service with a different image, run:

```bash
airlift start -d /my/dag/path --image apache/airflow:2.4.0
```

Now, the base image for Airflow will be 2.4.0.

***NOTE: Be careful when changing the image and using `requirements.txt` files. Incorrectly specified requirements could cause the Airflow version to downgrade unexpectedly.***
