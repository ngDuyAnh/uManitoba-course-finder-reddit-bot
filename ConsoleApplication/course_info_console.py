from bs4 import BeautifulSoup
import requests

def get_info(course_name, course_code):
    
    # Make the course_name upper case
    course_name = course_name.upper()
    
    url = "http://crscalprod.ad.umanitoba.ca/Catalog/ViewCatalog.aspx?pageid=viewcatalog&topicgroupid=27309&entitytype=CID&entitycode=" + course_name + "+" + course_code  #get the database for the course name
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    
    text_td = soup.find_all("td", class_ = "courseValueCell")  # get all course names from the website
    
    if not text_td: # if empty, this means the course name doesn't exist 
        return "Sorry, I couldn't find the course you were looking for :("
    
    else:
        name = "*Course name:* " + text_td[2].text
        faculty = "*Faculty:* " + text_td[4].text
        credit_hours = "*Credit hours:* " + text_td[1].text
        description  = "*Description:* " + text_td[3].text
        
        return (name + "\n" + faculty + "\n" + credit_hours + "\n" + description)
    

def main():
    # Starting the application
    print("Application start.")
    
    # Keep getting the course identification and print the information of the course
    while (True):
        try:
            courseSearch = input("Course: ")
            
            # Split into course name and number
            courseSearch = courseSearch.split(" ")
            courseName = courseSearch[0]
            courseNum = courseSearch[1]
            
            # Get the course detail
            courseInfo = get_info(courseName, courseNum)
            
            # Print the course information
            print(courseInfo, end = "\n\n")
            
        except Exception as e:
            print("Error ", str(e))
            
    # Program terminate
    print("Application terminate, exist ok.")

if __name__ == "__main__": # for Python interpreter if you want to run the bot from there as a py file
    main()
  
    
main()
