import parsedatetime

cal: parsedatetime.Calendar = parsedatetime.Calendar()


def parse_time(raw_date, raw_time):
    parsed_time = convert_numeric_time(raw_time)
    return cal.parseDT(f"{raw_date}, {parsed_time}")[0]


def convert_numeric_time(raw_time):
    try:
        x = int(raw_time)
        if x > 24:
            return raw_time[:-2] + ":" + raw_time[-2:]
        return raw_time + ":00"
    except:
        try:
            x = float(raw_time)
            return str(int(x)) + ":" + str("%.2f" % x)[3:]
        except:
            return raw_time
