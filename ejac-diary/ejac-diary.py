#!/usr/bin/env python3
__version__ = "2.3.1"
print(f"ejac-diary ({__version__}|25.08.2026) - a cli for logging ejaculations")

import os
import sys
import json
import calendar
from datetime import datetime, timedelta
from pathlib import Path

class Ejac():
    def __init__(self, date, time, act_type, place, note):
        self.date = date
        self.time = time
        self.act_type = act_type
        self.place = place
        self.note = note

    def st(self):
        return f"{self.date} {self.time} {" "*(5-len(self.time))}- {self.act_type} at {self.place} ({self.note})"
    
    def to_json(self):
        return {"date": self.date, "time": self.time, "act_type": self.act_type, "place": self.place, "note": self.note}

EJACS = []

if sys.platform == "win32":
    local_appdata = os.environ.get("LOCALAPPDATA")
    base_dir = Path(local_appdata) if local_appdata else Path.home() / "AppData" / "Local"
elif sys.platform == "darwin":
    base_dir = Path.home() / "Library" / "Application Support"
else:
    xdg_data = os.environ.get("XDG_DATA_HOME")
    base_dir = Path(xdg_data) if xdg_data else Path.home() / ".local" / "share"

data_dir = base_dir / "ejac-diary"
data_dir.mkdir(parents=True, exist_ok=True)
data_file_path = data_dir / "data.json"

