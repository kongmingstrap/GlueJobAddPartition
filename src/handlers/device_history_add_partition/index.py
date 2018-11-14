import boto3

from device_history_add_partition import DeviceHistoryAddPartition

athena = boto3.client('athena')


def handler(event, context):
    DeviceHistoryAddPartition(event, context, athena).main()
