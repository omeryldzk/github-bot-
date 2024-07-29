from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
class Github:
    
    def __init__(self,username,password):
        self.browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        self.base_Url = "https://github.com/"
        self.username = username
        self.password = password  
        self.followers = []
        self.repos = []
    def sign_in(self):
        self.browser.get(self.base_Url)
        sign_in_Btn = self.browser.find_element(By.XPATH ,"/html/body/div[1]/header/div/div[2]/div[2]/div[2]/a")
        sign_in_Btn.click()
        time.sleep(3)
        username_btn = self.browser.find_element(By.ID ,"login_field")
        passwod_btn = self.browser.find_element(By.ID ,"password")
        sign_in_btn2 = self.browser.find_element(By.NAME,"commit")
        time.sleep(1)
        username_btn.send_keys(self.username)
        passwod_btn.send_keys(self.password)
        sign_in_btn2.send_keys(Keys.ENTER)
        time.sleep(2)
        self.__del__()

    def loadRepos(self,repo_name):
        new_url = self.base_Url + self.username+ "/" + repo_name
        self.browser.get(new_url)
        time.sleep(2)
        self.__del__()
    def findRepos(self,keyword):
        self.sign_in()
        search_btn =self.browser.find_element(By.XPATH ,"/html/body/div[1]/header/div[3]/div/div/form/label/input[1]")
        search_btn.send_keys(keyword)
        search_btn.send_keys(Keys.ENTER)
        repos = self.browser.find_element(By.CLASS_NAME,"repo-list").find_elements(By.XPATH,"*")
        repo_num=0
        for repo in repos:
            print(repo_num)
            user_info = repo.find_element(By.CLASS_NAME,"f4").find_element(By.TAG_NAME,"a")
            print(user_info)
            description = repo.find_element(By.CLASS_NAME,"mb-1").text
            username = user_info.text.split("/")[0]
            repo_name = user_info.find_element(By.TAG_NAME,"em").text
            self.repos.append(
                {
                "username" : username,
                "repo-name " : repo_name,
                "description" : description
                }
            )
            repo_num+=1
        print(self.repos)
        self.__del__()
    def get_followers(self): 
        counter_page = 1
        counter_user = 0
        self.base_Url = self.base_Url + self.username+ "/" + "?tab=following"
        self.browser.get("https://github.com/Omeryldzz?tab=following")
        while(True):
            time.sleep(3)
            followers_list = self.browser.find_elements(By.CSS_SELECTOR,".d-table.table-fixed")
            for x in followers_list:
                follower_name=x.find_elements(By.TAG_NAME,"div")[1].find_elements(By.TAG_NAME,"span")
                self.followers.append(
                {
                "name" : follower_name[0].text,
                "username " : follower_name[1].text
               
                }
                )
                counter_user += 1
            time.sleep(2)
            page_btns = self.browser.find_element(By.CLASS_NAME,"pagination").find_elements(By.CSS_SELECTOR,"*")
            next_btn = page_btns[1]
            if(next_btn.get_attribute("href")):
                
                next_btn.click()
                time.sleep(1)
                counter_page+=1
            else:
                break
            print("{} user on {} page".format(counter_user,counter_page))
            self.__del__()
    def loadFollowers(self):
        self.get_followers()
        print(self.followers)
        self.__del__()
    def __del__(self):
        time.sleep(2)
        self.browser.close()
        
g = Github("Username","password")
# g.sign_in()
g.findRepos("Python")
# g.get_followers()
