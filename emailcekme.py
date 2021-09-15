from selenium import webdriver
import time,openpyxl,threading
from selenium.webdriver.chrome.options import Options

tripadvisorlink = input("Linki yapıştır: ")

wb = openpyxl.Workbook()
sheet = wb.active
c1 = sheet.cell(row = 1, column = 1)
c1.value = "Website"
c2 = sheet.cell(row= 1 , column = 2)
c2.value = "Email"

options = webdriver.ChromeOptions()
options.add_argument('--disable-notifications')
options.add_extension(r"C:\Users\Goaltesting IT\Desktop\Botlar\Emailcekme\adblock.crx")
driver = webdriver.Chrome(executable_path=r"C:\Users\Goaltesting IT\Desktop\Botlar\Emailcekme\chromedriver.exe",chrome_options=options)
driver.get(tripadvisorlink)
time.sleep(3)
#adbloker yüklenir. adblocker olmazsa yeni bir sayfa açar ve geri dönemezsin baştan başlatmak gerekir.
driver.switch_to.window(driver.window_handles[1])
time.sleep(1)
driver.close()
driver.switch_to.window(driver.window_handles[0])
time.sleep(3)
#cookie
driver.find_element_by_xpath("//*[@id='_evidon-accept-button']").click()
time.sleep(2)
#show more
driver.find_element_by_xpath('//*[@id="component_48"]/div/div[2]/div[2]/div[5]').click()
time.sleep(2)
#Choises
try:
    driver.find_element_by_xpath('//*[@id="component_48"]/div/div[2]/div[2]/div[2]/div/label/div/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="component_48"]/div/div[2]/div[2]/div[3]/div/label/div/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="component_48"]/div/div[2]/div[2]/div[4]/div/label/div/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="component_48"]/div/div[2]/div[2]/div[5]/div/label/div/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="component_48"]/div/div[2]/div[2]/div[6]/div/label/div/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="component_48"]/div/div[2]/div[2]/div[7]/div/label/div/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="component_48"]/div/div[2]/div[2]/div[8]/div/label/div/span').click()
    time.sleep(2)
except:
    pass
toplamsayi = driver.find_element_by_xpath('//*[@id="component_36"]/div[1]/div[1]/div/span[1]/span/span').text

sayfasayisi = int((int(toplamsayi)-50)/30)
#İlk sayfanın xpath i farklı olduğu için 2.sayfadan başlıyor!
driver.find_element_by_xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a').click()
time.sleep(3)
listx = []
try:
    #ortalama sayfa sayısı
    for i in range(int(sayfasayisi)):
        print(i)
        x= 0
        #1 sayfada 30 restorant var ama 36 xpath var
        while x<=36:
            x+=1
            #restorant click
            try:
                driver.find_element_by_xpath('//*[@id="component_2"]/div/div['+str(x)+']/span/div[1]/div[2]/div[1]/div/span/a').click()
                time.sleep(3)
                #sekme 2 ye geçiş
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(2)
                try:
                    sitex = driver.find_element_by_link_text("Website").get_attribute('href')
                except:
                    sitex = "Yok"
                try:
                    emailx = driver.find_element_by_link_text("Email").get_attribute('href')
                except:
                    emailx = "Yok"
                time.sleep(1)
                driver.close()
                time.sleep(1)
                #sekme 1 e geçiş
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
                listx.extend([[sitex,emailx]])
                print(sitex,emailx)
            except:
                pass
        #Sonraki sayfa
        driver.find_element_by_xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a[2]').click()
        time.sleep(5)

        
except:
    pass
#Excel e yazdırılan alan bu
try:
    a=-1
    while a<int(toplamsayi)-50:
        a+=1  
        c3 = sheet.cell(row = a+2, column = 1)
        c3.value = str(listx[a][0])
        c4 = sheet.cell(row= a+2 , column = 2)
        c4.value = str(listx[a][1][7:-10])
except:
    pass
outf = tripadvisorlink[47:-5]+".xlsx"
wb.save(outf)
driver.quit()

