import re

import pandas as pd
from django.db import connection
import numpy as np
from datetime import datetime
from  dateutil.relativedelta import relativedelta


def parse_data(data_object):
    for item in data_object:
        if not data_object[item]:
            data_object[item][item] = 0
    return data_object


def parse_data_bar(data, keys):
    new_data = []
    for key in keys["keys"]:
        new_data.append({"name": key["value"], "count": data[key["name"]] if key["name"] in data else 0})

    return new_data


def check_keys(data, keys):
    new_data = {}
    for key in keys["keys"]:
        new_data[key["value"]] = 0
        if key["name"] in data:
            new_data[key["value"]] = data[key["name"]]
    return new_data


def extract_key_from_dataframe(dataframe, column_name, required_keys=None):
    final_data = {}
    if required_keys is None:
        required_keys = []

    if dataframe.size == 0:
        for key in required_keys:
            final_data[key] = 0
    else:
        data = dataframe.groupby(column_name).size()
        keys = data.keys()
        for key in keys:
            final_data[key] = int(data[key])
        for key in required_keys:
            if key not in keys:
                final_data[key] = 0
    return final_data


def check_required_fields(json_data: dict, required_fields: dict):
    success = False
    for attr_name, attr_type in required_fields.items():
        if attr_name in json_data:
            if type(json_data[attr_name]) in attr_type:
                success = True
            else:
                success = False
                break
        else:
            success = False
            break
    return success


def dict_conversion(data: dict, change_format):
    if change_format:
        final_data = []
        for k, v in data.items():
            final_data.append({"count": int(v), "name": str(k).title() if not str(k).isupper() else k})
    else:
        final_data = {}
        for k, v in data.items():
            final_data[str(k).title() if not str(k).isupper() else k] = int(v)
    return final_data


def compare_chart(graph_data: list, start_date, end_date):
    required_fields = {
        "field_name": [str]
    }
    final_data = {}
    for query_data in graph_data:
        success = check_required_fields(query_data, required_fields)
        if success:
            field_name = str(query_data["field_name"]).title()
            count_chart_data = count_chart(query_data, start_date, end_date, convert_data=False)
            if count_chart_data:
                final_data[field_name] = count_chart_data
        else:
            print("Query Data Fail")

    return final_data


def count_chart(json_data: dict, start_date, end_date, convert_data=True):
    required_fields = {
        "query": [str],
        "others": [bool],
        "count_column": [str],
        "required_columns": [str, list],
        "count": [bool],
        "group_by_field": [str, list]
    }
    params_check = check_required_fields(json_data, required_fields)
    if params_check:
        query = json_data["query"]
        if check_query(query):
            final_data = {}
            try:
                dataset = pd.read_sql_query(query, params={"start": start_date, "end": end_date}, con=connection)
                is_count = json_data["count"]
                group_by_field = json_data["group_by_field"]
                required_columns = json_data["required_columns"]
                if is_count:
                    if len(group_by_field) == 1 or type(group_by_field) == str:
                        group_by_field = group_by_field if type(group_by_field) == str else group_by_field[0]
                        dataset_column = dataset.columns[0]
                        if len(dataset.columns) == 1:
                            dataset["temp"] = 1
                        dataset_column = dataset_column if dataset_column != group_by_field else dataset.columns[1]
                        dataset[dataset_column] = dataset.fillna("val")
                        dataset = dataset.groupby(dataset[group_by_field].str.lower()).count()[dataset_column]
                    else:
                        dataset.replace(to_replace="None", value=np.nan, inplace=True)
                        dataset = dataset.count()
                        # Adding Group by to Required if not Present
                        for group_by in group_by_field:
                            if str(group_by).lower() not in [str(each_col).lower() for each_col in required_columns]:
                                list(required_columns).append(group_by)
                else:
                    group_by_field = group_by_field if type(group_by_field) == str else group_by_field[0]
                    count_column = json_data["count_column"]
                    dataset = dataset.set_index(dataset[group_by_field].str.lower())[count_column]
                dataset = dataset.sort_values(ascending=False)
                required_columns = required_columns if type(required_columns) == list else [required_columns]
                dataset_index = dataset.index
                for column in required_columns:
                    if column.lower() not in dataset_index.str.lower():
                        count = 0
                    else:
                        count = dataset[column.lower()]
                    final_data[column.lower()] = count
                for item in dataset_index:
                    if item not in final_data:
                        if len(final_data) < 6:
                            final_data[item.lower()] = dataset[item]
                        else:
                            break
                is_others = json_data["others"]
                if is_others:
                    keys = [key for key in final_data]
                    left_keys = list(set(dataset_index) - set(keys))
                    final_data["Others"] = dataset[left_keys].sum()
                not_required_columns = json_data["not_required_fields"] if "not_required_fields" in json_data else []
                for nr_column in not_required_columns:
                    if nr_column.lower() in final_data:
                        final_data.pop(nr_column.lower())
                if "rename_columns" in json_data:
                    keys_list = json_data["rename_columns"]
                    if keys_list:
                        rename_keys(final_data, keys_list)
                return dict_conversion(final_data, convert_data)

            except Exception as e:
                print(e)
        else:
            print("Query Fails")
    else:
        print("Args failes")


