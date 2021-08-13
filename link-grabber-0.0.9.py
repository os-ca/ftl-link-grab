import subprocess, platform, json, time, sys, os, operator, ctypes
from datetime import datetime
from pathlib import Path

try:
    from colorama import init, Fore, Style
    from imap_tools import MailBox
    from bs4 import BeautifulSoup

except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colorama'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'imap_tools'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4'])
bot_version = "0.0.9c"
# Initializing Colorama || Utils
init(convert=True) if platform.system() == "Windows" else init()
print(f"{Fore.CYAN}{Style.BRIGHT}Link Grabber {bot_version}\n")
ctypes.windll.kernel32.SetConsoleTitleW(f"Link Grabber {bot_version}")
cwd = Path(__file__).parents[0]
cwd = str(cwd)

lightblue = "\033[94m"
orange = "\033[33m"

class Logger:
    @staticmethod
    def timestamp():
        return str(datetime.now())[:-7]
    @staticmethod
    def normal(message):
        print(f"{lightblue}[{Logger.timestamp()}] {message}")
    @staticmethod
    def other(message):
        print(f"{orange}[{Logger.timestamp()}] {message}")
    @staticmethod
    def error(message):
        print(f"{Fore.RED}[{Logger.timestamp()}] {message}")
    @staticmethod
    def success(message):
        print(f"{Fore.GREEN}[{Logger.timestamp()}] {message}")

def inits(n):
    global mail_domain, email_folder, email_limit, username, password, timeout
    #if not os.path.exists("Emails to confirm.txt"):
        #Logger.other("Creating Emails to confirm.txt...")
        #open("Emails to confirm.txt", 'w').close()
    with open(f"{cwd}/settings.json", "r") as settings:
        data = json.loads(settings.read())
        mail_domain = data['mail_domain']
        email_folder = data['email_folder_to_search'].upper()
        email_limit = data['amount_of_emails_to_check']
        timeout = data['timeout'] * 1000
        username = data["login"][n]['username']
        password = data["login"][n]['password']
    global detected, success, failed
    detected, success, failed = 0,0,0
 
def save_to_txt(acti):
    with open("./data\Emails to confirm.txt", "a") as success_file:
        success_file.write(f'{acti}\n')
        success_file.close()

def login():
    global email
    Logger.normal("Logging in...")
    try: 
        email = MailBox(f'imap.{mail_domain}.com')
        email.login(username, password, email_folder)
        Logger.normal(f"Credentials: {orange}{username}")
        Logger.success("Logged In!")

    except Exception as e:
        Logger.error(f"Failed to log in! Error : {e}")
        
def logout():
    Logger.normal("Logging out...")
    email.logout()


def get_mail():
    messages = imap.select("INBOX", readonly=False)
    messages = int(messages[0])
    msg_nums = imap.search(None, '(UNSEEN)')
    msg_nums = msg_nums[0].split(b" ")


    pass
if __name__ == "__main__":
    while True:
        print(Style.RESET_ALL)
        print("[1] Run\n[2] View Settings\n[3] Edit Settings\n[4] Exit")
        task = input("Input: ")
        print("\n")
        if task == "1":
            n=0
            max=0
            number = input("Number of emails to check: ")  
            if number.isdigit():
                with open(f"{cwd}/settings.json", "r+") as settings:
                    data = json.loads(settings.read())
                    for logins in data['login']:
                        max=max+1
                    data["amount_of_emails_to_check"] = int(number)
                    settings.seek(0)
                    json.dump(data, settings,indent=4)
                    settings.truncate()
                while n < max:
                    inits(n)
                    login()
                    Logger.normal(f"Checking {orange}{email_limit} emails")
                    global detected, success, failed
                    ctypes.windll.kernel32.SetConsoleTitleW(f"{username} | Emails : {email_limit} | Extracted : {success} | Failed : {str(failed)}")
                    try:
                        for mail in email.fetch(reverse=True, limit=email_limit, bulk=True):
                            if "Finish Activating Your Account" in mail.subject:
                                ctypes.windll.kernel32.SetConsoleTitleW(f"{username} | Emails : {email_limit} | Extracted : {success} | Failed : {str(failed)}")
                                detected +=1
                                soup = BeautifulSoup(mail.html, 'html.parser')
                                for link in soup.find_all('a'):
                                    if operator.contains(link.get('href'), 'https://www.footlocker.ca/user-activation.html?activationToken='):
                                        acti = link.get('href')
                                        success+=1
                                        save_to_txt(acti)
                            else:
                                failed+=1
                                ctypes.windll.kernel32.SetConsoleTitleW(f"{username} | Emails : {email_limit} | Extracted : {success} | Failed : {str(failed)}")
                            
                        logout()
                        Logger.success("Done")
                        n=n+1
    
                    except Exception as e:
                        print(e)
                        continue
            else:
                print("INVALID!!! NUMBERS ONLY WTF??")

        elif task == "2":
            with open(f"{cwd}/settings.json", "r") as settings:
                data = json.loads(settings.read())
                print("Domain: "+data['mail_domain'])
                max=0
                for logins in data['login']:
                    print("Username: "+ logins['username'])
                    max = max+1
                print("\n"+str(max) + " unique emails found")
                input("\nPress any key to go back")
                continue
            
                
        elif task == "3":
            select = input("Edit\n[1] Mail Domain\n[2] Go Back\n")
            if select == "1":
                try:
                    mail_domain = input("Enter Mail Domain: ")
                    with open(f"{cwd}/settings.json", "r+") as settings:
                        obj = json.load(settings)
                        obj["mail_domain"] = mail_domain
                        settings.seek(0)
                        json.dump(obj, settings,indent=4)
                        settings.truncate()
                        print(f"{mail_domain} saved")
                except Exception as e:
                    print(e)
            
            elif select =="2":
                continue

            else:
                print("Invalid")
            
        elif task == "4":
            print("Exiting...")
            time.sleep(1)
            sys.exit()

        else:
            print("Invalid")

                
            
        
