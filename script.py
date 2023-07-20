# 참고한 영상 : https://www.youtube.com/watch?v=ygtOz_14Mhk 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time 

from openpyxl import Workbook

product_code = {'food': 194276, 'household_items': 115573, 'beauty': 176422, 'interior': 184455, 'electronics_digital': 178155, 'home_kitchen': 185569, 'maternity_baby': 221834, 'pet_supplies': 115574, 'toys': 317679, 'automotive': 183960, 'stationery_office': 177195, 'sports': 317678, 'books_music_movies': 317677, 'health_supplements': 305698, 'women_fashion': 186664, 'men_fashion': 186969, 'kids_baby_fashion': 213101, 'unisex_clothing': 502893}


original_list = [
    "food", "household_items", "beauty", "electronics_digital", "home_kitchen",
    "maternity_baby", "pet_supplies", "toys", "automotive", "stationery_office", "sports",
    "books_music_movies", "health_supplements", "women_fashion", "men_fashion",
    "kids_baby_fashion", "unisex_clothing"
]
url_list = [] 
for lis in original_list:
    key = product_code[lis] 
    raw_url = f"https://www.coupang.com/np/categories/{key}?listSize=120&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&page="
    url_list.append(raw_url)

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("authority=" + "www.coupang.com")
options.add_argument("method=" + "GET")
options.add_argument("accept=" + "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
options.add_argument("accept-encoding=" + "gzip, deflate, br")
options.add_argument("user-agent=" + "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36")
options.add_argument("sec-ch-ua-platform=" + "macOS")
options.add_argument("cookie=" + "PCID=31489593180081104183684; _fbp=fb.1.1644931520418.1544640325; gd1=Y; X-CP-PT-locale=ko_KR; MARKETID=31489593180081104183684; sid=03ae1c0ed61946c19e760cf1a3d9317d808aca8b; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; x-coupang-accept-language=ko_KR;")

for name, main_url in zip(original_list, url_list) : 
    print("*" * 50 + " " + f"{name}시작하겠습니다." + " " + "*" * 50)
    
    for i in range(1, 6):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)   
        temp_url = main_url + f"{i}"
        driver.get(temp_url)
        time.sleep(10)
        print("*" * 50 + " " + str(i) + "Page start!" + " " + "*" * 50)

        wb = Workbook()
        ws = wb.create_sheet(name)
        wb.remove_sheet(wb["Sheet"])
        ws.append(["상품명", "가격", "배송기한", "상세URL"]) 

        try :
            product = driver.find_element(By.ID, "productList")
            lis = product.find_elements(By.CLASS_NAME, "baby-product")

            for li in lis:
                try : 
                    product = li.find_element(By.CLASS_NAME, "name").text
                    price = li.find_element(By.CLASS_NAME, "price-value").text
                    delivery = li.find_element(By.CLASS_NAME, "delivery").text
                    product_url = li.find_element(By.CLASS_NAME, "baby-product-link").get_attribute("href")
                    ws.append([product, price, delivery, product_url])
                    print("product : ", product)
                    print("price : ", price)
                    print("delivery : ", delivery)
                    print("url : ", product_url)
                except Exception:
                    pass 
            print("*" * 50 + " " + str(i) + "Page end!" + " " + "*" * 50)
            time.sleep(5)
            wb.save(f"/Users/kds/Documents/coupang/{name}_{i}page.xlsx")
            wb.close()
            
            driver.quit()

        except NoSuchElementException :
            print("에러가 발생하여 정상적으로 데이터가 수집되지 않았습니다.")
    
    
print(f"*" * 50 + "모든 데이터 수집을 마쳤습니다. 감사합니다. " + " " + "*" * 50)