#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#     Alberto Pérez García-Plaza <alpgarcia@bitergia.com>
#
import argparse
import sys
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def load_dashboard(driver, url, img_name, viz_id=None, date_range=None):

    if date_range:
        url += f"?_g=(refreshInterval:(display:Off,pause:!f,value:0),time:(from:'{date_range[0]}'," +\
            "mode:absolute,to:'{date_range[1]}'))"

    print(url)
    driver.get(url)

    print(driver.title)

    # we have to wait for the page to refresh, the last thing that seems
    # to be updated is the title
    WebDriverWait(driver, 120).until(ec.visibility_of_all_elements_located((By.TAG_NAME, "visualize")))

    # Next 3 lines were taken from: https://gist.github.com/elcamino/5f562564ecd2fb86f559
    win_width = driver.execute_script(
        "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, " +
        "document.documentElement.scrollWidth, document.documentElement.offsetWidth);")
    win_height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, " +
        "document.documentElement.clientHeight, document.documentElement.scrollHeight, " +
        "document.documentElement.offsetHeight);")
    driver.set_window_size(win_width + 100, win_height + 100)

    # save a screenshot of the whole page to disk
    driver.save_screenshot("full-window_" + img_name)

    if viz_id:
        # Crop image to get only the specified viz
        element = driver.find_element_by_xpath(f"//dashboard-panel[.//div[@title='{viz_id}']]")
    elif '/visualize/' in url:
        # Crop image to get editor canvas only
        element = driver.find_element_by_tag_name("visualize")
    else:
        # Crop image to remove menus
        element = driver.find_element_by_tag_name("dashboard-app")

    x_pos = element.location["x"]
    y_pos = element.location["y"]
    width = element.size["width"]
    height = element.size["height"]

    png = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(png))

    img = img.crop((x_pos, y_pos, x_pos + width, y_pos + height))
    img.save(img_name)

    print(driver.title)


def main():
    """Everything starts here. """
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("img_name")
    parser.add_argument("-v", "--viz-id", dest="viz_id")
    parser.add_argument("-s", "--start-date", dest="start_date")
    parser.add_argument("-e", "--end-date", dest="end_date", default="now")

    args = parser.parse_args()

    date_range = None
    if args.start_date:
        date_range = (args.start_date, args.end_date)

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('window-size=1920x1080')

    driver = webdriver.Chrome(chrome_options=options)

    try:
        load_dashboard(driver, args.url, args.img_name, args.viz_id, date_range)

    except Exception as ex:
        print(ex)

    finally:
        driver.quit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        s = "\n\nReceived Ctrl-C or other break signal. Exiting.\n"
        sys.stdout.write(s)
        sys.exit(0)
    except RuntimeError as e:
        s = "Error: %s\n" % str(e)
        sys.stderr.write(s)
        sys.exit(1)
