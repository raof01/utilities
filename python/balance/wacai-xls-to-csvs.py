# -*- coding: utf-8 -*-

import argparse
import xlrd
import pandas as pd
from datetime import datetime
from pathlib2 import Path
import os

# Constants
car_cost_file_name = 'car-cost.csv'
baby_cost_file_name = 'baby-cost.csv'
balance_file_name = 'balance.csv'
car_cost_cata = ['加油', '停车费', '过路过桥', '保养维修', '车款车贷', '罚款赔偿', '车险','驾照费用']
baby_cost_cata = ['育儿', '婴儿用品', '宝宝用品', '婴幼儿用品', '母婴用品', '婴幼儿门诊']
l1_name = 'cata_l1'
l2_name = 'cata_l2'
date_name = 'date'
amount_name = 'amount'
cost_sheet_name = '支出'
transport_name = '交通'
income_name = '收入'

l1_pos = 0
l2_pos = 1
date_pos = 7
amout_pos = 8

income_date_pos = 5
income_amount_pos = 6

def xl_date_to_date_str(d, mode):
    return datetime.strptime(
        str(datetime(*xlrd.xldate_as_tuple(d, mode)))[:10], '%Y-%m-%d')

def append_to_csv(df, file_name):
    f = Path(file_name)
    if not f.exists():
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        with open(file_name, 'a') as output:
            df.to_csv(output, header=False, index=False, encoding='utf-8-sig')

def get_running_sum(ds):
    running_sum = [ds[0]]
    for i in range(1, ds.size):
        running_sum.append(ds[i] + running_sum[i-1])
    return running_sum

def get_cost_data_frame(workbook):
    sheet = workbook.sheet_by_name(cost_sheet_name)
    cata_l1 = [sheet.col(l1_pos)[i].value for i in range(1, sheet.nrows)]
    cata_l2 = [sheet.col(l2_pos)[i].value for i in range(1, sheet.nrows)]
    date = [xl_date_to_date_str(sheet.col(date_pos)[i].value, workbook.datemode) for i in range(1, sheet.nrows)]
    amount = [sheet.col(amout_pos)[i].value for i in range(1, sheet.nrows)]
    data = pd.DataFrame()
    data[l1_name] = pd.Series(cata_l1)
    data[l2_name] = pd.Series(cata_l2)
    data[date_name] = pd.Series(date)
    data[amount_name] = pd.Series(amount)
    data.sort_values(by=date_name, inplace=True)
    return data

def get_car_cost_data_frame(df):
    car_cost = df[df[l1_name].__eq__(transport_name)
                  & df[l2_name].__eq__(car_cost_cata[0])
                  | df[l2_name].__eq__(car_cost_cata[1])
                  | df[l2_name].__eq__(car_cost_cata[2])
                  | df[l2_name].__eq__(car_cost_cata[4])
                  | df[l2_name].__eq__(car_cost_cata[5])
                  | df[l2_name].__eq__(car_cost_cata[6])
                  | df[l2_name].__eq__(car_cost_cata[7])]
    car_cost = car_cost.drop({l1_name, l2_name}, axis=1)
    car_cost.sort_values('date')
    return car_cost

def get_baby_cost_data_frame(df):
    baby_cost = df[df[l1_name].__eq__(baby_cost_cata[0])
                   | df[l2_name].__eq__(baby_cost_cata[1])
                   | df[l2_name].__eq__(baby_cost_cata[2])
                   | df[l2_name].__eq__(baby_cost_cata[3])
                   | df[l2_name].__eq__(baby_cost_cata[4])
                   | df[l2_name].__eq__(baby_cost_cata[5])]
    baby_cost = baby_cost.drop({l1_name, l2_name}, axis=1)
    baby_cost.sort_values('date', inplace=True)
    return baby_cost

def get_income_data_frame(workbook):
    income_sheet = workbook.sheet_by_name(income_name)
    income_date = [xl_date_to_date_str(income_sheet.col(income_date_pos)[i].value,
                                       workbook.datemode) for i in range(1, income_sheet.nrows)]
    income_amount = [income_sheet.col(income_amount_pos)[i].value for i in range(1, income_sheet.nrows)]
    income_data = pd.DataFrame()
    income_data[date_name] = income_date
    income_data[amount_name] = income_amount
    income_data.sort_values('date', inplace=True)
    return income_data

def get_balance_data_frame(df_income, df_cost):
    balance = df_income
    spent = df_cost.drop({l1_name, l2_name}, axis=1)
    spent[amount_name] = spent[amount_name].apply(lambda x: -x)
    balance = balance.append(spent, ignore_index=True)
    balance.sort_values('date', inplace=True)
    return balance

def get_reduced_data_frame(df):
    reduced = df.groupby(date_name)[amount_name].sum()
    return pd.DataFrame(reduced).reset_index()

def convert(file_name, output_dir):
    # load cost data to data frame
    workbook = xlrd.open_workbook(file_name)
    data = get_cost_data_frame(workbook)

    car_cost = get_car_cost_data_frame(data)
    baby_cost = get_baby_cost_data_frame(data)
    balance = get_balance_data_frame(get_income_data_frame(workbook), data)

    baby_cost_sum_df = get_reduced_data_frame(baby_cost)
    car_cost_sum_df = get_reduced_data_frame(car_cost)
    balance_sum_df = get_reduced_data_frame(balance)

    append_to_csv(car_cost_sum_df, output_dir + os.path.sep +  car_cost_file_name)
    append_to_csv(baby_cost_sum_df, output_dir + os.path.sep + baby_cost_file_name)
    append_to_csv(balance_sum_df, output_dir + os.path.sep + balance_file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='wacai-xls-to-csvs.py',
                                     description='Convert xls exported from wacai to csv files')
    parser.add_argument('-i', dest='input_xls', required=True, type=str, nargs='+',
                        help='Xls files to be converted')
    # Optional arguments
    parser.add_argument('-o', dest='output_dir', type=str,
                        help='Output path for csv fiels')

    args = parser.parse_args()
    if args.output_dir is None:
        args.output_dir = '.'
    args.input_xls.sort()
    for xls in args.input_xls:
        print('Converting ' + xls)
        convert(xls, args.output_dir)
        print('Done')
