import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.log import configure_logging
from scrapy.exceptions import CloseSpider
import logging
import json
from datetime import datetime
import pandas as pd
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import time

class ExRxSpider(scrapy.Spider):
    name = "exrx"
    start_urls = ["https://exrx.net"]
    allowed_domains = ["exrx.net"]
    custom_settings = {
        "LOG_LEVEL": "INFO",
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS": 5,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1,
        "AUTOTHROTTLE_MAX_DELAY": 10,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 1.0,
        "ROBOTSTXT_OBEY": True,
        "DEPTH_LIMIT": 5,
        "DOWNLOAD_TIMEOUT": 15,
        "RETRY_HTTP_CODES": [500, 502, 503, 504, 408],
        "FEEDS": {
            "exrx_data.json": {"format": "json", "encoding": "utf-8"},
        },
        "RETRY_TIMES": 5,
        "USER_AGENT": "ExRxSpider (+http://tu-sitio-web.com/contacto)"
    }

    def __init__(self):
        self.start_time = time()  # Iniciar el temporizador
        self.scraped_data = []
        self.conn = self.init_url_db()
        self.driver = webdriver.Chrome(
            service=Service(os.getenv("CHROMEDRIVER_PATH", "/ruta/a/chromedriver")),
            options=self.get_selenium_options()
        )

    def init_url_db(self):
        conn = sqlite3.connect("visited_urls.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS urls (url TEXT PRIMARY KEY)")
        conn.commit()
        return conn

    def add_visited_url(self, url):
        self.conn.execute("INSERT OR IGNORE INTO urls (url) VALUES (?)", (url,))
        self.conn.commit()

    def is_url_visited(self, url):
        c = self.conn.cursor()
        c.execute("SELECT 1 FROM urls WHERE url = ?", (url,))
        return c.fetchone() is not None

    def get_selenium_options(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        return options

    def parse(self, response):
        logging.info(f"Scraping {response.url}")
        if self.is_url_visited(response.url):
            logging.info(f"URL ya procesada: {response.url}")
            return
        self.add_visited_url(response.url)

        try:
            page_data = {
                "url": response.url,
                "title": response.css("title::text").get(),
                "headings": self.extract_headings(response),
                "paragraphs": self.clean_text(response.css("p::text").getall()),
                "tables": self.extract_tables(response),
                "lists": self.extract_lists(response),
            }
            if not page_data["tables"] and not page_data["lists"] and not page_data["paragraphs"]:
                logging.warning(f"La página {response.url} no contiene datos útiles.")
            self.scraped_data.append(page_data)
        except Exception as e:
            logging.error(f"Error inesperado al procesar {response.url}: {e}")

        link_extractor = LinkExtractor(allow_domains=self.allowed_domains)
        for link in link_extractor.extract_links(response):
            if self.is_valid_url(link.url):
                yield scrapy.Request(link.url, callback=self.parse)

    def fetch_dynamic_content(self, url):
        try:
            self.driver.get(url)
            html = self.driver.page_source
            return html
        except Exception as e:
            logging.error(f"Error al cargar contenido dinámico: {e}")
            return ""

    def closed(self, reason):
        elapsed_time = time() - self.start_time
        logging.info(f"Scraping completado en {elapsed_time:.2f} segundos. Guardando datos...")
        try:
            self.conn.close()
        except Exception as e:
            logging.error(f"Error al cerrar SQLite: {e}")

        try:
            self.driver.quit()
        except Exception as e:
            logging.error(f"Error al cerrar Selenium: {e}")

        try:
            self.save_scraped_data()
        except Exception as e:
            logging.error(f"Error al guardar los datos: {e}")

    def save_scraped_data(self):
        output_data = {
            "scraped_at": datetime.now().isoformat(),
            "total_pages": len(self.scraped_data),
            "data": self.scraped_data,
        }
        output_path = os.path.join(os.getcwd(), "exrx_final_data.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        logging.info(f"Datos guardados en {output_path}")
        self.save_data_chunked(self.scraped_data, chunk_size=100)

    def extract_headings(self, response):
        headings = {}
        try:
            for level in range(1, 7):
                selector = f"h{level}::text"
                headings[f"h{level}"] = self.clean_text(response.css(selector).getall())
        except Exception as e:
            logging.error(f"Error al extraer encabezados: {e}")
        return headings

    def extract_tables(self, response):
        tables = []
        try:
            for table in response.css("table"):
                rows = []
                for row in table.css("tr"):
                    cells = [
                        {
                            "text": self.clean_text([cell.css("::text").get()])[0] if cell.css("::text").get() else "",
                            "html": cell.get()
                        }
                        for cell in row.css("td, th")
                    ]
                    rows.append(cells)
                tables.append(rows)
        except Exception as e:
            logging.error(f"Error al extraer tablas: {e}")
        return tables

    def extract_lists(self, response):
        lists = {
            "unordered": [],
            "ordered": [],
        }
        try:
            for ul in response.css("ul"):
                lists["unordered"].append(self.clean_text(ul.css("li::text").getall()))
            for ol in response.css("ol"):
                lists["ordered"].append(self.clean_text(ol.css("li::text").getall()))
        except Exception as e:
            logging.error(f"Error al extraer listas: {e}")
        return lists

    def clean_text(self, text_list):
        return [
            text.strip().replace("\n", " ").encode("ascii", "ignore").decode("ascii")
            for text in text_list if text and text.strip()
        ]

    def is_valid_url(self, url):
        excluded_patterns = ["privacy", "terms", "login", "download"]
        return (
            url.startswith("https://exrx.net") and
            not any(pattern in url for pattern in excluded_patterns)
        )

    def save_data_chunked(self, data, chunk_size=100):
        for i in range(0, len(data), chunk_size):
            chunk_path = os.path.join(os.getcwd(), f"exrx_data_part_{i // chunk_size + 1}.json")
            with open(chunk_path, "w", encoding="utf-8") as f:
                json.dump(data[i:i+chunk_size], f, indent=4, ensure_ascii=False)
            logging.info(f"Chunk guardado en {chunk_path}")

if __name__ == "__main__":
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        handlers=[
            logging.FileHandler("exrx_info.log", mode="a"),
            logging.FileHandler("exrx_errors.log", mode="a")
        ],
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    process = CrawlerProcess()
    process.crawl(ExRxSpider)
    try:
        process.start()
    except CloseSpider as e:
        logging.error(f"Proceso detenido: {e}")
