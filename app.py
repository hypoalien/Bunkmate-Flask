from flask import Flask
from flask import abort
from bs4 import BeautifulSoup
import requests
import html5lib
import json

#initializing flask
app = Flask(__name__)

#endpoint for bio-data, path ='/bio/'
@app.route('/bio/<int:pin>+<int:p_no>', methods=['GET'])
def get_pin(pin,p_no):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }

    # Header data for logging in
    login_data1 = {'txtuserid': pin ,
                  'txtpassword': p_no,
                  'Button2': 'Login',
                  'ctl00$MainContent$Button5': 'This semester'
    }


    student_bio= {

    }
    #starting session
    with requests.Session() as s:
        url = "https://gparent.gitam.edu/login"
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        # extracting headers for login
        login_data1['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data1['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data1['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
        r = s.post(url, data=login_data1, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        #checking if the given username and password are correct
        try:
            student_bio['Name'] = soup.find('input', attrs={'name': 'ctl00$MainContent$txtname'})['value']
        except TypeError:
            abort(401)
        else:
            # extracting student bio data
            soup = BeautifulSoup(r.content, 'html5lib')
            student_bio['Name'] = soup.find('input', attrs={'name': 'ctl00$MainContent$txtname'})['value']
            student_bio['Pin Number'] = soup.find('input', attrs={'name': 'ctl00$MainContent$txtregdno'})['value']
            student_bio['Current Semester'] = soup.find('input', attrs={'name': 'ctl00$MainContent$txtsen'})['value']
            student_bio['Branch'] = soup.find('input', attrs={'name': 'ctl00$MainContent$txtbranch'})['value']

            #converting dictionary into a json object
            json_student_bio = json.dumps(student_bio)
            #returning the student bio
            return json_student_bio


#endpoint for semester attendance, path '/sem_attendance/'
@app.route('/sem_att/<int:pin>+<int:p_no>', methods=['GET'])
def get_semester(pin,p_no):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }

    #header data for logging in
    login_data1 = {'txtuserid': pin,
                  'txtpassword': p_no,
                  'Button2': 'Login',
                  'ctl00$MainContent$Button5': 'This semester'
    }

    # data for semester attendance
    login_data2 = {

        'MainContent_ToolkitScriptManager1_HiddenField': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ctl00$MainContent$Button5': 'This semester'
    }
    sem_att={

    }
    with requests.Session() as s:
        url = "https://gparent.gitam.edu/login"
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        # extracting headers for login
        login_data1['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data1['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data1['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
        r = s.post(url, data=login_data1, headers=headers)

      
        # extracting headers for semester attendance
        url = 'https://gparent.gitam.edu/Attendance_new'
        r = s.get(url, data=login_data1, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        login_data2['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data2['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data2['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
        r = s.post(url, data=login_data2, headers=headers)

        # extracting semester attendance
        soup = BeautifulSoup(r.content, 'html5lib')
        sem_att['semester Attendance'] = soup.find('span', {'id': 'MainContent_lbltotal'}).text.strip()
        #converting dictionary to a json object
        json_sem_att= json.dumps(sem_att)
        #returning semester attendance
        return json_sem_att

#endpoint for subject attendance, path"/subject_attendance
@app.route('/sub_att/<int:pin>+<int:p_no>', methods=['GET'])
def get_subject(pin,p_no):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }

    #headers for logging in
    login_data1 = {'txtuserid': pin,
                  'txtpassword': p_no,
                  'Button2': 'Login',
                  'ctl00$MainContent$Button5': 'This semester'
                  }

    #header data for subject attendance

    login_data3 = {
        'MainContent_ToolkitScriptManager1_HiddenField': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ctl00$MainContent$Button4': 'By subject'
    }
    sub_att = {

    }
    with requests.Session() as s:
        url = "https://gparent.gitam.edu/login"
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        # extracting headers for login
        login_data1['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data1['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data1['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
        r = s.post(url, data=login_data1, headers=headers)

        # checking if the given username and password are correct
        '''try:
            student_bio['Name'] = soup.find('input', attrs={'name': 'ctl00$MainContent$txtname'})['value']
        except TypeError:
            abort(401)
        else:
        '''
        # extracting headers for subject attendance
        url = 'https://gparent.gitam.edu/Attendance_new'
        r = s.get(url, data=login_data1, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        login_data3['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data3['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data3['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']

        #extracting subject attendance
        r = s.post(url, data=login_data3, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.find('div', {'class': 'table-responsive'})
        rows = table.findAll('tr')
        #extracting in a dictionary
        for row in range(1, len(rows)):
            cn = rows[row].findAll('td', attrs={'align': 'left', 'valign': 'middle'})[1].text.strip()
            at = rows[row].findAll('td')[2]
            ca = at.find('span', {'id': 'MainContent_GridView4_lblid_' + str(row - 1)}).text.strip()
            sub_att[cn] = ca
        #converting dictionary into json
        json_sub_att =json.dumps(sub_att)

        return json_sub_att

#endpoint for timeTable, path"/timetable
@app.route('/timetable/<int:pin>+<int:p_no>', methods=['GET'])
def get_timetable(pin,p_no):
    days_array=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    timetable={
        'Monday':'',
        'Tuesday':'',
        'Wednesday':'',
        'Thursday':'',
        'Friday':'',
        'Saturday':'',
    }
    day_time_table={

    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }

    #headers for logging in
    login_data1 = {'txtuserid': pin,
                  'txtpassword': p_no,
                  'Button2': 'Login',
                  'ctl00$MainContent$Button5': 'This semester'
                  }

    #header data for subject attendance

    login_data3 = {
        'MainContent_ToolkitScriptManager1_HiddenField': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ctl00$MainContent$Button4': 'By subject'
    }
    sub_att = {
        'Spt':'Sports/Lib',
        #'AMC':'AMC',
        'Break':'Break',
        'Lunch':'Lunch'

    }
    with requests.Session() as s:
        url = "https://gparent.gitam.edu/login"
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        # extracting headers for login
        login_data1['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data1['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data1['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
        r = s.post(url, data=login_data1, headers=headers)

        # checking if the given username and password are correct
        '''try:
            student_bio['Name'] = soup.find('input', attrs={'name': 'ctl00$MainContent$txtname'})['value']
        except TypeError:
            abort(401)
        else:
        '''
        # extracting headers for subject attendance
        url = 'https://gparent.gitam.edu/Attendance_new'
        r = s.get(url, data=login_data1, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        login_data3['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data3['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data3['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']

        #extracting subject attendance
        r = s.post(url, data=login_data3, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.find('div', {'class': 'table-responsive'})
        rows = table.findAll('tr')
        #extracting in a dictionary
        for row in range(1, len(rows)):
            cn = rows[row].findAll('td', attrs={'align': 'left', 'valign': 'middle'})[0].text.strip()
            at = rows[row].findAll('td')[2]
            ca = rows[row].findAll('td', attrs={'align': 'left', 'valign': 'middle'})[1].text.strip()
            sub_att[cn] = ca
        #converting dictionary into json
        json_sub_att =json.dumps(sub_att)

        #loading timetable page
        url = "https://gparent.gitam.edu/Newtimetable"
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        #extracting timetables
        table= soup.find('div', {'class': 'col-md-12 abcs'})
        rows = table.findAll('tr')
        # extracting in a dictionary
        '''time=rows[0].findAll('th', attrs={'scope': 'col'})
        for row in range(1,len(time)):
            timings[row] =time[row].text.strip()
        print(timings)
        '''
        time = rows[0].findAll('th', attrs={'scope': 'col'})
        for row in range(1, len(rows)):
            for col in range(1, len(time)):
                code=rows[row].findAll('td')[col].text.strip()
                if '/' in code:
                    print(code)
                    code =code.split('/', 1)[-1]
                    print(code)
                    print(sub_att[code])

                try:
                    day_time_table[time[col].text.strip()]=sub_att[code]
                except KeyError:
                    day_time_table[time[col].text.strip()] = code

            timetable[days_array[row-1]]=day_time_table

        #print(day_time_table)
        #print(timetable)


        return timetable

#endpoint for today attendance, path"/today_att
@app.route('/today_att/<int:pin>+<int:p_no>', methods=['GET'])
def get_today_att(pin,p_no):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }

    #headers for logging in
    login_data1 = {'txtuserid': pin,
                  'txtpassword': p_no,
                  'Button2': 'Login',
                  #'ctl00$MainContent$Button5': 'This semester'
                  }

    #header data for subject attendance

    login_data3 = {
        'MainContent_ToolkitScriptManager1_HiddenField': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ctl00$MainContent$Button1': 'Today'
    }
    empty={

    }
    sub_att = {

    }
    with requests.Session() as s:
        url = "https://gparent.gitam.edu/login"
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        # extracting headers for login
        login_data1['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data1['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data1['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
        r = s.post(url, data=login_data1, headers=headers)

        # checking if the given username and password are correct
        '''try:
            student_bio['Name'] = soup.find('input', attrs={'name': 'ctl00$MainContent$txtname'})['value']
        except TypeError:
            abort(401)
        else:
        '''
        # extracting headers for subject attendance
        url = 'https://gparent.gitam.edu/Attendance_new'
        r = s.get(url, data=login_data1, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        login_data3['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data3['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data3['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']

        #extracting subject attendance
        r = s.post(url, data=login_data3, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.find( attrs={'class': 'col-md-12'})
        try:

            rows = table.findAll('tr')
            print(rows)
            #extracting in a dictionary
            for row in range(1, len(rows)):
                cn = rows[row].findAll('td', attrs={'align': 'left', 'valign': 'middle'})[1].text.strip()

                ca = rows[row].findAll('td')[3].text.strip()
                #ca = at.find('span', {'id': 'MainContent_GridView4_lblid_' + str(row - 1)}).text.strip()
                sub_att[cn] = ca

        except IndexError:
            return empty
        #converting dictionary into json
        json_sub_att =json.dumps(sub_att)

        return json_sub_att

#endpoint for Login
@app.route('/login/<int:pin>+<int:p_no>', methods=['GET'])
def get_login(pin,p_no):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }

    # Header data for logging in
    login_data1 = {'txtuserid': pin ,
                  'txtpassword': p_no,
                  'Button2': 'Login',
                  'ctl00$MainContent$Button5': 'This semester'
    }
    login_data2 = {

        'MainContent_ToolkitScriptManager1_HiddenField': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ctl00$MainContent$Button5': 'This semester'

    }
    login_data3 = {
        'MainContent_ToolkitScriptManager1_HiddenField': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ctl00$MainContent$Button4': 'By subject'
    }

    sub_att = {

    }
    sem_att = {

    }


    student_bio= {

    }
    #starting session
    with requests.Session() as s:
        url = "https://gparent.gitam.edu/login"
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        # extracting headers for login
        login_data1['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data1['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data1['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
        r = s.post(url, data=login_data1, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        # extracting student bio data

        student_bio['Name'] = soup.find('input', attrs={'name': 'ctl00$MainContent$txtname'})['value']
        student_bio['Pin Number'] = soup.find('input', attrs={'name': 'ctl00$MainContent$txtregdno'})['value']
        student_bio['Current Semester'] = soup.find('input', attrs={'name': 'ctl00$MainContent$txtsen'})['value']
        student_bio['Branch'] = soup.find('input', attrs={'name': 'ctl00$MainContent$txtbranch'})['value']


        #converting dictionary into a json object
        json_student_bio = json.dumps(student_bio)


        url = 'https://gparent.gitam.edu/Attendance_new'
        r = s.get(url, data=login_data1, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        login_data2['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data2['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data2['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
        r = s.post(url, data=login_data2, headers=headers)

        # extracting semester attendance
        soup = BeautifulSoup(r.content, 'html5lib')
        sem_att['semester Attendance'] = soup.find('span', {'id': 'MainContent_lbltotal'}).text.strip()
        # converting dictionary to a json object
        json_sem_att = json.dumps(sem_att)

        url = 'https://gparent.gitam.edu/Attendance_new'
        r = s.get(url, data=login_data1, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        login_data3['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data3['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data3['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']

        # extracting subject attendance
        r = s.post(url, data=login_data3, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.find('div', {'class': 'table-responsive'})
        rows = table.findAll('tr')
        # extracting in a dictionary
        for row in range(1, len(rows)):
            cn = rows[row].findAll('td', attrs={'align': 'left', 'valign': 'middle'})[1].text.strip()
            at = rows[row].findAll('td')[2]
            ca = at.find('span', {'id': 'MainContent_GridView4_lblid_' + str(row - 1)}).text.strip()
            sub_att[cn] = ca
        # converting dictionary into json

        student_bio
        login = {
            'bio':student_bio,
            'sem':sem_att,
            'sub':sub_att
        }
        json_login= json.dumps(login)
        return json_login

@app.route('/api_call/<int:pin>+<int:p_no>', methods=['GET'])
def get_api_call(pin,p_no):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }

    # Header data for logging in
    login_data1 = {'txtuserid': pin ,
                  'txtpassword': p_no,
                  'Button2': 'Login',
                  'ctl00$MainContent$Button5': 'This semester'
    }
    login_data2 = {

        'MainContent_ToolkitScriptManager1_HiddenField': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ctl00$MainContent$Button5': 'This semester'

    }
    login_data3 = {
        'MainContent_ToolkitScriptManager1_HiddenField': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ctl00$MainContent$Button4': 'By subject'
    }

    sub_att = {

    }
    sem_att = {

    }


    student_bio= {

    }
    #starting session
    with requests.Session() as s:
        url = "https://gparent.gitam.edu/login"
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        # extracting headers for login
        login_data1['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data1['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data1['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
        r = s.post(url, data=login_data1, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        # extracting student bio data

        url = 'https://gparent.gitam.edu/Attendance_new'
        r = s.get(url, data=login_data1, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        login_data2['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data2['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data2['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
        r = s.post(url, data=login_data2, headers=headers)

        # extracting semester attendance
        soup = BeautifulSoup(r.content, 'html5lib')
        #sem_att['semester Attendance'] = soup.find('span', {'id': 'MainContent_lbltotal'}).text.strip()
        sem_att['semester Attendance']="30.00"
        # converting dictionary to a json object
        json_sem_att = json.dumps(sem_att)

        url = 'https://gparent.gitam.edu/Attendance_new'
        r = s.get(url, data=login_data1, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        login_data3['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data3['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data3['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']

        # extracting subject attendance
        r = s.post(url, data=login_data3, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        table = soup.find('div', {'class': 'table-responsive'})
        rows = table.findAll('tr')
        # extracting in a dictionary
        for row in range(1, len(rows)):
            cn = rows[row].findAll('td', attrs={'align': 'left', 'valign': 'middle'})[1].text.strip()
            at = rows[row].findAll('td')[2]
            ca = at.find('span', {'id': 'MainContent_GridView4_lblid_' + str(row - 1)}).text.strip()
            sub_att[cn] = ca
        # converting dictionary into json

        student_bio
        login_call = {
            'sem':sem_att,
            'sub':sub_att
        }
        json_login_call= json.dumps(login_call)
        return json_login_call

@app.route('/backlogs/<int:pin>+<int:p_no>',methods=['GET'])
def get_backlogs(pin,p_no):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }

    # Header data for logging in
    login_data1 = {'txtuserid': pin ,
                  'txtpassword': p_no,
                  'Button2': 'Login',
                  'ctl00$MainContent$Button5': 'This semester'
    }
    empty={

    }

    student_backlogs= {

    }
    #starting session
    with requests.Session() as s:
        url = "https://gparent.gitam.edu/login"
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        # extracting headers for login
        login_data1['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data1['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data1['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
        r = s.post(url, data=login_data1, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        #checking if the given username and password are correct
        try:
            sName = soup.find('input', attrs={'name': 'ctl00$MainContent$txtname'})['value']
            print (sName)
        except TypeError:
            abort(401)
        else:

            url = "https://gparent.gitam.edu/backlogs"
            r = s.get(url, headers=headers)

            # extracting student backlogs
            soup = BeautifulSoup(r.content, 'html5lib')
            table = soup.find('table', {'id': 'MainContent_GridView1'})
            print (table)

            try:

                rows = table.findAll('tr')
                # extracting in a dictionary
                for row in range(1, len(rows)):
                    student_backlogs['subject code'] = rows[row].findAll('td')[0].text.strip()
                    student_backlogs['subject name'] = rows[row].findAll('td')[1].text.strip()
                    student_backlogs['grade'] = rows[row].findAll('td')[2].text.strip()
                    student_backlogs['semester'] = rows[row].findAll('td')[3].text.strip()
            except IndexError:
                return empty


            #converting dictionary into a json object
            print (student_backlogs)
            json_student_backlogs = json.dumps(student_backlogs)
            #returning the student bio
            return json_student_backlogs

@app.route('/academic/<int:pin>+<int:p_no>',methods=['GET'])
def get_academic(pin,p_no):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }
    student_backlogs = {

    }
    # Header data for logging in
    sub_grade={

    }
    sub_grade_all={

    }
    cgpa={

    }
    sgpa={

    }
    login_data1 = {'txtuserid': pin,
                   'txtpassword': p_no,
                   'Button2': 'Login',
                   'ctl00$MainContent$Button5': 'This semester'
                   }
    login_data2 = {'txtuserid': pin,
                   'txtpassword': p_no,
                   'Button2': 'Login',
                   '__EVENTARGUMENT': '',
                   '__LASTFOCUS': '',
                   '__EVENTTARGET': '',
                   '__VIEWSTATE': '',
                   '__VIEWSTATEGENERATOR': '',
                   '__EVENTVALIDATION': '',
                   'ctl00$MainContent$ddlexternal': ''
                   }

    student_bio = {

    }
    # starting session
    with requests.Session() as s:
        url = "https://gparent.gitam.edu/login"
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        # extracting headers for login
        login_data1['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        login_data1['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        login_data1['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']

        r = s.post(url, data=login_data1, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')

        # checking if the given username and password are correct
        try:
            student_bio['Name'] = soup.find('input', attrs={'name': 'ctl00$MainContent$txtname'})['value']
        except TypeError:
            abort(401)
        else:
            soup = BeautifulSoup(r.content, 'html5lib')
            student_bio['Current Semester'] = int(soup.find('input', attrs={'name': 'ctl00$MainContent$txtsen'})['value'])

            url = "https://gparent.gitam.edu/backlogs"
            r = s.get(url, data=login_data1,headers=headers)

            # extracting student backlogs
            soup = BeautifulSoup(r.content, 'html5lib')
            table = soup.find('table', {'id': 'MainContent_GridView1'})
            print (table)

            rows = table.findAll('tr')
            # extracting in a dictionary
            for row in range(1, len(rows)):
                student_backlogs['subject code'] = rows[row].findAll('td')[0].text.strip()
                student_backlogs['subject name'] = rows[row].findAll('td')[1].text.strip()
                student_backlogs['grade'] = rows[row].findAll('td')[2].text.strip()
                student_backlogs['semester'] = rows[row].findAll('td')[3].text.strip()

            # extracting student bio data
            url = "https://gparent.gitam.edu/Academictrack"
            r = s.get(url, data =login_data1,headers=headers)
            soup = BeautifulSoup(r.content, 'html5lib')
            login_data2['__EVENTTARGET'] = soup.find('input', attrs={'name': '__EVENTTARGET'})['value']
            login_data2['__EVENTARGUMENT'] = soup.find('input', attrs={'name': '__EVENTARGUMENT'})['value']
            login_data2['__LASTFOCUS'] = soup.find('input', attrs={'name': '__LASTFOCUS'})['value']
            login_data2['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
            login_data2['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
            login_data2['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']


            for x in range(1,student_bio['Current Semester']-1):
                login_data2['ctl00$MainContent$ddlexternal']=x

                r = s.post(url, data=login_data2, headers=headers)
                soup = BeautifulSoup(r.content, 'html5lib')

                table = soup.find('table', attrs={'class': 'table table-3','id':'MainContent_grdresults'})

                rows = table.findAll('tr')

                # extracting in a dictionary
                for row in range(1, len(rows)):

                    sn= rows[row].findAll('td')[0].text.strip()

                    at = rows[row].findAll('td')[2]

                    ca = at.find('span').text.strip()

                    sub_grade[sn] = ca

                sub_grade_all[str(x)]=sub_grade
                all= soup.findAll('div', {'class': 'form-group col-md-4'})[1]
                sgpa[str(x)]= all.find('span',{'id':'MainContent_lblsgpa'}).text.strip()

                all = soup.findAll('div', {'class': 'form-group col-md-4'})[2]
                cgpa[str(x)] = all.find('span', {'id': 'MainContent_lblcgpa'}).text.strip()


            ret= {
                'grades':sub_grade_all,
                'sgpa':sgpa,
                'cgpa':cgpa,
                'backlogs':student_backlogs
            }
            json_ret=json.dumps(ret)
            print (json_ret)
            return json_ret


if __name__ == '__main__':
    #app.run(host ='0.0.0.0', port=80)
   
    #app.run()
    app.run(threaded=True, port=5000)