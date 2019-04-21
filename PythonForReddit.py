import praw
from enum import Enum
import os
from prawcore import NotFound
import datetime
import xml.dom.minidom
import sys

#https://www.geeksforgeeks.org/print-colors-python-terminal/
#https://stackoverflow.com/questions/2330245/python-change-text-color-in-shell
def hilite(string, color, bold=False):
    attr = []
    if color.value == Color.Green.value:
        attr.append('32')
    elif color.value == Color.Red.value:
        attr.append('31')
    elif color.value == Color.Orange.value:
        attr.append('33')
    elif color.value == Color.Grey.value:
        attr.append('30')
    elif color.value == Color.White.value:
        attr.append('29')
    elif color.value == Color.Blue.value:
        attr.append('94')
    elif color.value == Color.Purple.value:
        attr.append('35')
    if bold:
        attr.append('1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

class Option(Enum):
    MyStats = 1
    Preferences = 2
    Random = 3
    SearchSub = 4
    Top10 = 5
    SearchUser = 6
    Quit = 10

class Color(Enum):
    Red = 1
    Green = 2
    Orange = 3
    Grey = 4
    White = 5
    Blue = 6
    Purple = 7

def Clear():
    input("Press Enter to continue...")
    ClearWOMessage();

def ClearWOMessage():
    os.system('cls' if os.name == 'nt' else 'clear');

def sub_exists(sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists

def user_exists(username):
    exists = True
    try:
        reddit.redditor(username).link_karma
    except NotFound:
        exists = False
    return exists

def PrintSub(SubName):
    if (SubName != ""):
        try:
            while(True):
                subobj = reddit.subreddit(SubName)
                print("Name                   : %s" % subobj.stream.subreddit.display_name_prefixed)
                print("Description            : %s" % subobj.stream.subreddit.public_description)
                print("Active users           : %s" % subobj.stream.subreddit.active_user_count)
                print("Quarantine             : %s" % subobj.stream.subreddit.quarantine)
                print("Subscribers            : %s" % subobj.stream.subreddit.subscribers)
                print("Subreddit Type         : %s" % subobj.stream.subreddit.subreddit_type)
                print("Created                : %s" % datetime.datetime.fromtimestamp(subobj.stream.subreddit.created))
                print("Advertiser category    : %s" % subobj.advertiser_category)
                print("Over 18                : %s" % subobj.over18)

                if ViewPostAndComments(reddit.subreddit(SubName).hot(limit=10), reddit.subreddit(SubName).hot(limit=10)) == False:
                    break;
        except Exception as e:
            print("Error : %s" % str(e));
    else:
        print("Sub cannot be empty.");

def ViewPostAndComments(SubList1, SubList2):
    var = input("View top 10 hottest posts? (Y/N)")

    if var == "Y":
        i = 1
        for submission in SubList1:
            ViewTop10(submission, i)
            i += 1
    else:
        return False;
    var = input("Enter number for the comments to view.")

    i = 1
    if var.isdigit() and int(var) <= 10 and int(var) >= 0:
        GetToHere = int(var)
        for submission in SubList2:
            if (i == GetToHere):
                ClearWOMessage();
                ViewTop10(submission, i)
                for Comment in submission.comments:
                    PrintComment(Comment)
            i += 1
    else:
        return False;
    Clear();
    return True;


#https://www.2daygeek.com/rtv-reddit-terminal-viewer-a-simple-terminal-viewer-for-reddit/
def PrintComment(Comment, indent=""):
    try:
        print("")

        if (Comment.author == None):
            name = "[deleted]"
        else:
           name = Comment.author.name

        print(hilite("%s%s" % (indent, name), Color.Blue))
        print("%sScore: %d Upvotes: %d Downvotes: %d Controversiality: %d" % (indent, Comment.score, Comment.ups, Comment.downs, Comment.controversiality))
        print("%sMessage          : %s" % (indent, Comment.body))
        print("%sPostdate         : %s" % (indent,datetime.datetime.fromtimestamp(Comment.created_utc)))
        print("%sPermalink        : %s" % (indent,Comment.permalink))

        for Replies in Comment.replies:
            indent += "    "
            PrintComment(Replies, indent)
    except Exception as e:
        print("Error: %s" % str(e));

def ViewTop10(submission, i):
    print("")
    print(hilite("%s.  %s" % (i, submission.title), Color.White, True))
    print("%s" % submission.shortlink)
    print("%s pts" % submission.score)
    sys.stdout.write(hilite("%s " % submission.author, Color.Green, False))
    print(hilite("%s" % submission.subreddit_name_prefixed, Color.Orange))
    

def ViewUserStats(Name):
    redditor_obj = reddit.redditor(Name)
    print("Username       : %s" % redditor_obj.name)
    print("Comment karma  : %s" % redditor_obj.comment_karma)
    print("Link karma     : %s" % redditor_obj.link_karma)
    print("Is Mod         : %s" % redditor_obj.is_mod)
    print("Is Gold        : %s" % redditor_obj.is_gold)
    print("Avatar URL     : %s" % redditor_obj.icon_img)
    print("Cake day       : %s" % datetime.datetime.fromtimestamp(redditor_obj.created_utc))

    var = input("View newest 10 comments? (Y/N)")
        
    if var == "Y":
        for comment in redditor_obj.comments.new(limit=10):
            print("--------------------------------------------------------------------------")
            print("Upvotes         : %d Downvotes: %d, Controversiality: %d" % (comment.ups, comment.downs, comment.controversiality))
            print("Comment         : %s" % comment.body)
            print("Permalink       : %s" % comment.permalink)

doc = xml.dom.minidom.parse("Credentials.xml")

def ReadXML(nodename):
    return doc.getElementsByTagName(nodename)[0].firstChild.data

reddit = praw.Reddit(client_id=ReadXML("client_id"),
    client_secret=ReadXML("client_secret"),
    password=ReadXML("password"),
    user_agent=ReadXML("user_agent"),
    username=ReadXML("username"))

ClearWOMessage();

while(True):
    print(hilite("____   ____.__                                                            ", Color.Orange));
    print(hilite("\   \ /   /|__|  ____  __  _  __  ____  _______                           ", Color.Orange));
    print(hilite(" \   Y   / |  |_/ __ \ \ \/ \/ /_/ __ \ \_  __ \                          ", Color.Orange));
    print(hilite("  \     /  |  |\  ___/  \     / \  ___/  |  | \/                          ", Color.Orange));
    print(hilite("   \___/   |__| \___  >  \/\_/   \___  > |__|                             ", Color.Orange));
    print(hilite("                    \/               \/                                   ", Color.Orange));
    print(hilite("___________                 __________             .___    .___.__   __   ", Color.Orange));
    print(hilite("\_   _____/  ____  _______  \______   \  ____    __| _/  __| _/|__|_/  |_ ", Color.Orange));
    print(hilite(" |    __)   /  _ \ \_  __ \  |       _/_/ __ \  / __ |  / __ | |  |\   __\\", Color.Orange));
    print(hilite(" |     \   (  <_> ) |  | \/  |    |   \\\\  ___/ / /_/ | / /_/ | |  | |  |  ", Color.Orange));
    print(hilite(" \___  /    \____/  |__|     |____|_  / \___  >\____ | \____ | |__| |__|  ", Color.Orange));
    print(hilite("     \/                             \/      \/      \/      \/            ", Color.Orange));
    print(hilite("By: Nicholas Bruno", Color.Green, False));
    print("Made using the Python Reddit API Wrapper (PRAW)")
    print("--------------------------------------------------------------------------")
    print("Select an option:")
    print(" 1. About me.")
    print(" 2. My preferences.")
    print(" 3. Random sub.")
    print(" 4. Search sub.")
    print(" 5. Top hot posts.")
    print(" 6. Search for user.")
    print("10. Quit.")
    print("--------------------------------------------------------------------------")
    var = input("Your choice: ")

    if var.isdigit():
        var = int(var)
        if var == Option.MyStats.value:
            ViewUserStats(reddit.user.me().name)
        elif var == Option.Preferences.value:
            preferences = reddit.user.preferences()
            print("Label NSFW       : %s" % preferences['label_nsfw'])
            print("Include Over 18  : %s" % preferences['search_include_over_18'])
            print("Accept PMs       : %s" % preferences['accept_pms'])
        elif var == Option.Random.value:
            SubName = reddit.random_subreddit(False)
            ClearWOMessage();
            PrintSub(SubName.display_name)
        elif var == Option.SearchSub.value:
            SubName = input("Enter a subreddit name: ")

            if sub_exists(SubName):
                ClearWOMessage();
                PrintSub(SubName)
            else:
               print("Subreddit doesn't exist.")
        elif var == Option.SearchUser.value:
            username = input("Enter a username: ")
            if user_exists(username):
                ClearWOMessage();
                ViewUserStats(username)
            else:
                print("User not found.")

        elif var == Option.Quit.value:
            print("You chose to quit with the '%d' option." % var)
            break
        elif var == Option.Top10.value: 
            ClearWOMessage();
            while(ViewPostAndComments(reddit.front.hot(limit=10), reddit.front.hot(limit=10)) == True):
                no_op = 0
            

        else:
            print("Invalid entry number.")
    else:
       print("Please enter a digit.")
    Clear();