import datetime
import os

from pytz import timezone


class DeviceHistoryAddPartition(object):
    def __init__(self, event, context, athena):
        self.event = event
        self.context = context
        self.athena = athena

    def main(self):
        try:
            database = os.environ['ATHENA_DATABASE']
            table_name = os.environ['ATHENA_TABLENAME']
            target_bucket = os.environ['TARGET_BUCKET']
            output_location = os.environ['OUTPUT_LOCATION']

            now = datetime.datetime.now(timezone('UTC'))
            jst_now = now.astimezone(timezone('Asia/Tokyo'))
            yesterday = jst_now - datetime.timedelta(days=1)

            sql = self.make_sql(table_name, target_bucket, yesterday)

            self.athena.start_query_execution(
                QueryString=sql,
                QueryExecutionContext={
                    'Database': database
                },
                ResultConfiguration={
                    'OutputLocation': output_location
                }
            )
        except Exception as e:
            return e.message

    def make_sql(self, table_name, target_bucket, date):
        path = os.path.join(
            'year={0}'.format(date.year),
            'month={0:02}'.format(date.month),
            'day={0:02}'.format(date.day)
        )
        s3_path = os.path.join(target_bucket, path)

        sql = 'ALTER TABLE `{0}` ADD IF NOT EXISTS PARTITION (year={1},month={2:02},day={3:02})' \
              ' location \'{4}\''.format(table_name, date.year, date.month, date.day, s3_path)

        return sql
