import os
import sys
import time

import pyautogui
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.auto_util import AppName, AutoUtil
class WechatAuto:
    def __init__(self):
        self.auto_util = AutoUtil(AppName.WECHAT)
        
    def go_to_chat(self):
        self.auto_util.find_click_img("chat_unselect.png")

    def search_friend(self, friend_name):
        try:
            self.auto_util.find_click_img("chat_unselect")
        except pyautogui.ImageNotFoundException:
            self.auto_util.find_click_img("chat_select")
        self.auto_util.find_click_img("search", offset_x=100)
        self.auto_util.send_text(friend_name)
        self.auto_util.find_click_img("contact_person",offset_x=100,offset_y=100,minSearchTime=10)
        self.auto_util.find_click_img("search",offset_x=-100,offset_y=-100,minSearchTime=10)

if __name__ == "__main__":
    time.sleep(3)
    wechat_auto = WechatAuto()
    wechat_auto.search_friend("李杨林")
    
