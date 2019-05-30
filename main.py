import time
import random
import MySQLdb
from selenium import webdriver
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup


# get all courses url from category page
def get_courses_url(course_url):
    link_list = []
    driver.get(course_url)
    time.sleep(3)
    try:
        # remove the close-icon
        driver.find_element_by_class_name("u-icon-close").click()

    except:
        pass

    while True:
        # get the page source
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        link_area = soup.find_all('div', {'class': 'cnt f-pr'})
        for tags in link_area:
            tag = tags.find_all('a')
            for a in tag:
                link = a.get('href')
                try:
                    if link.__contains__(
                            'www') and not link.__contains__('http'):
                        link = 'https:' + link
                        link_list.append(link)
                except:
                    continue

        # auto click the next page
        next_page = driver.find_element_by_xpath(
            '//li[@class="ux-pager_btn ux-pager_btn__next"]/a')
        next_page.click()
        time.sleep(random.randint(1, 3))

        if next_page.get_attribute("class") == "th-bk-disable-gh":
            link_list.append(link)
            break

    link_list = list(set(link_list))
    return link_list


def paser_comments(url, category):
    driver.get(url)
    cont = driver.page_source
    soup = BeautifulSoup(cont, 'html.parser')

    find_comments = driver.find_element_by_id(
        "review-tag-button")  # click the comment tag
    find_comments.click()
    time.sleep(1)

    # get the course name and teacher info
    info = pq(driver.page_source)
    course_name = info(".course-title.f-ib.f-vam").text()
    teacher = info(".cnt.f-fl").text().replace("\n", " ")

    # init the parameter list
    names_list = []  # nikename
    comments_list = []  # comments
    created_time_list = []  # created_time
    course_times_list = []  # course_times
    voteup_list = []  # voteup
    rating_list = []  # rating

    while True:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        try:
            # use bs4 to locate the comments
            content = soup.find_all('div', {
                'class':
                'ux-mooc-comment-course-comment_comment-list_item_body'
            })

            for ctt in content:

                author_name = ctt.find_all(
                    'a', {
                        'class':
                        'primary-link ux-mooc-comment-course-comment_comment-list_item_body_user-info_name'
                    })
                comments = ctt.find_all(
                    'div', {
                        'class':
                        'ux-mooc-comment-course-comment_comment-list_item_body_content'
                    })
                created_time = ctt.find_all(
                    'div', {
                        'class':
                        'ux-mooc-comment-course-comment_comment-list_item_body_comment-info_time'
                    })
                course_times = ctt.find_all(
                    'div', {
                        'class':
                        'ux-mooc-comment-course-comment_comment-list_item_body_comment-info_term-sign'
                    })
                voteup = ctt.find_all('span', {'primary-link'})
                rating = ctt.find_all('div', {"star-point"})

                for name in author_name:
                    names_list.append(name.text)
                for comment in comments:
                    comments_list.append(comment.text.strip('\n'))
                for ct in created_time:
                    created_time_list.append(ct.text)
                for cts in course_times:
                    course_times_list.append(cts.text)
                for vt in voteup:
                    voteup_list.append(vt.text.strip('\n'))
                for r in rating:
                    rating_list.append(str(len(r)))

            # auto click the next page
            next_page = driver.find_element_by_xpath(
                '//li[@class="ux-pager_btn ux-pager_btn__next"]/a')
            next_page.click()
            time.sleep(random.randint(1, 3))

            if next_page.get_attribute("class") == "th-bk-disable-gh":
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                # if the page is the last page, then get the last page's source page
                content = soup.find_all(
                    'div', {
                        'class':
                        'ux-mooc-comment-course-comment_comment-list_item_body'
                    })

                for ctt in content:

                    author_name = ctt.find_all(
                        'a', {
                            'class':
                            'primary-link ux-mooc-comment-course-comment_comment-list_item_body_user-info_name'
                        })
                    comments = ctt.find_all(
                        'div', {
                            'class':
                            'ux-mooc-comment-course-comment_comment-list_item_body_content'
                        })
                    created_time = ctt.find_all(
                        'div', {
                            'class':
                            'ux-mooc-comment-course-comment_comment-list_item_body_comment-info_time'
                        })
                    course_times = ctt.find_all(
                        'div', {
                            'class':
                            'ux-mooc-comment-course-comment_comment-list_item_body_comment-info_term-sign'
                        })
                    voteup = ctt.find_all('span', {'primary-link'})
                    rating = ctt.find_all('div', {"star-point"})

                    for name in author_name:
                        names_list.append(name.text)
                    for comment in comments:
                        comments_list.append(comment.text.strip('\n'))
                    for ct in created_time:
                        created_time_list.append(ct.text)
                    for cts in course_times:
                        course_times_list.append(cts.text)
                    for vt in voteup:
                        voteup_list.append(vt.text.strip('\n'))
                    for r in rating:
                        rating_list.append(str(len(r)))

                break

        except:
            break

    # saving to database
    for i in range(len(names_list)):
        author_name = names_list[i]
        comments = comments_list[i]
        created_time = created_time_list[i]
        course_times = course_times_list[i]
        voteup = voteup_list[i]
        rating = rating_list[i]
        line = [
            category, course_name, teacher, url, author_name, comments,
            created_time, course_times, voteup, rating
        ]

        insert_sql = """
                        insert into rating_and_comments(category,course_name, teacher, url, author_name, comments, created_time, course_times, voteup, rating)
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                     """

        cursor.execute(insert_sql,
                       (category, course_name, teacher, url, author_name,
                        comments, created_time, course_times, voteup, rating))

        conn.commit()

        print("{0}-{1}: saving to database successful".format(
            author_name, course_name))


if __name__ == "__main__":
    '''
    Init Setting
    '''
    conn = MySQLdb.connect(
        '127.0.0.1', 'root', 'ROOT', 'mooc', charset='utf8', use_unicode=True)
    cursor = conn.cursor()
    driver = webdriver.Chrome(executable_path=r"../drivers/chromedriver.exe")

    category_list = ['foreign-language']

    for category in category_list:
        # category = 'teaching-method'
        course_url = 'https://www.icourse163.org/category/' + category
        link_list = get_courses_url(course_url)
        for url in link_list:
            try:
                paser_comments(url, category)
            except:
                continue

    driver.quit()
    conn.close()

    print("Done...")
