def getParams(start, length, company):
    return (
        ("draw", "2"),
        ("columns[0][data]", "DT_Row_Index"),
        ("columns[0][name]", ""),
        ("columns[0][searchable]", "false"),
        ("columns[0][orderable]", "false"),
        ("columns[0][search][value]", ""),
        ("columns[0][search][regex]", "false"),
        ("columns[1][data]", "published_date"),
        ("columns[1][name]", ""),
        ("columns[1][searchable]", "true"),
        ("columns[1][orderable]", "false"),
        ("columns[1][search][value]", ""),
        ("columns[1][search][regex]", "false"),
        ("columns[2][data]", "open"),
        ("columns[2][name]", ""),
        ("columns[2][searchable]", "false"),
        ("columns[2][orderable]", "false"),
        ("columns[2][search][value]", ""),
        ("columns[2][search][regex]", "false"),
        ("columns[3][data]", "high"),
        ("columns[3][name]", ""),
        ("columns[3][searchable]", "false"),
        ("columns[3][orderable]", "false"),
        ("columns[3][search][value]", ""),
        ("columns[3][search][regex]", "false"),
        ("columns[4][data]", "low"),
        ("columns[4][name]", ""),
        ("columns[4][searchable]", "false"),
        ("columns[4][orderable]", "false"),
        ("columns[4][search][value]", ""),
        ("columns[4][search][regex]", "false"),
        ("columns[5][data]", "close"),
        ("columns[5][name]", ""),
        ("columns[5][searchable]", "false"),
        ("columns[5][orderable]", "false"),
        ("columns[5][search][value]", ""),
        ("columns[5][search][regex]", "false"),
        ("columns[6][data]", "per_change"),
        ("columns[6][name]", ""),
        ("columns[6][searchable]", "false"),
        ("columns[6][orderable]", "false"),
        ("columns[6][search][value]", ""),
        ("columns[6][search][regex]", "false"),
        ("columns[7][data]", "traded_quantity"),
        ("columns[7][name]", ""),
        ("columns[7][searchable]", "false"),
        ("columns[7][orderable]", "false"),
        ("columns[7][search][value]", ""),
        ("columns[7][search][regex]", "false"),
        ("columns[8][data]", "traded_amount"),
        ("columns[8][name]", ""),
        ("columns[8][searchable]", "false"),
        ("columns[8][orderable]", "false"),
        ("columns[8][search][value]", ""),
        ("columns[8][search][regex]", "false"),
        ("start", start),
        ("length", length),
        ("search[value]", ""),
        ("search[regex]", "false"),
        ("company", company),
        ("_", "1620702742670"),
    )
