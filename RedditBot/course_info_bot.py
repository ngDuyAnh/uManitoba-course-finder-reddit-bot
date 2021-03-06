import praw
import time
from bs4 import BeautifulSoup
import requests
import easygui
from datetime import datetime

# Const variable
SLEEP_TIME = 10
PRAW_ERROR_TIME_OUT = 10
ERROR_TIME_OUT = 10
TEST_MODE = False

# Redit variable
POST_LIMIT = 120

# File name
FILE_NAME = "botLog.txt"

def run_bot(reddit):
    
    sub = reddit.subreddit("umanitoba").new(limit = POST_LIMIT)   #get the latest posts on the subreddit

    for post in sub: #looping through all the latest posts 
        if ("!find" in post.selftext) and (not post.saved):  # checking if the bot is called in that post and if the bot hasn't already replied 
            reply_post(post)
    #post = reddit.submission(url = "https://www.reddit.com/r/test/comments/hrxbu6/find_comp_2080/")
        post.comments.replace_more(limit=None)
        for comment in post.comments.list(): #looping through all the comments (even replies to other comments)
            if ("!find" in comment.body) and (not comment.saved):
                reply_comment(comment)

            
# not using sub.stream.comments() or sub.stream.submissions() as that will be much more complicated to check for both new comments and posts continuously
# so it is best to do it manually and have the bot run once every certain minutes as the subreddit itself isn't very active


def reply_comment(comment):
    bot_request = comment.body.upper().split("!FIND", 2)[1].strip()  #get only the 2 words after !find which represent the course name & code
    request = bot_request.split(" ")  #separate the course name and code 
    course_name = request[0].strip() 
    course_code = request[1].strip()
    bot_reply = get_info(course_name, course_code)
    comment.reply(bot_reply + "\n\n**BEEP BOP. I'm a bot. You can contact my creator [here](https://www.reddit.com/message/compose?to=CanadianSorryPanda&subject=&message=)**")
    comment.save()  # save the comment so the bot doesn't reply to it multiple times
    testMessage("Reddit Bot - KidHelpline", "Replied to a comment")
    
    # Update log
    log("Replied to a comment")
    
def reply_post(post):
    bot_request = post.selftext.upper().split("!FIND", 2)[1].strip()
    request = bot_request.split(" ")
    course_name = request[0].strip()
    course_code = request[1].strip()
    bot_reply = get_info(course_name, course_code)
    post.reply(bot_reply + "\n\n**BEEP BOP. I'm a bot. You can contact my creator [here](https://www.reddit.com/message/compose?to=CanadianSorryPanda&subject=&message=)**")
    post.save()
    testMessage("Reddit Bot - KidHelpline", "Replied to a post")
    
    # Update log
    log("Replied to a post")
  
  
def login_bot(): 
    
    reddit = praw.Reddit(client_id = "",  
                         client_secret = "",
                         password = "",
                         user_agent = "",
                         username = "")
    return reddit


def get_info(course_name, course_code):
    
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
        
        return (name + "\n\n" + faculty + "\n\n" + credit_hours + "\n\n" + description)
    

def messageBox(title, message):
    easygui.msgbox(message, title = title)

def testMessage(title, message):
    if (TEST_MODE):
        messageBox(title, message)
        
def log(MESSAGE):
    # Append to the log
    FILE_HANDLE = open(FILE_NAME, "a")
    
    # Append the information
    FILE_HANDLE.write(str(datetime.now()) + " " + MESSAGE + "\n")
    

def main():  
    
    # Start the application
    messageBox("Reddit Bot - KidHelpline", "Application start")
    
    while True:
        
        # Local variable dictionary
        reddit = login_bot()
        
        # Starting of the application
        log("Application start")
        
        while True:
            try:
                run_bot(reddit)
                testMessage("Reddit Bot - KidHelpline", "Sleeping")
                time.sleep(SLEEP_TIME) # bot checks for new posts or comments once every 2 minutes
            except praw.exceptions.PRAWException as e:
                log(str(e))
                time.sleep(PRAW_ERROR_TIME_OUT) # rest for 10 minutes if PRAW related error, longer wait-time is fine as the subreddit is not very active
            except Exception as e:
                log(str(e))
                time.sleep(ERROR_TIME_OUT)
                break;
            # if a non-PRAW error occurs then stop the program, if you want to run the bot indefinitely simply replace this line with time.sleep()
        
        # End application
        log("Application end")


if __name__ == "__main__": # for Python interpreter if you want to run the bot from there as a py file
    main()
  
    
main()
