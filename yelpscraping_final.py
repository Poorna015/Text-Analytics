import urllib2
import requests
import re
import unicodedata
from bs4 import BeautifulSoup

#Read the files in the Assignment data folder from 1 to 1000
for file in range(1,1001,1):
    page_name = "file:///C:/Users/gorapalp/Desktop/Python/DC/assignmentData" + str(file) + ".html"
    print file
    page =urllib2.urlopen(page_name)
    soup = BeautifulSoup(page,"lxml")

#Create Dictionary object and assign spaces to all Keys
    dict_name = "dict" + str(file)
    dict_name = {}
    
    dict_name['Accepts Apple Pay']= ''
    dict_name['Accepts Android Pay']= ''
    dict_name['Accepts Bitcoin']= ''
    dict_name['Alcohol']=''
    dict_name['Noise Level']= ''
    dict_name['Gender Neutral Restrooms']= ''
    dict_name['Has TV']= ''
    dict_name['Attire']= ''
    dict_name['Ambience']= ''
    dict_name['Good for Kids']= ''
    dict_name['Good for Groups']= ''
    dict_name['Wheelchair Accessible']= ''
    dict_name['Caters']= ''
    dict_name['Delivery']= ''
    dict_name['Accepts Credit Cards']= ''
    dict_name['Take-out']= ''
    dict_name['Outdoor Seating']= ''
    dict_name['Takes Reservations']= ''
    dict_name['Waiter Service']= ''
    dict_name['Wi-Fi']= ''
    dict_name['Bike Parking']= ''
    dict_name['Good For']= ''
    dict_name['Parking']= ''
    dict_name['Business_url']= ''
    dict_name['Business_email']= ''
    dict_name['Business_phone']= ''
    dict_name['Business_address']=''
    dict_name['Opening_hours']=''
    dict_name['Contact_us']=''
    
#Read Business name value from the webpage
    name = soup.find("h1")
    temp= name.text.strip()
    nfkd_form = unicodedata.normalize('NFKD', temp)
    bus_name = nfkd_form.encode('ascii', 'ignore')
    dict_name['Business_name']=bus_name

#Read Business phone value from the webpage    
    phone = soup.find("span",class_="biz-phone")
    if phone:
        dict_name['Business_phone']= phone.text.strip()
        
#Read Business url from the webpage
    website_dt = soup.find("span",class_="biz-website js-add-url-tagging")
    if website_dt:
        website_coll= website_dt.text.split('\n')
        if len(website_coll) >0:
            website_nm = website_dt.find("a").get('href')
            url_text=urllib2.unquote(website_nm).decode('utf8') 
            url_temp = url_text.split("url=") 
            url_temp2 = url_temp[1].split("&")
            url_final = str(url_temp2[0])
            dict_name['Business_url']=url_final
        
#Read Business address from the webpage        
    address = soup.find("address")
    if address:
        dict_name['Business_address'] = address.text.strip()
        
#Read more business info from the webpage
    short_list = soup.find("div",class_="short-def-list")
    if short_list:
        dl_items = short_list.find_all("dt", class_="attribute-key")
        for dl in dl_items:
            dict_name[dl.text.strip()] = dl.find_next_sibling("dd").text.strip()
            
#Read opening hours data from the webpage
    hours_table =soup.find("table",class_="table table-simple hours-table")
    text = ""
    if hours_table:
        for row in hours_table.find_all("tr")[0:]:
            if row.th:
                thead= row.find("th").get_text().strip()
                tdata= row.find("td").get_text().strip()
                text = text + thead+ ":" +tdata+ " "
        dict_name["Opening_hours"]=text
 
#Read email id from the Business URL
    if website_dt:
        if len(website_coll) >0:
            try:            
                req1 = requests.get(url_final)
                data1 =req1.text
                soup1 = BeautifulSoup(data1,"lxml")
                new_url =''