def check_query(query: str, restrict_key=None):
    restrict_key = [] if not restrict_key else restrict_key
    success = True
    restrict_keywords = ["delete", "update", "truncate", "drop", "insert", "create", "show"]
    restrict_keywords.extend(restrict_key)
    for keyword in restrict_keywords:
        if f' {keyword} ' in f' {query} ':
            success = False
            break

    return success


def rename_keys(final_data: dict, keys: dict):
    for key, value in keys.items():
        key_lower = str(key).lower()
        if key_lower in [str(data).lower() for data in final_data]:
            final_data[value] = final_data[key_lower]
            final_data.pop(key_lower)


def create_graph(json_data, start_date, end_date):
    required_fields = {
        "title": [str],
        "graph_type": [int],
        "graph_data": [dict, list]
    }
    success = check_required_fields(json_data, required_fields)
    if success:
        graph_type = json_data["graph_type"]
        graph_type_switcher = {
            1: count_chart,
            2: count_chart,
            3: count_chart,
            4: compare_chart
        }
        data = graph_type_switcher.get(graph_type, "Graph Type not Found/Null")
        if graph_type in [1, 2, 3]:
            graph_data = json_data["graph_data"][0] if type(json_data["graph_data"]) == list else json_data[
                "graph_data"]
        else:
            graph_data = json_data["graph_data"]
        data = data(graph_data, start_date, end_date)
        return data
    else:
        return {}


def _verify_query(query):
    cursor = connection.cursor()
    if check_query(query):
        try:
            cursor.execute(query, {"start": "2020-05-01", "end": "2020-05-30"})
            success = True
            msg = "Query Success"
        except Exception as e:
            success = False
            msg = e
    else:
        success = False
        msg = "Restrict Keywords Used"
    return success, str(msg)


def verify_count_data(data):
    try:
        required_fields = ["title", "query", "graph_type", "group_by_field"]
        msg = []
        success = True
        for field in required_fields:
            if field not in data:
                msg.append({field: f"This not Found"})
                success = False
            else:
                if not data[field]:
                    msg.append({field: f"This Cannot be left blank"})
                    success = False
        if success:
            query = data["query"]
            query_success, query_msg = _verify_query(query)
            if not query_success:
                success = False
                msg.append({"query": query_msg})
            else:
                success = True
                msg = _create_count_chart_json(data)

        return success, msg
    except Exception as e:
        return False, "Some Error Occurred, Contact Admin"


def _create_count_chart_json(data, is_multi=False):
    if not is_multi:
        graph_type = int(data["graph_type"])
        title = data["title"]
        final_json = {"graph_type": graph_type, "title": title, "graph_data": []}
    else:
        final_json = {"graph_data": []}
    graph_data = {}
    for key, value in data.items():
        if key not in ["graph_type", "title"]:
            if value == "false":
                value = False
            elif value == "true":
                value = True
            graph_data[key] = value

    temp_rename = {}
    for i, field in enumerate(graph_data["rename_columns"]):
        if ":" in field:
            key, value = field.split(":", 1)
            temp_rename[key] = value
        else:
            graph_data["rename_columns"].pop(i)
    graph_data["rename_columns"] = temp_rename if temp_rename else {}
    final_json["graph_data"].append(graph_data)
    return final_json


def verify_comparison_data(data):
    required_fields = {"single": ["title", "graph_type"], "multi": ["query", "group_by_field", "field_name"]}
    total_forms = int(data["form-TOTAL_FORMS"])
    temp_required_fields = []
    error = []
    success = True
    final_json = {}
    if total_forms > 1:
        for key, required_field in required_fields.items():
            if key == "single":
                temp_required_fields.extend(required_field)
            else:
                for i in range(0, total_forms):
                    for field in required_field:
                        field_name = f"form-{i}-{field}"
                        if field_name in data:
                            if not data[field_name]:
                                success = False
                                error.append({field_name: "This Field is Required"})
                        else:
                            success = False
                            error.append({field: "This Not Found"})
        if success:
            for i in range(0, total_forms):
                query_key = f"form-{i}-query"
                query = data[query_key]
                query_success, query_error = _verify_query(query)
                if not query_success:
                    success = False
                    error.append({query_key: query_error})

            if success:
                final_json["graph_type"] = int(data["graph_type"])
                final_json["title"] = data["title"]
                final_json["graph_data"] = []
                for i in range(0, total_forms):
                    form_data = {}
                    for key, value in data.items():
                        new_key = re.findall(f"form-{i}-(.*)", key)
                        new_key = new_key[0] if new_key else None
                        if new_key:
                            form_data[new_key] = value
                    final_json["graph_data"].append(_create_count_chart_json(form_data, True)["graph_data"][0])
                error = final_json

    else:
        success = False
        error = [{"common": "More than 1 field required for Comparison"}]
    return success, error


def verify_chart_data(data: dict):
    if "graph_type" in data:
        graph_type = int(data["graph_type"])
        if graph_type in [1, 2, 3]:
            success, msg = verify_count_data(data)
        elif graph_type == 4:
            success, msg = verify_comparison_data(data)
        else:
            success, msg = (None, None)
    else:
        success = False
        msg = "Graph Not Defined"

    return success, msg


def get_chart_data(data):
    success = False
    end = datetime.now()
    start = end - relativedelta(months=3)
    chart_data = create_graph(data, start, end)
    if chart_data:
        success = True
    else:
        chart_data = [{"common": "No Data Found"}]
    return success, chart_data
