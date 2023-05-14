# Frequently Asked Questions

**Table of Contents**

- [Question 1](#q1)
- [Question 2](#q2)
- [Question 3](#q3)
- [Question 4](#q4)
- [Question 5](#q5)

---

## Q1: How can I change an Airflow config value?

<a id='q1'></a>
Answer: Use the `--helm_values_file` flag when starting the service. This flag takes in an ABSOLUTE file path to a yaml file. This yaml file contains Helm chart overrides.
For example, if you want to change the executor type for Airflow:

```yaml
executor: KubernetesExecutor
```

See [this link](https://artifacthub.io/packages/helm/apache-airflow/airflow?modal=values) for all possible configuration options.

[Back to top](#frequently-asked-questions)

---

## Q2: I specified Airflow image `apache/airflow:2.X.X` but I see `2.Y.Y` in the UI. Why?

<a id='q2'></a>
Answer: Make sure you properly constrain your `requirements.txt` file to the appropriate package version for your Airflow installation.
If your package versions are incorrect, it can inadvertently downgrade your Airflow installation. For example, see [this link](https://github.com/apache/airflow/tree/constraints-2-2-2-fixed) for the Airflow 2.2.2 constraints file.

[Back to top](#frequently-asked-questions)

---

## Q3: Where are the tests for this repo?

<a id='q3'></a>
Answer: I haven't written them yet :)

[Back to top](#frequently-asked-questions)

---

## Q4: Does this support ARM machines (E.G. the Mac M1/M2 chipset)?  

<a id='q4'></a>
Answer: Yes, please pick a base image which supports ARM when starting the service.
You can do this by using the `--image` flag when starting the service. EX:

```bash
airlift start -d /my/dag/path --image apache/airflow:2.4.0
```

If you are using Airflow 2.2.2, I have built a custom image which supports *some* packages. Your mileage will vary depending on what PyPi packages you use.
To use this custom image, pass `--image jeredlittle/airflow:2.2.2-arm`

See [this link](https://hub.docker.com/r/apache/airflow/tags) for supported ARM images for Airflow. Note: ARM support for Airflow Docker images started in `2.3.0`

[Back to top](#frequently-asked-questions)

---

## Q5: Why did you build this CLI tool?

<a id='q5'></a>
Answer: I couldn't find a simple, yet flexible CLI tool for Airflow which met my local development needs. I wanted to be able to easily switch between Airflow releases & customize all configuration values
using a config file

[Back to top](#frequently-asked-questions)
