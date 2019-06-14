from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query
from sqlalchemy.sql import Insert

from pydataapi import DataAPI


class Users(declarative_base()):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255, collation='utf8_unicode_ci'), default=None)


database: str = 'test'
resource_arn: str = 'arn:aws:rds:us-east-1:123456789012:cluster:serverless-test-1'
secret_arn: str = 'arn:aws:secretsmanager:us-east-1:123456789012:secret:serverless-test1'

with DataAPI(database=database, resource_arn=resource_arn, secret_arn=secret_arn) as data_api:

    # start transaction

    insert: Insert = Insert(Users, {'name': 'ken'})
    # INSERT INTO my_table (name) VALUES ('ken')

    result = data_api.execute(insert)
    print(result)
    # Result(generated_fields=None, number_of_records_updated=1)

    query = Query(Users).filter(Users.id == 1)
    result = data_api.execute(query)
    # SELECT users.id, users.name FROM users WHERE my_table.id = 1

    print(result)
    # [[1, 'ken']]

    result = data_api.execute('select * from users', with_columns=True)
    print(result)
    # [{'id': 1, 'name': 'ken'}]

    # batch insert
    insert: Insert = Insert(Users)
    data_api.execute(insert, [
        {'id': 2, 'name': 'rei'},
        {'id': 3, 'name': 'lisa'},
        {'id': 4, 'name': 'taro'},
    ])

    result = data_api.execute('select * from users')
    print(result)
    # [[1, 'ken'], [2, 'rei'], [3, 'lisa'], [4, 'taro']]