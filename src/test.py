# # import sched, time

# # def myTask(m,n):
# #   print(n + ' ' + m)

# # def periodic_queue(interval,func,args=(),priority=1):
# #   s = sched.scheduler(time.time, time.sleep)
# #   periodic_task(s,interval,func,args,priority)
# #   s.run()

# # def periodic_task(scheduler,interval,func,args,priority):
# #   func(*args)
# #   scheduler.enter(interval,priority,periodic_task,
# #                    (scheduler,interval,func,args,priority))

# # periodic_queue(1,myTask,('world','hello'))

# from __future__ import print_function
# import datetime
# import pickle
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

# # If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# def main():
#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)

#     service = build('calendar', 'v3', credentials=creds)

#     # Call the Calendar API
#     now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#     print('Getting the upcoming 10 events')
#     events_result = service.events().list(calendarId='primary', timeMin=now,
#                                         maxResults=10, singleEvents=True,
#                                         orderBy='startTime').execute()
#     events = events_result.get('items', [])

#     if not events:
#         print('No upcoming events found.')
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         print(start, event['summary'])


# if __name__ == '__main__':
#     main()


# import rx
# from rx import operators as ops

# source = rx.of("Alpha", "Beta", "Gamma", "Delta", "Epsilon")

# composed = source.pipe(
#     ops.map(lambda s: len(s)),
#     ops.filter(lambda i: i >= 5)
# )
# composed.subscribe(lambda value: print("Received {0}".format(value)))

# obs1 = rx.from_([1, 2, 3, 4])
# obs2 = rx.from_([5, 6, 7, 8])

# res = rx.merge(obs1, obs2)
# res.subscribe(print)

import shutil
import requests
import os

path = os.getcwd()

def download_image(lable_user_name, file_name):
    # tạo nhãn thư mục ứng với user_name
    parent_path = os.path.join(path, lable_user_name)

    if not os.path.isdir(parent_path):
        os.mkdir(parent_path)

    full_file_name = lable_user_name + "_" + file_name
    url = 'http://192.168.0.101:8000/display/' + full_file_name
    response = requests.get(url, stream=True)
    new_path_file = parent_path + "/" + full_file_name
    with open(new_path_file, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response



images_list = [{'user_name': 'hungvt', 'file_name': 'file0.jpg'}, {'user_name': 'hungvt', 'file_name': 'file1.jpg'}, {'user_name': 'hungvt', 'file_name': 'file2.jpg'}, {'user_name': 'hungvt', 'file_name': 'file3.jpg'}, {'user_name': 'hungvt', 'file_name': 'file4.jpg'}, {'user_name': 'hungvt', 'file_name': 'file5.jpg'}]

for item in images_list:
    print(item['user_name'])

    user_name = item['user_name']
    file_name = item['file_name']
    download_image(lable_user_name=user_name, file_name=file_name)

