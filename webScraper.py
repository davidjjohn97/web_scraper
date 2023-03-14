# Invoking required Libraries
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import re
import pandas as pd
import numpy as np
from random import randint
from random import choice
from random import shuffle

max = 450
limits = np.arange(1, max + 1, 1)

df = pd.read_csv('TARGET_ENDPOINTS_DATA_FILE.csv')
extracted_Endpoints = df[['TARGET']].values
extracted_Endpoints = np.unique(extracted_Endpoints)
extracted_Endpoints = [x - 100000 for x in extracted_Endpoints]

limits = [i for i in limits if i not in extracted_Endpoints]

shuffle(limits)


# column_names = ['Column Names of Table on Website']
column_names = ['TARGET','API_NUM','LATITUDE','LONGITUDE']
df_final = pd.DataFrame(columns = column_names)


# Creating Dictionary
well_plug_info = {'API_NUM':'DATA'}

# Reading Proxy File
with open('list_proxy.txt', 'r') as file:
       proxies = file.readlines()

# Reading User Agent File
with open('user_agent_list.txt', 'r') as file:
       usr_agnts = file.readlines()

# print(usr_agnts)


# Null Counter
null_count = 0

# Iterate through url end points
for i in range(0,len(limits)-1):

    random_usr_agnt = choice(usr_agnts).strip()
    # print(random_usr_agnt)

    # Random Time Delay to mimick human usage and avoid server overload
    time.sleep(randint(0,2))
    start = time.perf_counter()
    target = 100000 + limits[i]
    print(i,target)

# In this case target URL ends with unique numeric values for each respective web page
    
    # Declaring the Target URL
    URL = f'https:targetwebsite{target}'
    ## Creating Headers to mimick Mozilla Browser AND By-passing Captch (N:B - Obtain Cookie info by inspecting web page)
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'Cookie': 'WEBSITE_CAPTCHA=03AIIukzgFenIPmhE-vWZYoJ0S16NVtSQq3meCkFNliBG3OZ94UlQ9H_9Q7ZDZPObVNzUdbTqR2xNjNt-kiCkDv2ugP5kbL5adwTEYLgzewcM0oZr0p7koEoIJ90-uMUP4OpnssMh6T4CVSl4N_0bal2qeE0v0_5ozDoNa5nbkI-7pQMpTtcA29RJthnO_d0w3XOVCKSsPbiJHfwxc0KyXWJOZHzM9PPMVTq2_NBMvzTtKT46YvaliYFJ46h6mPg8nlPTyqO-sgmAo1yozMPX_ox4O2FTao9GQ41rxIcI3W8bRnpD5wp7hmm3n8SIKqy9MltZWsXEmouVL5TFx0gw5kbWHbCgJE7QSpnKWGu7qsGF4Se6Lqb7z6gSt_lfg2E6UGMsGuVXp9osMuk6SvABiNozAOWi5kxZZ-Sc7_wUbx2JKcnevgnZn_ztGoukLz30InXD5m2vs2oRf4r4DT-0fyUJGZ6VQS63YNkIt4i02Zz1q03GcOkvathncpMTuKd3nyZk00BzOFhUmwOjJlxvARljCfstqlARMcEyOzZh_K-Cl_ZT3Fco73-b7nlb1OAlSTvRcaUAsO7lAsqFQHv9CEw0oSoE3SaXt9w',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive',
        'Cookie_Expires': 'False'
    })

    # print(headers)
    # Choose random proxy
    random_proxy = choice(proxies)

    # Setting SERVER Crash results
    results='SERVER OVERLOADED, PLEASE TRY AGAIN LATER.'

    # RE-Fetching until server NOT Overloaded
    while(results=='SERVER OVERLOADED, PLEASE TRY AGAIN LATER.'):
       # Additional Time Delay when server overloaded (N.B - First fetch would be considered to start from OVERLOADED Server)
       time.sleep(randint(0,5))
       #Fetch page
       page = requests.get(URL, headers=headers, proxies={'http': f"http://{random_proxy}"})
       # Parsing html using beautiful soup
       soup = bs(page.content, "html.parser").prettify()

       # Removing Newline charachters
       results = soup.replace("\n", "")

       end = time.perf_counter()
       if(round(end-start, 2) >= 30.00):
            time.sleep(randint(0,10))

    print('.........')

    # REGEX to extract SPECIFIC Data
    data_extract = re.findall(r"REGEX for specific extraction",results)

    if(len(results)!=0):

        # REGEX to extract NUMBER
        num = re.findall(r"<a href=\"cart\?p_apinum=[0-9]+ \">",results)
        
        # REGEX to extract LATLONG
        lat_long = re.findall(r"<th>     LONGITUDE 83    </th>    <th>     LATITUDE 83    [A-Za-z0-9<>./-=\"  -]+<a href=",results)
        lat_long = re.findall('\d*\.?\d+',str(lat_long))

        if((len(api_num)>0) & (len(lat_long)>0)):

              # Format Num and LatLong
              num = int(''.join((re.findall(r"[0-9]",api_num[0]))))
              latitude = lat_long[len(lat_long)-1]
              longitude = float('-'+lat_long[len(lat_long)-2])

              # Converting HTML string to table 
              data_df = pd.read_html(str(data_extract[0]))

              # Adding Key:Value pair to Dictionary
              ## Handling Plug Data with Null Values
              if(len(plug_df[0])==0):
                     null_count+=1
                     data_df = None
              else:
                     data_df=data_df[0]

                     # Copy API Numbers of plugs in same well
                     copy_API= np.full((1,len(data_df)),api_num)
                     data_df.insert(0,'NUM', copy_API[0] )


                     # Copy LATITUDE  of plugs in same well
                     copy_Lat= np.full((1,len(data_df)),latitude)
                     data_df.insert(0,'LATITUDE', copy_Lat[0] )


                     # Copy LONGITUDE of plugs in same well
                     copy_Long= np.full((1,len(data_df)),longitude)
                     data_df.insert(0,'LONGITUDE', copy_Long[0] )


                     # Copy URL End value
                     copy_target= np.full((1,len(data_df)),target)
                     data_df.insert(0,'TARGET', copy_target[0] )

                     # Append to Final Dataframe
                     # df_final = df_final.append(plug_df)
                     df_final = pd.concat([df_final,data_df])
              
              # Add to Data Dictionary
              data_info[api_num]=data_df

    

print("                   WEBSCRAPING Summary                        ")
print("--------------------------------------------------------------")
print("Count of Null Data:",null_count)
print("Count of Infos with Actual Data:",len(data_info))
print("Percentage of Infos with NULL  Data:",(null_count/(null_count+len(data_info)))*100,"%")
print(".\n")
print(".\n")
print(".\n")
print(".\n")
print(".\n")
print("--------------------------------------------------------------")
print("                   Completed Export to CSV                    ")

# Run Write for first run
# df_final.to_csv('sonaris_wells_plugData_TEST.csv')   


df_final.to_csv('scraped_Data.csv', mode='a', index=False, header=False)