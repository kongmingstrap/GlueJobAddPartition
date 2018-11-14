GlueJobAddPartition
=======

# Requirements

- [AWS CLI](https://aws.amazon.com/cli/)
- [Docker for Mac](https://www.docker.com/docker-mac)

## Development

- [pyenv](https://github.com/pyenv/pyenv)
- [localstack](https://github.com/localstack/localstack)

# Setting

## 1. Python

### shell

```shell
$ pyenv local 3.6
$ python -m venv .venv3
$ source .venv3/bin/activate
$ pip install pipenv
$ pipenv install
```

### fish shell

```shell
$ pyenv local 3.6
$ python -m venv .venv3
$ source .venv3/bin/activate.fish
$ pip install pipenv
$ pipenv install
```

## 2. Start localstack

```shell
$ make localstack-up
```

## 3. Stop localstack

```shell
$ make localstack-stop
```

# Deploy

## 1. Configure AWS credentials

- `~/.aws/credentials`

```bash
[sampler-development]
aws_access_key_id = <your_aws_access_key_id>
aws_secret_access_key = <your_aws_secret_access_key>
```

- `~/.aws/config`

```bash
[profile sampler-development]
region = ap-northeast-1
output = json
```

## 2. Deploy

```shell
$ make deploy
```

# Athena

## Create Table

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS `default.device-history` (
  `device_id` string,
  `timestamp` bigint,
  `diff_timestamp` bigint 
) PARTITIONED BY (
  year string,
  month string,
  day string 
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = '1'
) LOCATION '<YOUR_S3_LOCATION>'
TBLPROPERTIES ('has_encrypted_data'='false');
```
