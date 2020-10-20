import csv
import os
import re
import ssl
import sqlite3
import tempfile
import urllib.request


class Loader:
    """ Load and import file into sqlite database"""
    ROOT = "https://rossvyaz.ru/data/"
    FILE_EXTENSION = "csv"
    FILES_NAMES = ["ABC-3xx", "ABC-4xx", "ABC-8xx", "DEF-9xx"]

    def __init__(self, db_path):
        self.db_path = db_path
        self.tmp_dir = tempfile.gettempdir()
        self._create_db()

    def _create_db(self):
        if not os.path.exists(self.db_path):
            dir_path = os.path.dirname(os.path.realpath(__file__))
            backup_file = open("{}/files/dump.sql".format(dir_path), "r")
            sql = backup_file.read()
            self.connector = sqlite3.connect(self.db_path)
            cursor = self.connector.cursor()
            cursor.executescript(sql)
        else:
            self.connector = sqlite3.connect(self.db_path)
            cursor = self.connector.cursor()
        cursor.row_factory = sqlite3.Row

    def _get_files_url(self):
        files = []
        for file in self.FILES_NAMES:
            files.append("{}{}.{}".format(self.ROOT, file, self.FILE_EXTENSION))
        return files

    def load(self):
        files_urls = self._get_files_url()
        cursor = self.connector.cursor()
        cursor.execute("DELETE FROM `phone_codes`")
        print("File download started")
        for url in files_urls:
            file_name = url.split("/")[-1]
            file_path = self.tmp_dir + '/' + file_name
            print("{} is loading...".format(file_name))
            ssl._create_default_https_context = ssl._create_unverified_context
            response = urllib.request.urlopen(url)
            tmp_file = open(file_path, "wb")
            data = response.read()
            tmp_file.write(data)
            tmp_file.close()
            file = open(file=file_path, mode="r", encoding="utf8")
            file_format_data = ""
            for line in file:
                if "Оператор" in line:
                    continue
                format_line = (
                    re.sub("(\|.*\|)", ";", line)
                    if line.count("|") > 1
                    else line.replace("|", ";")
                )
                file_format_data += (
                    format_line.replace("'", "").replace("\n", "") + ";\n"
                    if format_line.count(";") == 5
                    else format_line
                )
            tmp_file_path = self.tmp_dir + "/tmp.csv"
            tmp_file = open(tmp_file_path, "wb")
            tmp_file.write(file_format_data.encode())
            tmp_file.close()
            os.remove(file_path)
            file = open(file=tmp_file_path, mode="r", encoding="utf8")
            reader = csv.reader(file, delimiter=";")
            rows = list(map(tuple, reader))
            cursor.executemany(
                "INSERT INTO `phone_codes` (`code`, `begin`, `end`, `count`, `carrier`, `city`, `region`) VALUES (?, ?, ?, ?, ?, ?, ?)",
                rows,
            )
            self.connector.commit()
            os.remove(tmp_file_path)
        self.connector.close()
        print("Database file ready, path: " + self.db_path)
