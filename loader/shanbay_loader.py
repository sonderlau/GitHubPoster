import requests

from .base_loader import BaseLoader
from .config import SHANBAY_CALENDAR_API


class ShanBayLoader(BaseLoader):
    track_color = "#33C6A4"
    unit = "days"

    def __init__(self, from_year, to_year, **kwargs):
        super().__init__(from_year, to_year)
        self.user_name = kwargs.get("user_name", "")

    @classmethod
    def add_loader_arguments(cls, parser):
        parser.add_argument(
            "--user_name",
            dest="user_name",
            type=str,
            required=True,
            help="",
        )

    def get_api_data(self):
        month_list = self.make_month_list()
        data_list = []
        for m in month_list:
            r = requests.get(
                SHANBAY_CALENDAR_API.format(
                    user_name=self.user_name,
                    start_date=m.to_date_string(),
                    end_date=m.end_of("month").to_date_string(),
                )
            )
            if not r.ok:
                print(f"get shanbay calendar api failed {str(r.text)}")
            try:
                data_list.extend(r.json()["logs"])
            except Exception:
                # just pass for now
                pass
        return data_list

    def make_track_dict(self):
        data_list = self.get_api_data()
        for d in data_list:
            if d:
                self.number_by_date_dict[d["date"]] = 1
                self.number_list.append(1)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
