from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
import pandas as pd

ua = UserAgent()
user_agent = ua.random
options = Options()

options.add_argument(f'user-agent={user_agent}')
#options.add_argument('--headless=new')  #İsteğe bağlı olarak kullanılabilir. Tarayıcı açılmadan işlemler arkaplanda yapılacaktır.
driver = webdriver.Chrome(options=options)
driver.maximize_window()
players_data = []

# Sayfayı yükle
driver.get("https://www.sofascore.com/team/football/İstenenTakımLinki") #Hedeflenen takımın sofascore linki
driver.execute_script("document.body.style.zoom='33%'")

# WebDriverWait nesnesini başlat
wait = WebDriverWait(driver, 10)
wait2 = WebDriverWait(driver, 200)
# Sayfanın tam olarak yüklenmesini bekle

wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'fSBPoD')]")))

# Sayfanın en altına kaydırma
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(15)

# Oyuncuların bilgilerini toplama
        
player_links = [player_link.get_attribute('href') for player_link in driver.find_elements(By.XPATH, ".//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'fSBPoD')]//a[contains(@href, '/player/')]")]
for player_link in player_links:
    
    try:
        driver.get(player_link)
        driver.execute_script("document.body.style.zoom='33%'")
        wait2.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'dpRTkT') and contains(@class, 'ihxqpK')]//h2[contains(@class, 'sc-gFqAkR') and contains(@class, 'rPsHj')]")))
        # Göreli XPath kullanarak her bir oyuncunun isim bilgisini al
        try:
            name = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'dpRTkT') and contains(@class, 'ihxqpK')]//h2[contains(@class, 'sc-gFqAkR') and contains(@class, 'rPsHj')]").text
        except NoSuchElementException:
            name = "0"
        # Göreli XPath kullanarak her bir oyuncunun numara bilgisini al
        try:
            team = driver.find_element(By.XPATH, "//div[@class='sc-gFqAkR cDBfTX']").text
        except NoSuchElementException:
            team = "No Team"
        try:
            shirt_no = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-gFqAkR crobRI') and contains(., 'Shirt number')]/following-sibling::div[contains(@class, 'sc-gFqAkR jYYdYz')]").text
        except NoSuchElementException:
            shirt_no = "Unknown"
        try:
            country = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-gFqAkR jYYdYz')]//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'dpRTkT') and contains(@class, 'gnYoAh')]//span").text
        except NoSuchElementException:
            country = "null"
        try:
            position = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'hneMUU')]//div[contains(@class, 'sc-gFqAkR') and contains(@class, 'jYYdYz')]").text
        except NoSuchElementException:
            position = "Unknown"
        try:
            age = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-gFqAkR') and contains(@class, 'jYYdYz') and contains(text(), 'yrs')]").text
        except NoSuchElementException:
            age = "0"    
        try:
            height_not_number = driver.find_element(By.XPATH, ".//div[contains(@class, 'sc-gFqAkR jYYdYz') and contains(text(), 'cm')]").text
        except NoSuchElementException:
            height_not_number = "Unknown"
        try:
            Last_12_Month_Rating = driver.find_element(By.XPATH, ".//span[@class='sc-gFqAkR iwQUfz']").text
        except NoSuchElementException:
            Last_12_Month_Rating = "0"
        try:
            Market_Value = driver.find_element(By.XPATH, ".//div[@class='sc-gFqAkR cQUimj']").text
        except NoSuchElementException:
            Market_Value = "Unknown"
        try:
            This_Season_Match_Numbers = driver.find_element(By.XPATH, "//span[contains(@class, 'sc-gFqAkR hmjzNM') and contains(text(), 'Total played')]/following-sibling::span[1][contains(@class, 'sc-gFqAkR hmjzNM')]").text
        except NoSuchElementException:
            This_Season_Match_Numbers = "No Match"
        try:
            First_11 = driver.find_element(By.XPATH, "//span[contains(@class, 'sc-gFqAkR hmjzNM') and contains(text(), 'Started')]/following-sibling::span[1][contains(@class, 'sc-gFqAkR hmjzNM')]").text
        except NoSuchElementException:
            First_11 = "0"
        try:
            Team_of_the_Week = driver.find_element(By.XPATH, "//span[contains(@class, 'sc-gFqAkR hmjzNM') and contains(text(), 'Team of the week')]/following-sibling::span[1][contains(@class, 'sc-gFqAkR hmjzNM')]").text
        except NoSuchElementException:
            Team_of_the_Week = "0"
        try:
            Goal_The_Season = driver.find_element(By.XPATH, "//span[@class='sc-gFqAkR hmjzNM' and text()='Goals']/following-sibling::span[1][@class='sc-gFqAkR hmjzNM']").text
        except NoSuchElementException:
            Goal_The_Season = "0"
        try:
            xG_This_Season = driver.find_element(By.XPATH, "//span[@class='sc-gFqAkR hmjzNM' and text()='Expected Goals (xG)']/following-sibling::span[1][@class='sc-gFqAkR hmjzNM']").text
        except NoSuchElementException:
            xG_This_Season = "0"
        try:
            Goals_Per_Match = driver.find_element(By.XPATH, "//span[@class='sc-gFqAkR hmjzNM' and text()='Goals per game']/following-sibling::span[1][@class='sc-gFqAkR hmjzNM']").text
        except NoSuchElementException:
            Goals_Per_Match = "0"
        try:
            Saves_Made = driver.find_element(By.XPATH, "//span[contains(@class, 'sc-gFqAkR hmjzNM') and contains(text(), 'Saves made')]/following-sibling::span[1][contains(@class, 'sc-gFqAkR hmjzNM')]").text
        except NoSuchElementException:
            Saves_Made = "0"
        try:
            Goals_Conceded = driver.find_element(By.XPATH, "//span[contains(@class, 'sc-gFqAkR hmjzNM') and preceding-sibling::span[text()='Goals conceded']]").text
        except NoSuchElementException:
            Goals_Conceded = "0"
        try:
            Saves_from_inside = driver.find_element(By.XPATH, "//span[contains(@class, 'sc-gFqAkR hmjzNM') and preceding-sibling::span[text()='Saves from inside box']]").text
        except NoSuchElementException:
            Saves_from_inside = "0"
        try:
            Saves_from_outside = driver.find_element(By.XPATH, "//span[contains(@class, 'sc-gFqAkR hmjzNM') and preceding-sibling::span[text()='Saves from outside box']]").text
        except NoSuchElementException:
            Saves_from_outside = "0"
        try:
            Goals_Conceded_Per_Game = driver.find_element(By.XPATH, "//span[contains(@class, 'sc-gFqAkR hmjzNM') and preceding-sibling::span[text()='Goals conceded per game']]").text  
        except NoSuchElementException:
            Goals_Conceded_Per_Game = "0"
        try:
            Attack = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'evBvUI') and contains(@class, 'fXARVN') and contains(@class, 'attacking')]//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'dpRTkT') and contains(@class, 'fXARVN')]//div[contains(@class, 'sc-gFqAkR') and contains(@class, 'jIACKX')]").text
        except NoSuchElementException:
            Attack = "Unknown"
        try:
            Technical = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'evBvUI') and contains(@class, 'fXARVN') and contains(@class, 'technical')]//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'dpRTkT') and contains(@class, 'fXARVN')]//div[contains(@class, 'sc-gFqAkR') and contains(@class, 'jIACKX')]").text
        except NoSuchElementException:
            Technical = "Unknown"
        try:
            Creativity = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'evBvUI') and contains(@class, 'fXARVN') and contains(@class, 'creativity')]//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'dpRTkT') and contains(@class, 'fXARVN')]//div[contains(@class, 'sc-gFqAkR') and contains(@class, 'jIACKX')]").text
        except NoSuchElementException:
            Creativity = "Unknown"
        try:
            Tactical = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'evBvUI') and contains(@class, 'fXARVN') and contains(@class, 'tactical')]//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'dpRTkT') and contains(@class, 'fXARVN')]//div[contains(@class, 'sc-gFqAkR') and contains(@class, 'jIACKX')]").text
        except NoSuchElementException:
            Tactical = "Unknown"
        try:
            Defending = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'evBvUI') and contains(@class, 'fXARVN') and contains(@class, 'defending')]//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'dpRTkT') and contains(@class, 'fXARVN')]//div[contains(@class, 'sc-gFqAkR') and contains(@class, 'jIACKX')]").text
        except NoSuchElementException:
            Defending = "Unknown"
        try:
            Save = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'evBvUI') and contains(@class, 'fXARVN') and contains(@class, 'saves')]//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'dpRTkT') and contains(@class, 'fXARVN')]//div[contains(@class, 'sc-gFqAkR') and contains(@class, 'jIACKX')]").text
        except NoSuchElementException:
            Save = "Unknown"
        try:
            Aerial = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'evBvUI') and contains(@class, 'fXARVN') and contains(@class, 'aerial')]//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'dpRTkT') and contains(@class, 'fXARVN')]//div[contains(@class, 'sc-gFqAkR') and contains(@class, 'jIACKX')]").text
        except NoSuchElementException:
            Aerial= "Unknown"
        try:
            Anticipation = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'evBvUI') and contains(@class, 'fXARVN') and contains(@class, 'anticipation')]//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'dpRTkT') and contains(@class, 'fXARVN')]//div[contains(@class, 'sc-gFqAkR') and contains(@class, 'jIACKX')]").text
        except NoSuchElementException:
            Anticipation = "Unknown"
        try:
            Ball_Distribution = driver.find_element(By.XPATH, "//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'evBvUI') and contains(@class, 'fXARVN') and contains(@class, 'ballDistribution')]//div[contains(@class, 'sc-fqkvVR') and contains(@class, 'sc-dcJsrY') and contains(@class, 'dpRTkT') and contains(@class, 'fXARVN')]//div[contains(@class, 'sc-gFqAkR') and contains(@class, 'jIACKX')]").text
        except NoSuchElementException:
            Ball_Distribution = "Unknown"
        players_data.append({
            'Name': name,
            'Team' : team,
            'Number': shirt_no,
            'Nationality': country,
            'Position' : position,
            'Height' : height_not_number,
            'Last 12 Month Rating' : Last_12_Month_Rating,
            'Market Value' : Market_Value,
            'Total Played This Season' : This_Season_Match_Numbers,
            'Started Matchs Number' : First_11,
            'Team Of The Week' : Team_of_the_Week,
            'Goals' : Goal_The_Season,
            'Expected Goals (xG)' : xG_This_Season,
            'Goals Per Match' : Goals_Per_Match,
            'Saves' : Saves_Made,
            'Goals Conceded' : Goals_Conceded,
            'Goals Conceded Per Game' : Goals_Conceded_Per_Game,
            'Saves from Inside' : Saves_from_inside,
            'Saves from Outside' : Saves_from_outside,
            'Attack (/100)' : Attack,
            'Technical (/100)' : Technical,
            'Creativity (/100)' : Creativity,
            'Tactical (/100)' : Tactical,
            'Defending (/100)' : Defending,
            'Save (/100)' : Save,
            'Aerial Balls (/100)' : Aerial,
            'Anticipation (/100)' : Anticipation,
            'Ball Distribution (/100)' : Ball_Distribution
        })
        driver.execute_script("document.body.style.zoom='33%'")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
# WebDriver'ı kapatma
driver.quit()

# Pandas DataFrame oluşturma
df_players = pd.DataFrame(players_data)
# DataFrame'i CSV dosyasına kaydetme
csv_file_path = 'Hedef Dizin' #Kaydetmek istenilen dizin, dosya adı ve uzantısı
df_players.to_csv(csv_file_path, index=False, encoding='utf-8')
print("CSV dosyası başarıyla kaydedildi:", csv_file_path)