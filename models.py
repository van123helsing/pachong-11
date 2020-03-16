class Site:
    def __init__(self, domain, robots_content, sitemap_content):
        self.domain = domain
        self.robots_content = robots_content
        self.sitemap_content = sitemap_content


class Page:
    def __init__(self, site_id, page_type_code, url, html_content, http_status_code, accessed_time):
        self.site_id = site_id
        self.page_type_code = page_type_code
        self.url = url
        self.html_content = html_content
        self.http_status_code = http_status_code
        self.accessed_time = accessed_time


class PageData:
    def __init__(self, page_id, data_type_code, data):
        self.page_id = page_id
        self.data_type_code = data_type_code
        self.data = data


class Image:
    def __init__(self, page_id, filename, content_type, data, accessed_time):
        self.page_id = page_id
        self.filename = filename
        self.content_type = content_type
        self.data = data
        self.accessed_time = accessed_time


class Link:
    def __init__(self, from_page, to_page):
        self.from_page = from_page
        self.to_page = to_page