def parsing_noHp(value):
    # convert value to str
    value = str(value)
    if value[:3] == '628':
        value = value.replace(value[:3], '08')

    return value
