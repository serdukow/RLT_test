import json
import dateutil.relativedelta as rdelta


from datetime import datetime, timedelta
from aiogram import types

from db import connect_to_mongodb

collection = connect_to_mongodb()


async def calculate(dt_from, dt_upto, group_type):
    if group_type == 'month':
        format_str = "%Y-%m-01T00:00:00"
        group_id = {"$dateToString": {"format": format_str, "date": "$dt"}}
        sort_id = {"_id": 1}
        timedelta_arg = rdelta.relativedelta(months=1)
    elif group_type == 'week':
        format_str = "%Y-%U-1T00:00:00"
        group_id = {"$dateToString": {"format": format_str, "date": "$dt"}}
        sort_id = {"_id": 1}
        timedelta_arg = timedelta(weeks=1)
    elif group_type == 'day':
        format_str = "%Y-%m-%dT00:00:00"
        group_id = {"$dateToString": {"format": format_str, "date": "$dt"}}
        sort_id = {"_id": 1}
        timedelta_arg = timedelta(days=1)
    elif group_type == 'hour':
        format_str = "%Y-%m-%dT%H:00:00"
        group_id = {"$dateToString": {"format": format_str, "date": "$dt"}}
        sort_id = {"_id": 1}
        timedelta_arg = timedelta(hours=1)
    else:
        raise ValueError(f"Invalid group_type: {group_type}")

    pipeline = [
        {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
        {"$group": {"_id": group_id, "total_salary": {"$sum": "$value"}}},
        {"$sort": sort_id}
    ]
    results = list(collection.aggregate(pipeline))
    dataset = []
    labels = []
    current_dt = dt_from
    while current_dt <= dt_upto:
        labels.append(current_dt.strftime(format_str))
        current_dt += timedelta_arg
    for label in labels:
        found = False
        for result in results:
            if label == result['_id']:
                dataset.append(result['total_salary'])
                found = True
                break
        if not found:
            dataset.append(0)
    return {"dataset": dataset, "labels": labels}


async def handle_message(message: types.Message):
    try:
        data = json.loads(message.text)
        dt_from = datetime.strptime(data['dt_from'], '%Y-%m-%dT%H:%M:%S')
        dt_upto = datetime.strptime(data['dt_upto'], '%Y-%m-%dT%H:%M:%S')
        group_type = data['group_type']
        result = await calculate(dt_from, dt_upto, group_type)
        await message.answer(json.dumps(result))
    except Exception as e:
        await message.answer(f"Error: {str(e)}")



