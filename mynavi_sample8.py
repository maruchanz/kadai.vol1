import os   
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
from itertools import zip_longest

# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

# main処理

def main():
    search_keyword = input("キーワードを入力してください>>> ")
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得
    df = pd.DataFrame({'name':[],'salary':[]})
    exp_name_list = []
    exp_salary_list = []
    page_num = driver.find_elements_by_class_name("js__searchRecruit--count")
    
    # try:
    page_count = int(page_num[0].text)//50
    print(page_count)
    # except:
    #     pass
    # 検索結果の一番上の会社名を取得

    for n in range(page_count):
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        salary_list = driver.find_elements_by_class_name("tableCondition__body")

        for name in name_list:
            exp_name_list.append(name.text)

        for salary in salary_list:
            exp_salary_list.append(salary.text)
            # # print(name.text)
            # print(salary.text)　

        url = driver.find_element_by_class_name("iconFont--arrowLeft")
        URL=url.get_attribute("href")
        driver.get(URL)


    name = exp_name_list
    salary = exp_salary_list
    series = pd.Series([name, salary],["name", "salary"])  
    print(series)
    df = df.append(series, ignore_index =True)
    df.to_csv('hoge.csv')
    print('完了')



# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
