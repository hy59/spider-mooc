'''
@Description: The main file
@Author: Chase Huang
@Date: 2019-05-30 09:29:39
@LastEditTime: 2019-05-30 11:10:23
'''
import MySQLdb
from selenium import webdriver
from utils.parser import get_courses_url, paser_comments
from utils.saver import saver


def main():
    '''
    @description: This is the main function to set the database info and load the webdriver, then start the crawler
    '''
    conn = MySQLdb.connect(
        'mysql address deafult:127.0.0.1',
        'user',
        'pwd',
        'database',
        charset='utf8',
        use_unicode=True)
    cursor = conn.cursor()
    driver = webdriver.Chrome(executable_path=r"drivers/chromedriver.exe")
    # category list from mooc category
    category_list = [
        'computer', 'foreign-language', 'psychology', 'ECO', 'management',
        'law', 'literature', 'historiography', 'philosophy', 'engineering',
        'science', 'biomedicine', 'agriculture', 'art-design',
        'teaching-method'
    ]
    for category in category_list:
        course_url = 'https://www.icourse163.org/category/' + category
        link_list = get_courses_url(course_url, driver)
        for url in link_list:
            try:
                category, course_name, teacher, url, names_list, comments_list, created_time_list, course_times_list, voteup_list, rating_list = paser_comments(
                    url, category, driver)

                saver(category, course_name, teacher, url, names_list,
                      comments_list, created_time_list, course_times_list,
                      voteup_list, rating_list, conn, cursor)

            except:
                continue

    driver.quit()
    conn.close()

    print("\nALL Done...")


if __name__ == "__main__":
    main()
