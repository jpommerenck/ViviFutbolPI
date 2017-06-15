from dbUtil import get_log_activity, get_config_value

print(get_config_value("PICTURES_LOCALIZATION_PATH"))
logs = get_log_activity()
for log in logs:
    print(log['action']+' - '+log['description'])
