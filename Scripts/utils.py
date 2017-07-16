from logger import log_error
from dbUtil import download_code_exists


def decode_time(encryptedHour):
    hours_char = encryptedHour[0:1]
    minute_tens = encryptedHour[1:2]
    minute_digit = encryptedHour[2:3]
    hours = decode_hour(hours_char)

    if hours is None:
        return None

    minute_first = decode_minute_tens(minute_tens)
    if minute_first is None:
       return None

    minute_second = decode_minute_digits(minute_digit)
    if minute_second is None:
        return None

    return ""+hours+":"+minute_first+""+minute_second

def decode_hour(hours_char):
    return {
            'A':'00',
            'B':'01',
            'C':'02',
            'D':'03',
            'E':'04',
            'F':'05',
            'G':'06',
            'H':'07',
            'I':'08',
            'J':'09',
            'K':'10',
            'L':'11',
            'M':'12',
            'N':'13',
            'O':'14',
            'P':'15',
            'Q':'16',
            'R':'17',
            'S':'18',
            'T':'19',
            'U':'20',
            'V':'21',
            'W':'22',
            'X':'23',
        }.get(hours_char, None)

def decode_minute_tens(minute_tens):
    return {
            'A':'0',
            'B':'1',
            'C':'2',
            'D':'3',
            'E':'4',
            'F':'5',
        }.get(minute_tens, None)

def decode_minute_digits(minute_digit):
    return {
            'A':'0',
            'B':'1',
            'C':'2',
            'D':'3',
            'E':'4',
            'F':'5',
            'G':'6',
            'H':'7',
            'I':'8',
            'J':'9',
        }.get(minute_digit, None)


def is_valid_code(code):
    try:
        if(len(code) > 4):
            if code == "ABC123":
                ##TODO DEBUG - sacar
                return True
            else:
                video_code = code[:-3]
                encrypted_time = code[-3:]
                time = decode_time(encrypted_time)
                if time is not None:
                    if(download_code_exists(video_code)):
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            return False
        
    except Exception as e:
        log_error('SYSTEM', 'SYSTEM', 'fileUtil.py - validate_code()', str(e))
        return False
