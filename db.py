import psycopg2


class DataBase:
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", user="postgres", password="password")
        self.conn.autocommit = True

    def insert_site(self,data_object):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO crawldb.site VALUES (%s, %s, %s, %s)",
                    (data_object.id, data_object.domain,data_object.robots_content, data_object.sitemap_content))
        cur.close()
        return True

    def insert_page(self,data_object):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO crawldb.page VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (data_object.id, data_object.site_id,data_object.page_type_code, data_object.url,
                     data_object.html_content, data_object.html_status_code, data_object.accessed_time))
        cur.close()
        return True

    def insert_image(self,data_object):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO crawldb.image VALUES (%s, %s, %s, %s, %s, %s)",
                    (data_object.id, data_object.page_id,data_object.filename, data_object.content_type,
                     data_object.data, data_object.accessed_time))
        cur.close()
        return True

    def insert_page_data(self,data_object):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO crawldb.page_data VALUES (%s, %s, %s, %s)",
                    (data_object.id, data_object.page_id, data_object.data_type_code,
                     data_object.data))
        cur.close()
        return True

    def insert_link(self,data_object):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO crawldb.link VALUES (%s, %s)",
                    (data_object.from_page, data_object.to_page))
        cur.close()
        return True