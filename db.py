import psycopg2


class DataBase:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="postgres",
            user="postgres",
            password="password"
        )
        self.conn.autocommit = True

    def insert_site(self, data_object):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO crawldb.site (domain, robots_content, sitemap_content) VALUES (%s, %s, %s) RETURNING id",
            (data_object.domain, data_object.robots_content, data_object.sitemap_content))
        site_id = cur.fetchone()[0]
        cur.close()
        return site_id

    def insert_page(self, data_object):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO crawldb.page (site_id,page_type_code,url,html_content,http_status_code,accessed_time,hash)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (data_object.site_id, data_object.page_type_code, data_object.url,
             data_object.html_content, data_object.http_status_code, data_object.accessed_time, data_object.hash))
        page_id = cur.fetchone()[0]
        cur.close()
        return page_id

    def insert_image(self, data_object):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO crawldb.image (page_id,filename,content_type,data,accessed_time) VALUES (%s, %s, %s, %s, %s)",
            (data_object.page_id, data_object.filename, data_object.content_type,
             data_object.data, data_object.accessed_time))
        cur.close()
        return True

    def insert_page_data(self, data_object):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO crawldb.page_data (page_id,data_type_code,data) VALUES (%s, %s, %s)",
                    (data_object.page_id, data_object.data_type_code,
                     data_object.data))
        cur.close()
        return True

    def insert_link(self, data_object):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO crawldb.link VALUES (%s, %s)",
                    (data_object.from_page, data_object.to_page))
        cur.close()
        return True

    def empty_database(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM crawldb.link")
        cur.execute("DELETE FROM crawldb.image")
        cur.execute("DELETE FROM crawldb.page_data")
        cur.execute("DELETE FROM crawldb.page")
        cur.execute("DELETE FROM crawldb.site")
        cur.close()
        return True

    def check_if_hash_exists(self, hash):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM crawldb.page WHERE hash=%s", (hash,))
        value = cur.fetchone()
        cur.close()
        return value

    def check_if_domain_exists(self, domain):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM crawldb.site WHERE domain=%s", (domain,))
        value = cur.fetchone()
        cur.close()
        return value
