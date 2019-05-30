'''
@Description: The saver file 
@Author: Chase Huang
@Date: 2019-05-30 09:39:29
@LastEditTime: 2019-05-30 11:15:58
'''
import MySQLdb


def saver(category, course_name, teacher, url, names_list, comments_list,
          created_time_list, course_times_list, voteup_list, rating_list, conn,
          cursor):
    '''
    @description: Save the comments info to mysql
    @param All field in mysql; {"conn,cursor": the code to use mysql}
    @return: None
    '''
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