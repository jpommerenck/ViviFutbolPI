from dbUtil import get_all_marks_between_dates

marks = get_all_marks_between_dates('2016-10-15_12-04-23', '2016-10-15_12-04-50')


for row in marks:
    print(row)

#MP4Box -cat /home/pi/Desktop/v1.h264:fps=30 -cat /home/pi/Desktop/v2.h264:fps=30 -cat /home/pi/Desktop/v3.h264:fps=30 -cat /home/pi/Desktop/v4.h264:fps=30 -new /home/pi/Desktop/v1234.mp4

    
