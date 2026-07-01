_COLUMNS = [
    "DT_Row_Index",
    "published_date",
    "open",
    "high",
    "low",
    "close",
    "per_change",
    "traded_quantity",
    "traded_amount",
]


def build_history_payload(start, length, company, token):
    payload = {
        "draw": 1,
        "start": start,
        "length": length,
        "company": company,
        "_token": token,
        "search[value]": "",
        "search[regex]": "false",
    }
    for i, name in enumerate(_COLUMNS):
        payload[f"columns[{i}][data]"] = name
        payload[f"columns[{i}][name]"] = ""
        payload[f"columns[{i}][searchable]"] = "true" if name == "published_date" else "false"
        payload[f"columns[{i}][orderable]"] = "false"
        payload[f"columns[{i}][search][value]"] = ""
        payload[f"columns[{i}][search][regex]"] = "false"
    return payload
