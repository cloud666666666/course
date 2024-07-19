import datetime
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
today = datetime.datetime.now().strftime("%A")
course_list=[]
week_list=["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
messages = []
class Course():
    def __init__(self, name,time,location):
        self.name = name
        self.time = time
        self.location = location
    def show(self):
        print(self.name, self.time,self.location)

class timetable():
    def __init__(self,course):
        self.time = course.time
        self.course = course
        self.location = course.location



def get_course():
    with open('get_course.html', 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, "lxml")
    for i in range(4):
        str_name='DERIVED_SSR_FL_SSR_SCRTAB_DTLS$'+str(i)
        str_time='DERIVED_REGFRM1_SSR_MTG_SCHED_LONG$'+str(i)
        str_location='DERIVED_REGFRM1_SSR_MTG_LOC_LONG$'+str(i)
        course_name=soup.find('a',id=str_name).text
        course_time=soup.find('span', id=str_time)
        course_time=[i.text for i in course_time if i.text!='']
        course_location=soup.find('span', id=str_location)
        course_location=[i.text for i in course_location if i.text!='']
        course_list.append(Course(course_name,course_time,course_location))
    return course_list


def convert_time_to_minutes(time_str):
    """将时间段转换为分钟，以便排序"""
    start_time, end_time = time_str.split(' - ')
    start_hour, start_minute = map(int, start_time.split(':'))
    return start_hour * 60 + start_minute


def get_timetable(messages=messages):

    for course in get_course():
        # print(course.name, course.time, course.location)
        for i in range(len(course.time)):
            if course.time[i][0:2] ==today[0:2]:
                messages.append([course.name,course.time[i][2:],course.location[i]])
    messages = sorted(messages, key=lambda x: convert_time_to_minutes(x[1]))
    return (messages)
def send_email(subject, message, to_email):
    SMTP_SERVER = 'smtp.qq.com'
    SMTP_PORT = 587
    SMTP_USERNAME = '2353493891@qq.com'  # 更改为您的Email地址
    SMTP_PASSWORD = 'gswqhdstochteceh'  # 更改为您的Email密码授权码
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = SMTP_USERNAME
    msg['To'] = to_email
    msg['Subject'] = subject
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
def start():
    if messages:
        message=''
        str_subject='Today you will have '+str(len(messages))+' classes'
        for i in messages:
            message+=str(i)+'\n'
    else:
        str_subject='Have a good day!'
        message='There is no class today, go do something you want to do!'
    send_email(subject=str_subject, message=message, to_email='yunhaowang326@gmail.com')

if __name__ == '__main__':
    get_timetable()
    start()
