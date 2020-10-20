import os
import re
from numverify_rossvyaz_client.loader.main import Loader


class Client:
    def __init__(self, db_path):
        loader = Loader(db_path)
        self.cursor = loader.connector.cursor()

    def get_carrier(self, phone_number):
        phone_number = self._format_phone_number(phone_number)
        sql = """
            SELECT `carrier` FROM `phone_codes` pc
            WHERE pc.`code` = {} and {} BETWEEN pc.`begin` AND pc.`end`
        """.format(
            phone_number[1:4], phone_number[4:11]
        )
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        return list(row)[0] if row is not None else "Неизвестный"

    def get_info(self, phone_number):
        phone_number = self._format_phone_number(phone_number)
        sql = """
            SELECT * FROM `phone_codes` pc
            WHERE pc.`code` = {} and {} BETWEEN pc.`begin` AND pc.`end`
        """.format(
            phone_number[1:4], phone_number[4:11]
        )
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        row = list(row) if row is not None else []
        return {
            "phone": phone_number,
            "carrier": row[4],
            "region": ", ".join(part for part in row[5:7] if part),
        }

    def _format_phone_number(self, phone_number):
        pattern = re.compile(r"[^\d]")
        formated_phone_number = pattern.sub("", phone_number)
        return formated_phone_number if formated_phone_number else ""
