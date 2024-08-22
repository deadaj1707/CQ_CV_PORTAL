
import streamlit as st
import pandas as pd
import base64,random
import time,datetime
#libraries to parse the resume pdf files
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos,software_course,finance_quant_course,consulting_course,core_electrical_electronics_course,product_dev_course
# import pafy 
import plotly.express as px 
import nltk
nltk.download('stopwords')
import os
import time

# import pafy
# os.environ["PAFY_BACKEND"] = "internal"
 
# nltk
# spacy==2.3.5


# def fetch_yt_video(link):
#     video = pafy.new(link)
#     return video.title
import jwt
import time
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"  # Replace with your own secret key

def generate_jwt_token(user_data):
    """Generate a JWT token for the user"""
    payload = {
        "user_id": user_data["id"],
        "username": user_data["username"],
        "exp": datetime.utcnow() + timedelta(minutes=30)  # Token expires in 30 minutes
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token):
    """Decode a JWT token"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
    
def get_table_download_link(df,filename,text)
    
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    # href = f'<a href="data:file/csv;base64,{b64}">Download Report</a>'
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations 🎓**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course





#CONNECT TO DATABASE

connection = pymysql.connect(host='',user='',password='',db='', port=27490 , ssl={'ca': 'certs/ca.pem'})
cursor = connection.cursor()

def insert_data(name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses, drive_link, status, profile):
    DB_table_name = 'user_data'
    status = 0
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (str(name), email, str(res_score), timestamp,str(no_of_pages), reco_field, cand_level, skills,recommended_skills,courses, str(drive_link) , int(status), str(profile))
    cursor.execute(insert_sql, rec_values)
    connection.commit()


def insert_data_reviewers(name,username,pwd, reviewsnum, cvsreviewed):
    DB_table_name = 'reviewer_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%f,%f)"""
    rec_values = (str(name),str(username), str(pwd), int(reviewsnum), int(cvsreviewed))
    cursor.execute(insert_sql, rec_values)
    connection.commit()

