import random
import time
import getpass

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from urllib.request import urlretrieve
from selenium import webdriver
from bs4 import BeautifulSoup
import PIL.Image as image
import re
import matplotlib.pyplot as plt


class BilibiliLogger(object):

    def __init__(self, username, password, windowsize=(750, 800), executable_path="chromedriver"):
        '''
        function: parameters initialize
        input username: username
        input password: password
        input windowsize: windowsize
        input executable_path: the path of chromedriver
        return none
        '''
        # the login url
        self.url = 'https://passport.bilibili.com/login'
        # the blowaer
        chrome_options = webdriver.ChromeOptions()
        if windowsize != 'max':
            (m, n) = windowsize
            self.set_window_size = '--window-size=' + str(m) + ',' + str(n)
        else:
            self.set_window_size = '--start-maximized'
        chrome_options.add_argument(self.set_window_size)
        self.executable_path = executable_path
        self.browser = webdriver.Chrome(executable_path=executable_path, options=chrome_options)
        # username
        self.username = username
        # password
        self.password = password
        self.wait = WebDriverWait(self.browser, 100)
        self.border = 6
        # if logged in
        self.have_logged_in = False

    def open_webpage(self):
        '''
        function: open the webpage using chromedriver
        input: none
        return: none
        '''
        self.browser.get(self.url)

    def login_bilibili(self):
        '''
        function: input the username and password
        input: none
        return: none
        '''
        # find the username's line
        user_element = self.browser.find_element_by_xpath("//li[@class='item username status-box']/input")
        # find the password's line
        pawd_element = self.browser.find_element_by_xpath("//li[@class='item password status-box']/input")
        print('inputing username...')
        user_element.clear()
        for i in range(len(self.username)):
            user_element.send_keys(self.username[i])
            time.sleep(0.1)
        print('[OK] input username finished')
        print('inputing password...')
        pawd_element.clear()
        for i in range(len(self.password)):
            pawd_element.send_keys(self.password[i])
            time.sleep(0.1)
        print('[OK] input password finished')

    def get_identifying_images(self, gapbg_filename='gapbg.jpg', fullbg_filename='fullbg.jpg', show_images=False):
        '''
        function: get identifying images
        input gapbg_filename: filename of gap background image
        input fullbg_filename: filename of full background image
        input show_images: if show images
        return: location list of gap background image and full background image
        '''
        gapbg = []
        fullbg = []
        # save filenames
        self.gapbg_filename = gapbg_filename
        self.fullbg_filename = fullbg_filename
        while gapbg == [] and fullbg == []:
            bfs = BeautifulSoup(self.browser.page_source, 'lxml')
            gapbg = bfs.find_all('div', class_='gt_cut_bg_slice')
            fullbg = bfs.find_all('div', class_='gt_cut_fullbg_slice')
            # logged in
            if len(gapbg) == 0 or len(fullbg) == 0:
                self.have_logged_in = True
                return None, None
        # find url for gap background
        gapbg_url = re.findall('url\(\"(.*)\"\);', gapbg[0].get('style'))[0].replace('webp', 'jpg')
        # find url for full background
        fullbg_url = re.findall('url\(\"(.*)\"\);', fullbg[0].get('style'))[0].replace('webp', 'jpg')
        gapbg_location_list = []
        fullbg_location_list = []
        for each_gapbg in gapbg:
            location = {}
            location['x'] = int(re.findall('background-position: (.*)px (.*)px;', each_gapbg.get('style'))[0][0])
            location['y'] = int(re.findall('background-position: (.*)px (.*)px;', each_gapbg.get('style'))[0][1])
            gapbg_location_list.append(location)
        for each_fullbg in fullbg:
            location = {}
            location['x'] = int(re.findall('background-position: (.*)px (.*)px;', each_fullbg.get('style'))[0][0])
            location['y'] = int(re.findall('background-position: (.*)px (.*)px;', each_fullbg.get('style'))[0][1])
            fullbg_location_list.append(location)
        # download backgroung images
        urlretrieve(url=gapbg_url, filename=gapbg_filename)
        urlretrieve(url=fullbg_url, filename=fullbg_filename)
        if show_images:
            gapbp_image = plt.imread(gapbg_filename)
            plt.imshow(gapbp_image)
            plt.show()
            fullbp_image = plt.imread(fullbg_filename)
            plt.imshow(fullbp_image)
            plt.show()
        print('[OK] get backgrounds finished')
        return gapbg_location_list, fullbg_location_list

    def merge_identifying_image(self, filename, location_list, show_images=False):
        '''
        function: merge images according to the location list
        input filename: image name
        input location_list: images location list
        input show_images: if show image
        return: merged image
        '''
        print("merging '" + filename + "'...")
        img = image.open(filename)
        img_list_upper = []
        img_list_down = []
        for location in location_list:
            if location['y'] == -58:
                img_list_upper.append(img.crop((abs(location['x']), 58, abs(location['x']) + 10, 166)))
            if location['y'] == 0:
                img_list_down.append(img.crop((abs(location['x']), 0, abs(location['x']) + 10, 58)))
        # a new image
        new_img = image.new('RGB', (260, 116))
        x_offset = 0
        for img in img_list_upper:
            # merge
            new_img.paste(img, (x_offset, 0))
            x_offset += img.size[0]
        x_offset = 0
        for img in img_list_down:
            # merge
            new_img.paste(img, (x_offset, 58))
            x_offset += img.size[0]
        new_img.save(filename)
        if show_images:
            img_array = plt.imread(filename)
            plt.imshow(img_array)
            plt.show()
        print("[OK] image '" + filename + "'" + ' merge finished')
        return new_img

    def compare_pixel(self, img1, img2, x, y):
        '''
        function: compare the pixel in two images
        input img1: gap background image
        input img2: full background image
        x: location x
        y: location y
        return: bool
        '''
        # get the pixel in two images
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        # an error which can be tolerated
        threshold = 60
        # compare
        if (abs(pix1[0] - pix2[0]) < threshold and abs(pix1[1] - pix2[1]) < threshold and abs(
                pix1[2] - pix2[2]) < threshold):
            return True
        else:
            return False

    def get_gap(self, img1, img2):
        '''
        function: get the left of gap
        input img1: gap background image
        input img2: full background image
        return: left
        '''
        # gap size: 44 by 44
        left = 43
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self.compare_pixel(img1, img2, i, j):
                    left = i
                    print('[OK] gap getted')
                    return left
        return left

    def get_track(self, distance):
        """
        function: get the move track
        input distance: error location
        return: list track
        """
        print('creat track...')
        # the move track
        track = []
        # current location
        current = 0
        # mid
        mid = distance * 5 / 9
        # time unit
        t = 0.32
        # initial speed
        v = 0
        while current < distance:
            if current < mid:
                a = 4.5
            else:
                a = -5.2
            # initial speed v0
            v0 = v
            # current speed v = v0 + at
            v = v0 + a * t
            # move distance x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # current location
            current += move
            # track append
            track.append(round(move))
        while current > distance:
            move = -random.randint(0, 2)
            current += move
            track.append(round(move))
        for i in range(10):
            track.append(0)
        print('[OK] track created')
        return track

    def get_slider(self):
        '''
        function: get the slider
        input: none
        return element slider
        '''
        print('getting slider...')
        while True:
            try:
                slider = self.browser.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
                break
            except:
                time.sleep(0.5)
        print('[OK] slider getted')
        return slider

    def move_to_gap(self, slider, track):
        '''
        function: move to the gap
        input slider: element slider
        input track: list track
        return: none
        '''
        ActionChains(self.browser).click_and_hold(slider).perform()
        print('moving the slider...')
        while track:
            x = track[0]
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
            track.remove(x)
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()
        print('[OK] slider move finished')
        pass

    def crack(self, show_images=False):
        '''
        funnction: log in
        input show_images: if show images
        return: bool if logged in
        '''
        # open the web page
        self.open_webpage()
        # input username and password
        self.login_bilibili()
        while True and self.have_logged_in == False:
            try:
                # get background images
                gapbg_location_list, fullbg_location_list = self.get_identifying_images(show_images=show_images)
                # if not log in
                if gapbg_location_list != None and fullbg_location_list != None:
                    gapbg_image = self.merge_identifying_image(self.gapbg_filename, gapbg_location_list,
                                                               show_images=show_images)
                    fullbg_image = self.merge_identifying_image(self.fullbg_filename, fullbg_location_list,
                                                                show_images=show_images)
                    # get the left of gap
                    gap_left = self.get_gap(gapbg_image, fullbg_image)
                    print('gap left: ' + str(gap_left))
                    # get track
                    track = self.get_track(gap_left - self.border)
                    # get slider
                    slider = self.get_slider()
                    # move to gap
                    self.move_to_gap(slider, track)
                    print('verifying...')
                    time.sleep(5)
                # have logged in
                else:
                    print('[OK] login successfully')
                    break
            except:
                print('[ERROR] a unexpected error happend')
                self.have_logged_in = False
                break
        return self.have_logged_in


if __name__ == "__main__":
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    logger = BilibiliLogger(username=username, password=password, windowsize='max',
                            executable_path=r'D:\chromedriver_win32\chromedriver.exe')
    logger.crack(show_images=False)