#Retrieve contact us page url
                links=soup1.find_all("a",href=True)
                for link in links:
                    if 'contact' in link.text.lower():
                        if '.com' in link.get('href'):
                            new_url = link.get('href')
                            dict_name['Contact_us']=new_url
       
                email_list=re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",data1)

#If email id is available in the home page:               
                if len(email_list) > 0:
                    dict_name["Business_email"] = email_list[0]
#If email id is not available in the home page, try opening the contact us link
                else:
                    try:        
                        if '.com' in new_url:   
                            req2 = requests.get(new_url)
                            data2 =req2.text
                            soup2 = BeautifulSoup(data2,"lxml")
#Retrieving the email id information from contact us page           
                            email_list1=re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",data2)
                                       
                            if len(email_list1) > 0:
                                dict_name["Business_email"] = email_list1[0]
                              
                    except:
                        print "unable to open contact page"
            except:
                    print "no mail"
    str1 = dict_name['Business_name'] +"\t"+dict_name['Business_phone']+"\t"+dict_name['Business_url']+"\t"+dict_name['Business_address']+"\t" +dict_name['Business_email']+"\t"+dict_name['Contact_us']+"\t"+dict_name["Opening_hours"]+"\t"+dict_name['Accepts Apple Pay']+"\t"+dict_name['Alcohol']+"\t"+dict_name['Noise Level']+"\t"+dict_name['Gender Neutral Restrooms']+"\t"+dict_name['Has TV']+"\t"+dict_name['Attire']+"\t"+dict_name['Ambience']+"\t"+dict_name['Good for Kids']+"\t"+dict_name['Good for Groups']+"\t"+dict_name['Wheelchair Accessible']+"\t"+dict_name['Caters']+"\t"+dict_name['Delivery']+"\t"+dict_name['Accepts Credit Cards']+"\t"+dict_name['Accepts Android Pay']+"\t"+dict_name['Accepts Bitcoin']+"\t"+dict_name['Take-out']+"\t"+dict_name['Outdoor Seating']+"\t"+dict_name['Takes Reservations']+"\t"+dict_name['Waiter Service']+"\t"+dict_name['Wi-Fi']+"\t"+dict_name['Bike Parking']+"\t"+dict_name['Good For']+"\t"+dict_name['Parking']+"\t"+str(file) + "\n"

    try:
        if file == 1:
            file1 = open("C:\\Users\\gorapalp\\Desktop\\Python\\DC\\assignmentData\\result.tsv","w")
            heading = 'Business_name' +"\t"+'Business_phone'+"\t"+'Business_url'+"\t"+'Business_address'+"\t" +'Business_email'+"\t"+'Contact_us'+"\t"+'Opening_hours'+"\t"+'Accepts Apple Pay'+"\t"+'Alcohol'+"\t"+'Noise Level'+"\t"+'Gender Neutral Restrooms'+"\t"+'Has TV'+"\t"+'Attire'+"\t"+'Ambience'+"\t"+'Good for Kids'+"\t"+'Good for Groups'+"\t"+'Wheelchair Accessible'+"\t"+'Caters'+"\t"+'Delivery'+"\t"+'Accepts Credit Cards'+"\t"+'Accepts Android pay'+"\t"+'Accepts Bitcoin'+"\t"+'Take-out'+"\t"+'Outdoor Seating'+"\t"+'Takes Reservations'+"\t"+'Waiter Service'+"\t"+'Wi-Fi'+"\t"+'Bike Parking'+"\t"+'Good For'+"\t"+'Parking'+"\t"+ "\n"
            file1.write(heading+"\n")
            file1.write(str1+ "\n")
            file1.close()
        else:
            file1 = open("C:\\Users\\gorapalp\\Desktop\\Python\\DC\\assignmentData\\result.tsv","a")
            file1.write(str1+ "\n")
            file1.close()             
    except:
        print str(file) + "unable to scrape"     
        