if os.path.exists(data_file_path):
    with open(data_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        list_ejacs = data
        file_version = 0 # 2.3.0
        print("warning: save data format is outdated (2.3.0 format); it shall be updated, once you make the save")
        backup_path = data_dir / "data.json.backup"
        backup_path.write_bytes(data_file_path.read_bytes())
    else:
        list_ejacs = data["ejacs"]
        file_version = data["version"]

    for ejac in list_ejacs:
        EJACS.append(Ejac(**ejac))

if EJACS:
    first_ejac_date = datetime.strptime(EJACS[0].date, "%d.%m.%Y")
else:
    first_ejac_date = datetime.now()

def help():
    print("""
help - help
n - add new ejac
s - save all
h - view history
d - day time
w - week
a - avarage per different periods
c - calendar
m - months
t - times per day distribution
p - places distribution
e - exit""")

help()


def get_ed_avr():
    w = [0, 0, 0, 0, 0, 0, 0]
    ws = [0, 0, 0, 0, 0, 0, 0]
    for day in range((datetime.now() - first_ejac_date).days + 1):
        c_day = first_ejac_date + timedelta(days = day)
        t_day = c_day.strftime("%d.%m.%Y")
        ws[c_day.weekday()] += 1
        nw = len(list(filter(lambda w: w.date == t_day, EJACS)))
        w[c_day.weekday()] += nw
    return w, ws

if __name__ == "__main__":
    while True:
        if len(sys.argv) == 2:
            if sys.argv[1] in ("-v", "--version"):
                print(__version__)
        command = input("\ncommand: "); print()

        if command == "help":
            help()

        elif command == "n":
            date = input("date: ")
            if date == "t":
                date = datetime.now().strftime("%d.%m.%Y")
            elif date == "y":
                date = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y")
            elif date == "dby":
                date = (datetime.now() - timedelta(days=2)).strftime("%d.%m.%Y")
            args = {"date": date, "time": input("time: "), "act_type": input("act type: "), "place": input("place: "), "note": input("note: ")}
            EJACS.append(Ejac(**args))
            print("\nan ejac added: " + EJACS[-1].st())

        elif command == "h":
            print("\n".join([ejac.st() for ejac in EJACS]))

        elif command == "a":
            delta = (datetime.now() - first_ejac_date).days
            if delta != 0:
                today = datetime.now()

                all_before_today = len(list(filter(lambda ejac: ejac.date != today.strftime("%d.%m.%Y"), EJACS)))
                final_all_without_today = round(all_before_today / delta, 3)
                print(f"last midnight avrg per day (all time):      {final_all_without_today:<5} ({all_before_today}w/{delta}d){" "*(7-(len(str(all_before_today))+len(str(delta))))}{"■"*int(final_all_without_today*20)}")

                final_all_with_today = round((len(EJACS) / (delta + 1)), 3)
                print(f"next midnight avrg per day (all time):      {final_all_with_today:<5} ({len(EJACS)}w/{delta+1}d){" "*(7-(len(str(len(EJACS)))+len(str(delta+1))))}{"■"*int(final_all_with_today*20)}\n")

                for term in [7, 14, 30, 90, 180, 360]:
                    last_x_days = [(today - timedelta(days = i + 1)).strftime("%d.%m.%Y") for i in range(term)]
                    ejaces_per_x_days = len(list(filter(lambda ejac: ejac.date in last_x_days, EJACS)))
                    final_number_x_days = round(ejaces_per_x_days / term, 3)
                    print(f"last midnight avrg per day (last {term} days):{" "*(4-len(str(term)))}{final_number_x_days:<5} ({ejaces_per_x_days}w/{term}d){" "*(7-(len(str(ejaces_per_x_days))+len(str(term))))}{"■"*int(final_number_x_days*20)}")
            else:
                final_all_with_today = round((len(EJACS) / (delta + 1)), 3)
                print(f"""last midnight avrg per day (all time):      0.0   (0w/0d)
next midnight avrg per day (all time):      {final_all_with_today:<5} ({len(EJACS)}w/{delta+1}d){" "*(7-(len(str(len(EJACS)))+len(str(delta+1))))}{"■"*int(final_all_with_today*20)}

last midnight avrg per day (last 7 days):   0.0   (0w/7d)
last midnight avrg per day (last 14 days):  0.0   (0w/14d)
last midnight avrg per day (last 30 days):  0.0   (0w/30d)
last midnight avrg per day (last 90 days):  0.0   (0w/90d)
last midnight avrg per day (last 180 days): 0.0   (0w/180d)
last midnight avrg per day (last 360 days): 0.0   (0w/360d)""")

        elif command == "c":
            try:
                print(f"\n\n{first_ejac_date.strftime("%d.%m.%Y")}: |" + " "  * first_ejac_date.weekday(), end="")
                ejacs_at_week = 0
                for day in range((datetime.now() - first_ejac_date).days + 1):
                    c_day = first_ejac_date + timedelta(days = day)
                    t_day = c_day.strftime("%d.%m.%Y")
                    if c_day.weekday() == 0:
                        print(f"|{ejacs_at_week * "■"} \n{t_day}: |", end="")
                        ejacs_at_week = 0
                    nw = len(list(filter(lambda w: w.date == t_day, EJACS)))
                    ejacs_at_week += nw
                    if nw > 0:
                        if nw == 1:
                            print("░", end="")
                        elif nw == 2:
                            print("▒", end="")
                        else:
                            print("▓", end="")
                    else:
                        print("°", end="")
                print(f"{" " * (6 - c_day.weekday())}|{ejacs_at_week * "■"}")
            except BaseException as e:
                print(e)

        elif command  == "m":
            cmw = 0
            cm = first_ejac_date.month
            _, cml = calendar.monthrange(first_ejac_date.year, first_ejac_date.month)
            print(first_ejac_date.strftime("%m.%Y") + ": ", end="")
            for day in range((datetime.now() - first_ejac_date).days + 1):
                c_day = first_ejac_date + timedelta(days = day)
                if cm != c_day.month:
                    avr = round(cmw / cml, 3)
                    print(f"{cmw}w/{cml}d {avr:<5} {"■" * int(avr * 20)}")

                    cm = c_day.month
                    _, cml = calendar.monthrange(c_day.year, c_day.month)
                    cmw = 0
                    month = str(c_day.month)
                    if c_day.month < 10:
                        month = "0" + month
                    print(f"{month}.{c_day.year}: ", end="")
                else:
                    cmw += len(list(filter(lambda w: w.date == c_day.strftime("%d.%m.%Y"), EJACS)))
            print("...")

        elif command == "t":
            if len(EJACS) > 0:
                ejacs_per_day_distribution = {}
                for day in range((datetime.now() - first_ejac_date).days + 1):
                    c_day = first_ejac_date + timedelta(days=day)
                    t_day = c_day.strftime("%d.%m.%Y")
                    nw = len(list(filter(lambda w: w.date == t_day, EJACS)))
                    ejacs_per_day_distribution[nw] = ejacs_per_day_distribution.get(nw, 0) + 1
                
                max_val = max(ejacs_per_day_distribution.values(), default=0)

                for nw in sorted(ejacs_per_day_distribution):
                    count = ejacs_per_day_distribution[nw]
                    bar_len = int(100 * count / max_val) if max_val > 0 else 0
                    print(f"{nw}: {count:<4}{'■' * bar_len}")
                    if nw == 0:
                        print()
            
        elif command == "d":
            hours = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            wihl = 0
            for ejac in EJACS:
                if ejac.time != "":
                    hours[int(ejac.time.split(":")[0])] += 1
                    wihl += 1
            m = max(hours)

            for n in [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0, 1, 2, 3, 4, 5]:
                hour = hours[n]
                if m != 0:
                    print(f"{n:02}: |{"∎" * int(hour / m * 36):<36} |{str(round(hour / wihl * 100, 1))}% {hour}")
                else:
                    print(f"{n:02}: |{" " * 36} |0% {hour}")
            print()

        elif command =="w":
            w, ws = get_ed_avr()
            week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            for n in range(7):
                if ws[n] > 0:
                    avg = w[n] / ws[n]
                    ist = f"{w[n]}/{ws[n]}={avg:.2f}"
                else:
                    avg = 0.0
                    ist = "0/0=0.00"
                
                print(f"{week_days[n]:<10}: {ist:<10} | {'∎' * int(20 * avg)}")

        elif command == "p":
            counts = {}
            for ejac in EJACS:
                counts[ejac.place] = counts.get(ejac.place, 0) + 1
            sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
            for place, count in sorted_counts:
                print(f"{place}: {count}")

        elif command == "s":
            payload = {
                "version": "2.3.1",
                "ejacs": [ejac.to_json() for ejac in EJACS]
            }
            with open(data_file_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
                print("saved")

        elif command == "e":
            break