st.set_page_config(
   page_title="CQ Resume Portal",
   page_icon='./Logo/logo2.png',
)
def run():
    img = Image.open('./Logo/CQlogo2.png')
    img = img.resize((1000, 300))
    st.image(img)
    st.title("Communiqué - CV Portal")
    st.sidebar.markdown("# Choose User")
    activities = ["User", "Reviewer" ,"Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    link = '[Developed by ©Communiqué](https://www.cqiitkgp.com/)'
    st.sidebar.markdown(link, unsafe_allow_html=True)


    # Create the DB
    db_sql = """CREATE DATABASE IF NOT EXISTS cdc_companion;"""
    cursor.execute(db_sql)

    # Create table
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(500) NOT NULL,
                     Email_ID VARCHAR(500) ,
                     resume_score VARCHAR(8) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Page_no VARCHAR(5) NOT NULL,
                     Predicted_Field BLOB NOT NULL,
                     User_level BLOB NOT NULL,
                     Actual_skills BLOB NOT NULL,
                     Recommended_skills BLOB NOT NULL,
                     Recommended_courses BLOB NOT NULL,
                     drive_link VARCHAR(500) NULL,
                     status_num INT(10) NULL,
                     PRIMARY KEY (ID));
                    """
    
    #for reviewer table
    DB_table_name_reviewer = 'reviewer_data'
    reviewer_table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name_reviewer + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(500) NOT NULL,
                     UserName VARCHAR(30) NOT NULL,
                     Password VARCHAR(30) NOT NULL,
                     ReviewsNumber INT(200) NOT NULL,
                     Cvsreviewed INT(200) NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)
    cursor.execute(reviewer_table_sql)

    create_table_query_forreviwied = """
    CREATE TABLE IF NOT EXISTS reviews_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Email_ID VARCHAR(255),
    Reviewer_Name VARCHAR(255),
    Drive_Link VARCHAR(255),
    Review TEXT
    )
    """

    cursor.execute(create_table_query_forreviwied)
    if choice == 'User':

        name = st.text_input("Enter your Name & Roll No (follow the format):", placeholder="Jhonny Bravo 22XX9999")
        if name:
            name = name.strip();
            nameArray= name.split(' ');
            st.markdown('''<h5 style='text-align: left; color: #021659;'> Select Your CV Here:</h5>''',
                        unsafe_allow_html=True)
            pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
            if pdf_file is not None:
                with st.spinner('Uploading your Resume...'):
                    time.sleep(4)
                save_image_path = './Uploaded_Resumes/'+pdf_file.name
                with open(save_image_path, "wb") as f:
                    f.write(pdf_file.getbuffer())
                show_pdf(save_image_path)
                resume_data = ResumeParser(save_image_path).get_extracted_data()
                if resume_data:
                    ## Get the whole resume data
                    resume_text = pdf_reader(save_image_path)

                    st.header("**Resume Analysis**")
                    st.success("Hello "+ name)
                    st.subheader("**Your Basic info**")
                    try:
                        st.text('Name: '+ nameArray[:-1])
                        st.text('Resume pages: '+str(resume_data['no_of_pages']))
                        
                        
                        
                    except:
                        pass
                    cand_level = ''
                    if len(resume_data['skills']) <= 20:
                        cand_level = "Fresher"
                        st.markdown( '''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''',unsafe_allow_html=True)
                    elif len(resume_data['skills']) <= 40:
                        cand_level = "Intermediate"
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                    elif len(resume_data['skills']) > 40:
                        cand_level = "Experienced"
                        st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)

                    # st.subheader("**Skills Recommendation💡**")
                    ## Skill shows
                    keywords = st_tags(label='### Your Current Skills',
                    text='See our skills recommendation below',
                        value=resume_data['skills'],key = '1  ')

                    ##  keywords
                    ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit']
                    web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                                'javascript', 'angular js', 'c#', 'flask']
                    android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
                    ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
                    uiux_keyword = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']
                    product_keyword = ['product management', 'product development', 'product design', 'market research', 'product strategy']
                    software_keyword = ['software development', 'java', 'c++', 'python', 'software engineering', 'ruby', 'c#', 'javascript']
                    finance_keyword = ['finance', 'quant', 'investment', 'risk management', 'financial analysis', 'hedge fund', 'trading']
                    consulting_keyword = ['consulting', 'business strategy', 'market analysis', 'management consulting', 'operations consulting']
                    core_electrical_keyword = ['electrical engineering', 'electronics', 'circuit design', 'embedded systems', 'vlsi', 'signal processing']
                    
                    
                    recommended_skills = []
                    reco_field = ''
                    rec_course = ''
                    ## Courses recommendation
                    for i in resume_data['skills']:
                        ## Data science recommendation
                        if i.lower() in ds_keyword:
                            print(i.lower())
                            reco_field = 'Data Science'
                            st.success("** Our analysis says you are looking for Data Science Jobs.**")
                            recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
                            recommended_keywords = st_tags(label='### Recommended skills for you.',
                            text='Recommended skills generated from System',value=recommended_skills,key = '2')
                            st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job</h4>''',unsafe_allow_html=True)
                            rec_course = course_recommender(ds_course)
                            break

                        ## Web development recommendation
                        elif i.lower() in web_keyword:
                            print(i.lower())
                            reco_field = 'Web Development'
                            st.success("** Our analysis says you are looking for Web Development Jobs **")
                            recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
                            recommended_keywords = st_tags(label='### Recommended skills for you.',
                            text='Recommended skills generated from System',value=recommended_skills,key = '3')
                            st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                            rec_course = course_recommender(web_course)
                            break

                        ## Android App Development
                        elif i.lower() in android_keyword:
                            print(i.lower())
                            reco_field = 'Android Development'
                            st.success("** Our analysis says you are looking for Android App Development Jobs **")
                            recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
                            recommended_keywords = st_tags(label='### Recommended skills for you.',
                            text='Recommended skills generated from System',value=recommended_skills,key = '4')
                            st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                            rec_course = course_recommender(android_course)
                            break

                        ## IOS App Development
                        elif i.lower() in ios_keyword:
                            print(i.lower())
                            reco_field = 'IOS Development'
                            st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                            recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
                            recommended_keywords = st_tags(label='### Recommended skills for you.',
                            text='Recommended skills generated from System',value=recommended_skills,key = '5')
                            st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                            rec_course = course_recommender(ios_course)
                            break

                        ## Ui-UX Recommendation
                        elif i.lower() in uiux_keyword:
                            print(i.lower())
                            reco_field = 'UI-UX Development'
                            st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                            recommended_skills = ['UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research']
                            recommended_keywords = st_tags(label='### Recommended skills for you.',
                            text='Recommended skills generated from System',value=recommended_skills,key = '6')
                            st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                            rec_course = course_recommender(uiux_course)
                            break
                        
                        elif i.lower() in product_keyword:
                            print(i.lower())
                            reco_field = 'Product Development'
                            st.success("** Our analysis says you are looking for Product Development Jobs **")
                            recommended_skills = ['Product Management', 'Product Design', 'Market Research', 'Product Strategy', 'Agile Methodologies', 'Scrum', 'User Research']
                            recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                        text='Recommended skills generated from System', value=recommended_skills, key='7')
                            st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost🚀 the chances of getting a Job</h4>''', unsafe_allow_html=True)
                            rec_course = course_recommender(product_dev_course)
                            break

                        elif i.lower() in software_keyword:
                            print(i.lower())
                            reco_field = 'Software Development'
                            st.success("** Our analysis says you are looking for Software Development Jobs **")
                            recommended_skills = ['Software Engineering', 'Java', 'C++', 'Python', 'Ruby', 'C#', 'JavaScript', 'Agile Development', 'Scrum']
                            recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                        text='Recommended skills generated from System', value=recommended_skills, key='8')
                            st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost🚀 the chances of getting a Job</h4>''', unsafe_allow_html=True)
                            rec_course = course_recommender(software_course)
                            break

                        elif i.lower() in finance_keyword:
                            print(i.lower())
                            reco_field = 'Finance and Quant'
                            st.success("** Our analysis says you are looking for Finance and Quant Jobs **")
                            recommended_skills = ['Financial Analysis', 'Investment Management', 'Risk Management', 'Quantitative Analysis', 'Hedge Funds', 'Trading', 'Financial Modeling']
                            recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                        text='Recommended skills generated from System', value=recommended_skills, key='9')
                            st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost🚀 the chances of getting a Job</h4>''', unsafe_allow_html=True)
                            rec_course = course_recommender(finance_quant_course)
                            break

                        elif i.lower() in consulting_keyword:
                            print(i.lower())
                            reco_field = 'Consulting'
                            st.success("** Our analysis says you are looking for Consulting Jobs **")
                            recommended_skills = ['Business Strategy', 'Market Analysis', 'Management Consulting', 'Operations Consulting', 'Project Management', 'Data Analysis', 'Client Relations']
                            recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                        text='Recommended skills generated from System', value=recommended_skills, key='10')
                            st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost🚀 the chances of getting a Job</h4>''', unsafe_allow_html=True)
                            rec_course = course_recommender(consulting_course)
                            break

                        elif i.lower() in core_electrical_keyword:
                            print(i.lower())
                            reco_field = 'Core Electrical/Electronics'
                            st.success("** Our analysis says you are looking for Core Electrical/Electronics Jobs **")
                            recommended_skills = ['Circuit Design', 'Embedded Systems', 'VLSI', 'Signal Processing', 'Microcontrollers', 'PCB Design', 'Analog and Digital Electronics']
                            recommended_keywords = st_tags(label='### Recommended skills for you.',
                                                        text='Recommended skills generated from System', value=recommended_skills, key='11')
                            st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding these skills to your resume will boost🚀 the chances of getting a Job</h4>''', unsafe_allow_html=True)
                            rec_course = course_recommender(core_electrical_electronics_course)
                            break
                    
                    ## Insert into table
                    ts = time.time()
                    cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    timestamp = str(cur_date+'_'+cur_time)

                    ### Resume writing recommendation
                    st.subheader("**Resume Tips & Ideas💡**")
                    resume_score = 0
                    if 'POSITIONS OF RESPONSIBILITY' in resume_text:
                        resume_score = resume_score+20
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Position of Responsibility</h4>''',unsafe_allow_html=True)
                    else:
                        st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add your Positions of Responsibility, in case if you have any to improve your CV.</h4>''',unsafe_allow_html=True)

                    if 'EDUCATION'  in resume_text:
                        resume_score = resume_score + 20
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Education</h5>''',unsafe_allow_html=True)
                    else:
                        st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Education. This is very important as you are required to mention this in your CV/Resume.</h4>''',unsafe_allow_html=True)

                    if 'PROJECTS AND INTERNSHIPS' or 'PROJECTS'in resume_text:
                        resume_score = resume_score + 20
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects & Internships</h4>''',unsafe_allow_html=True)
                    else:
                        st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add your Projects & Internships. It will show your experience and how important your work would be to the Recruiters.</h4>''',unsafe_allow_html=True)

                    if 'AWARDS AND ACHIEVEMENTS' in resume_text:
                        resume_score = resume_score + 20
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h5>''',unsafe_allow_html=True)
                    else:
                        st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Achievements. It will show that you are capable for the required position.</h4>''',unsafe_allow_html=True)

                    if 'EXTRACURRICULAR ACTIVITIES' or 'EXTRA CURRICULAR ACTIVITIES' in resume_text:
                        resume_score = resume_score + 20
                        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Extracurricular Activities</h4>''',unsafe_allow_html=True)
                    else:
                        st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Extracurricular Activities. It will show what kind of a person you actually are, and what other skillsets you have in general.</h4>''',unsafe_allow_html=True)

                    st.subheader("**Resume Score📝**")
                    st.markdown(
                        """
                        <style>
                            .stProgress > div > div > div > div {
                                background-color: #d73b5c;
                            }
                        </style>""",
                        unsafe_allow_html=True,
                    )
                    my_bar = st.progress(0)
                    score = 0
                    for percent_complete in range(resume_score):
                        score +=1
                        time.sleep(0.1)
                        my_bar.progress(percent_complete + 1)
                    st.success('** Your Resume Writing Score: ' + str(score)+'**')
                    st.warning("** Note: This score is calculated based on the content that you have in your Resume. **")
                    st.balloons()
                    status = 0
                    email_forfun= "lmao@bmail.com"
                    print(f"Original email: {resume_data.get('email', 'Key not found')}")
                    if 'email' not in resume_data:
                        print("Email key not found in resume_data")
                    elif resume_data['email'] in [None, "NULL"]:
                        print(f"Email is {resume_data['email']}, setting to default email_forfun")
                        resume_data['email'] = email_forfun

                    print(f"Email after check: {resume_data['email']}")


                    insert_data(str(name), resume_data['email'], str(resume_score), timestamp,
                                str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']),
                                str(recommended_skills), str(rec_course), "NULL", status, "NULL")


                    # ## Resume writing video
                    # st.header("**Bonus Video for Resume Writing Tips💡**")
                    # resume_vid = random.choice(resume_videos)
                    # res_vid_title = fetch_yt_video(resume_vid)
                    # st.subheader("✅ **"+res_vid_title+"**")
                    # st.video(resume_vid)



                    # ## Interview Preparation Video
                    # st.header("**Bonus Video for Interview Tips💡**")
                    # interview_vid = random.choice(interview_videos)
                    # int_vid_title = fetch_yt_video(interview_vid)
                    # st.subheader("✅ **" + int_vid_title + "**")
                    # st.video(interview_vid)

                    st.markdown(
                    """
                    <h1>Would you like to get your CV Reviewed by a senior?</h1><br>
                    <h2>Please fill the following form below</h2>
                    <h6>Note: You will be allowed a single CV for Review only</h6>
                    """, 
                    unsafe_allow_html=True
                    )

                    #set the name later , ive forgotten
                    fetch_status_query = "SELECT status_num FROM user_data WHERE Name = %s"
                    cursor.execute(fetch_status_query, (name,))
                    status_row = cursor.fetchone()
                    profileList = ['Data', 'Software', 'Consult', 'Finance-Quant', 'Product', 'FMCG']
                    # Check if the status is NULL or not set
                    if status_row is None or status_row[0] == 0:
                        st.write("( Make sure you have provided access to your CV in the drive link )")
                        email_input = st.text_input("Enter your Email here: ")
                        drive_link = st.text_input("Enter your Drive Link: ")
                        profile = st.selectbox("Enter the profile you are targetting", profileList)
                        if st.button("Submit"):
                            if email_input and drive_link:  # Check if email and drive link are provided
                                # Update the email, drive_link, and status in the database
                                update_query = """
                                UPDATE user_data
                                SET Email_ID = %s, drive_link = %s, status_num = 1, profilez = %s
                                WHERE Name = %s
                                """
                                cursor.execute(update_query, (email_input, drive_link, profile, name))
                                connection.commit()
                                st.success("Information updated successfully!")
                            else:
                                st.error("Please provide both email and drive link.")
                    else:
                        st.write("Sorry, you've already submitted your CV for review.")
                

                #trying out the drive link updation ffs
                
                

                
    elif choice == 'Admin':
        ## Admin Side
        st.success('Welcome to Admin Side')
        # st.sidebar.subheader('**ID / Password Required!**')

        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.button('Login'):
            if ad_user == 'sujay' and ad_password == 'sujay123':
                st.success("Welcome Bruh !")
                # Display Data
                cursor.execute('''SELECT * FROM user_data''')
                data = cursor.fetchall()
                st.header("**User's Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                                                 'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
                                                 'Recommended Course', 'drive_link','status_num','profilez'])
                st.dataframe(df)
                st.markdown(get_table_download_link(df,'User_Data.csv','Download Report'), unsafe_allow_html=True)
                ## Admin Side Data
                query = 'select * from user_data;'
                plot_data = pd.read_sql(query, connection)

                # ## Pie chart for predicted field recommendations
                # labels = plot_data.Predicted_Field.unique()
                # print(labels)
                # values = plot_data.Predicted_Field.value_counts()
                # print(values)
                # st.subheader("**Pie-Chart for Predicted Field Recommendation**")
                # fig = px.pie(df, values=values, names=labels, title='Predicted Field according to the Skills')
                # st.plotly_chart(fig)

                # ### Pie chart for User's👨‍💻 Experienced Level
                # labels = plot_data.User_level.unique()
                # values = plot_data.User_level.value_counts()
                # st.subheader("**Pie-Chart for User's Experienced Level**")
                # fig = px.pie(df, values=values, names=labels, title="Pie-Chart📈 for User's👨‍💻 Experienced Level")
                # st.plotly_chart(fig)

                cursor.execute('''SELECT * FROM reviewer_data''')
                data = cursor.fetchall()
                st.header("**Reviewer's Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'UserName', 'Password', 'ReviewsNumber', 'Cvsreviewed', 'Rprofilez'])
                st.dataframe(df)
                st.markdown(get_table_download_link(df,'User_Data.csv','Download Report'), unsafe_allow_html=True)
                ## Admin Side Data
                # query = 'select * from _data;'

                cursor.execute('''SELECT * FROM reviews_data''')
                data = cursor.fetchall()
                st.header("**Reviews Data**")
                df = pd.DataFrame(data, columns=['id', 'Name', 'Email_ID', 'Reviewer_Name', 'Drive_link', 'Review'])
                st.dataframe(df)
                st.markdown(get_table_download_link(df,'User_Data.csv','Download Report'), unsafe_allow_html=True)

            else:
                st.error("Wrong ID & Password Provided")
    else:
        #Reviewer Side of the page:
        def reviewer_login():
            if 'logged_in' not in st.session_state:
                st.session_state['logged_in'] = False

            if not st.session_state['logged_in']:
                st.success('Welcome to the Reviewers Side')
                ad_user = st.text_input("Username")
                ad_password = st.text_input("Password", type='password')

                if st.button('Login'):
                    cursor.execute("SELECT ID, UserName, Password FROM reviewer_data WHERE UserName = %s", (ad_user,))
                    row = cursor.fetchone()
                    if row and (ad_password == row[2]):
                        user_data = {
                            "id": row[0],
                            "username": row[1]
                        }
                        token = generate_jwt_token(user_data)
                        st.session_state['token'] = token
                        st.session_state['logged_in'] = True
                        st.session_state['ad_user'] = ad_user
                        st.success(f"Welcome {ad_user}!")
                    else:
                        st.error("Invalid username or password")
            else:
                display_review_section(st.session_state['ad_user'], st.session_state['token'])

        # Function to display the review section
        def display_review_section(ad_user):
            if st.button('Logout'):
                st.session_state['logged_in'] = False
                st.experimental_rerun()


            cursor.execute("SELECT ReviewsNumber, Cvsreviewed, Rprofilez FROM reviewer_data WHERE UserName = %s", (ad_user,))
            cvnums = cursor.fetchone()

            if cvnums:
                ReviewsNumber = cvnums[0]
                Cvsreviewed = cvnums[1]
                reviewerProfile = cvnums[2]
                st.markdown(
                    f"""
                    <h3>Number of CVs Left to be Reviewed: <span style='color:blue;'>{ReviewsNumber - Cvsreviewed}</span></h3>
                    <h3>Number of CVs Reviewed: <span style='color:green;'>{Cvsreviewed}</span></h3>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error("User not found or no data available.")

            query = """
            SELECT DISTINCT Email_ID, Name, drive_link 
            FROM user_data 
            WHERE status_num = 1 AND profilez = %s
            LIMIT 5;
            """
            cursor.execute(query,(reviewerProfile,))
            cvsList = cursor.fetchall()

            st.success('Hello '+ ad_user);

            cv_count_query = "SELECT COUNT(*) FROM user_data WHERE status_num = 1;"
            cursor.execute(cv_count_query)
            cv_count = cursor.fetchone()[0]
            cv_display_count = min(5, cv_count)

            display_count = len(cvsList)
            st.write(f"Displaying {display_count}/{ReviewsNumber - Cvsreviewed} CVs left to be reviewed")

            if len(cvsList) ==0 :
                st.success("Currently, there are no more available cvs to be reviewed. Do come back later to find more.")

            for email_id, name, drive_link in cvsList[:cv_display_count]:
                st.image('./Logo/CVlogo.png', width=150)
                st.write(f"Name: {name}")
                st.write(f"Email: {email_id}")
                st.markdown(f"[Drive Link]({drive_link})")

                
                # st.markdown(js_alert, unsafe_allow_html=True)
                # Use a form to handle the review submission
                with st.form(key=f"form_{name}"):
                    review = st.text_area(f"Review for {name}", height=100, key=f"review_{name}")
                    submit_button = st.form_submit_button(label=f"Submit Review for {name}")

                    if submit_button:
                        
                            word_count = len(review.split())
                        # if word_count < 50:
                        #     st.error("The review must be at least 50 words long.")
                        # else:
                            update_review_query = "UPDATE user_data SET status_num = 2 WHERE Email_ID = %s AND Name = %s;"
                            cursor.execute(update_review_query, (email_id, name))
                            connection.commit()

                            # Insert the review into the done_reviews table
                            insert_review_query = """
                            INSERT INTO reviews_data (Name, Email_ID, Reviewer_Name, Drive_Link, Review)
                            VALUES (%s, %s, %s, %s, %s)
                            """
                            cursor.execute(insert_review_query, (name, email_id, ad_user, drive_link, review))
                            connection.commit()

                            update_reviewer_query = """
                            UPDATE reviewer_data 
                            SET Cvsreviewed = Cvsreviewed + 1 
                            WHERE UserName = %s
                            """
                            cursor.execute(update_reviewer_query, (ad_user,))
                            connection.commit()

                            st.success(f"Review for {name} submitted successfully!")
                            #make a deloay of 5seconds here.
                            # Remove the reviewed CV from the list
                            time.sleep(5)
                            cvsList = [cv for cv in cvsList if cv[0] != email_id]
                            st.experimental_rerun()

                        
        reviewer_login()


run()



#proflie wise distribution!!!!!!
#Change theme little
