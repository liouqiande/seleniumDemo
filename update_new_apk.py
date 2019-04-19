# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


class UpdateNewApk():
    # 登陆 jenkins
    def login_jenkins(self, driver):
        # 定位登陆元素
        username = (By.ID, "j_username")
        password = (By.NAME, "j_password")
        remember_me = (By.ID, "remember_me")
        login_btn = (By.ID, "yui-gen1-button")

        driver.find_element(*username).send_keys("xxxx")
        driver.find_element(*password).send_keys("xxxx")
        driver.find_element(*remember_me).click()
        driver.find_element(*login_btn).click()

    # 构建新debug_qa包
    def creat_new_apk(self, driver):
        # 点击构建选项
        build = (By.PARTIAL_LINK_TEXT, "Build with Parameters")
        driver.find_element(*build).click()
        # 新建debug_qa包
        config_box = (By.XPATH, "//*[@id='main-panel']/form/table/tbody[2]/tr[1]/td[3]/div/select")
        debug_qa = (By.XPATH,"//*[@id='main-panel']/form/table/tbody[2]/tr[1]/td[3]/div/select/option[3]")
        start_btn = (By.ID, "yui-gen1-button")

        driver.find_element(*config_box).click()
        driver.find_element(*debug_qa).click()
        driver.find_element(*start_btn).click()

    # 获取最新构建的qa包的二维码url
    def get_apk_url(self, driver):
        url = "xxxx"
        driver.get(url)
        driver.maximize_window()
        self.login_jenkins(driver)

        debug_qa_apk = (By.XPATH, "//a[@class='tip model-link inside build-link display-name zws-inserted']")

        for element in driver.find_elements(*debug_qa_apk):
            apk_url = element.get_attribute("href")
            if "​develop ​Debug_qa" in element.get_attribute("text"):
                apk_num = apk_url.split("/")[-2]
                self.final_url = "xxxx" + str(apk_num)
                break
            # if "​develop ​Debug_qa" not in element.get_attribute("text"):
            #     self.creat_new_apk(driver)
            #     time.sleep(180)
        return self.final_url

    def login_didifarm(self, driver):
        url = "xxxx"
        driver.get(url)
        driver.maximize_window()
        username = (By.ID, "username")
        password = (By.ID, "password")
        login_btn = (By.ID, "submit")

        driver.find_element(*username).send_keys("xxxx")
        driver.find_element(*password).send_keys("xxxx")
        driver.find_element(*login_btn).click()

    def upload_apk(self, driver, apk_version, apk_url):
        self.login_didifarm(driver)
        # 定位测前数据
        top_btn = (By.XPATH, "//a[@class='dropdown-toggle']")
        # 定位测试包->Android_司机
        andoroid_driver = (By.XPATH, "/html/body/div[3]/div[1]/ul[2]/li[1]/ul/div[4]/div[1]/a[1]")
        # 定位编辑按钮
        edit_btn = (By.XPATH, "//button[@class='btn btn-success editPackage']")

        # 识别需要悬停的测前数据元素
        top_btn_list = driver.find_elements(*top_btn)
        for ele in top_btn_list:
            # 鼠标移到悬停元素上
            ActionChains(driver).move_to_element(ele).perform()
            # 点击Android_司机
            driver.find_element(*andoroid_driver).click()
            break
        # 点击第二个编辑按钮
        edit_btn_list = driver.find_elements(*edit_btn)
        for ele in edit_btn_list:
            if "xxxx" in ele.get_attribute("cdata"):
                ele.click()
        # 输入apk信息
        version = (By.NAME, "version")
        apk_link = (By.NAME, "link")
        save_btn = (By.ID, "saveToUpdate")
        confirm_btn = (By.ID, "confirm_info")

        driver.find_element(*version).clear()
        driver.find_element(*version).send_keys(apk_version)
        time.sleep(3)
        if apk_url != "":
            driver.find_element(*apk_link).clear()
            driver.find_element(*apk_link).send_keys(apk_url)
        driver.find_element(*save_btn).click()
        driver.find_element(*confirm_btn).click()


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    up = UpdateNewApk()
    apk_url = up.get_apk_url(driver)
    apk_version = "5.1.50"
    up.upload_apk(driver, apk_version, apk_url)
    driver.close()
