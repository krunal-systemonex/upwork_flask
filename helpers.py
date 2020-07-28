from constants import *

import pandas as pd
import boto3
import os
import configparser

def read_aws_creds():
    config = configparser.RawConfigParser()
    path = os.path.join('/home/ubuntu','.aws/credentials')
    config.read(path)
    ACCESS_KEY_ID = config.get('default', 'aws_access_key_id') ##configparser.NoSectionError: No section: 'default'
    ACCESS_SECRET_KEY = config.get('default', 'aws_secret_access_key') ##configparser.NoSectionError: No section: 'default'
    return (ACCESS_KEY_ID, ACCESS_SECRET_KEY)    

ACCESS_KEY_ID, ACCESS_SECRET_KEY = read_aws_creds()
dynamodb_client = boto3.resource('dynamodb', region_name='eu-central-1', aws_access_key_id=ACCESS_KEY_ID,aws_secret_access_key=ACCESS_SECRET_KEY)
table = dynamodb_client.Table(DYNAMODB_TABLE_NAME)

def get_excel_files(excel_file_path=EXCEL_FILE_PATH):
    excel_file_list = []
    for folder, sub, filespath in os.walk(excel_file_path):
        for file in filespath:
            if file.endswith(".xls") or file.endswith(".xlsx"):
                excel_file_list.append(os.path.join(folder,file))
    return excel_file_list


def read_excel():
    excel_files_list = get_excel_files()
    df_lst = []
    for filepath in excel_files_list:
        excel_data_df = pd.read_excel(filepath) #, sheet_name='sheet1'
        df_lst.append(excel_data_df)
    # print whole sheet data
    return df_lst


def mapper(input_dict):
    schema_dict = {"client_name":"client_name","DATE":"date", "DAILY":"daily_profit_loss", "Notional":"notional",
    "_4":"notional_minus_realized_gains", 
    "_5":"net_notional_plus_minus_unrealized_gain_loss",
    "_6":"beginning_margin_balance",
    "_7":"unrealized_gain_loss",
    "_8":"realized_gain_Loss",
    "_9":"realized_gain_Loss_total",
    "_10":"mgt_fee",
    "_11":"mgt_fee_per_day",
    "_12":"accrd_mgt_fee",
    "_13":"pf_fee",
    "HWM":"hwm",
    "_15":"invoice_amount",
    "NAV":"nav"
    }
    return_dict ={}
    del input_dict["Index"]
    for key,value in input_dict.items():
        key_name = schema_dict[key]
        return_dict[key_name] = str(value)
    return return_dict

def update_dynamodb_records(df_lst):
    for df in df_lst:
        client_name = df.iloc[0][3]
        df_col = df.iloc[1].reset_index()[1]
        df_val = df[5:]
        df_val.columns = df_col
        df_val.reset_index()
        with table.batch_writer() as batch:
            for record in df_val.itertuples():
                dc={"client_name":client_name}
                dc.update(record._asdict())
                mapped_dict = mapper(dc)
                print(mapped_dict)
                batch.put_item(Item=mapped_dict)


def get_dynamo_db_data(client_name_lst=None):
    cl_lst = client_name_lst if client_name_lst else [DEFAULT_CLIENT]
    response_lst = []
    for client in cl_lst:
        response = table.query(
            TableName=DYNAMODB_TABLE_NAME,
            KeyConditionExpression=f'client_name = :client_name',
            ExpressionAttributeValues={
                ':client_name': client
            }
        )
        response_lst.extend(response['Items'])
    return response_lst

# [program:hello_world]
# directory=/home/ubuntu/hello_world
# command=/home/ubuntu/.env/bin/gunicorn app:app -b localhost:8000
# autostart=true
# autorestart=true
# stderr_logfile=/var/log/hello_world/hello_world.err.log
# stdout_logfile=/var/log/hello_world/hello_world.out.log


# df_lst = read_excel()
# update_dynamodb_records(df_lst)
