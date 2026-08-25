#!/usr/bin/env python3
__version__ = "2.3.2"

import os
import sys
import json
import calendar
from datetime import datetime, timedelta, date
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
weekdays_names = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")

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

def get_ed_avr(days):
    w = [0] * 7
    ws = [0] * 7
    wa = [0] * 7
    
    start_date = max(first_ejac_date, datetime.now() - timedelta(days=days))
    total_days = (datetime.now() - start_date).days + 1

    for day in range(total_days):
        c_day = start_date + timedelta(days=day)
        t_day = c_day.strftime("%d.%m.%Y")
        ws[c_day.weekday()] += 1
        nw = len([e for e in EJACS if e.date == t_day])
        w[c_day.weekday()] += nw

    for weekday in range(7):
        wa[weekday] = w[weekday] / ws[weekday] if ws[weekday] > 0 else 0

    return w, ws, wa

def get_unique_dates(ejacs):
    unique_dates = set()
    for e in ejacs:
        d = datetime.strptime(e.date, "%d.%m.%Y").date()
        unique_dates.add(d)
    return unique_dates


def get_current_streak():
    unique_dates = get_unique_dates(EJACS)
    if not unique_dates:
        return 0

    today = date.today()
    yesterday = today - timedelta(days=1)

    if today in unique_dates:
        check_date = today
    elif yesterday in unique_dates:
        check_date = yesterday
    else:
        return 0

    streak = 0
    while check_date in unique_dates:
        streak += 1
        check_date -= timedelta(days=1)

    return streak


def get_max_streak():
    unique_dates = sorted(get_unique_dates(EJACS))
    if not unique_dates:
        return (0, (None, None))

    max_s = 1
    current_s = 1

    best_start = unique_dates[0]
    best_end = unique_dates[0]
    current_start = unique_dates[0]

    for i in range(1, len(unique_dates)):
        if unique_dates[i] == unique_dates[i - 1] + timedelta(days=1):
            current_s += 1
        else:
            current_s = 1
            current_start = unique_dates[i]

        if current_s > max_s:
            max_s = current_s
            best_start = current_start
            best_end = unique_dates[i]

    return (max_s, (best_start, best_end))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] in ("-v", "--version"):
            print(__version__)
            sys.exit(0)

    print("\n" + f" ejac-diary ({__version__}|25.08.2026) ".center(95, "="))
    print()

    if len(EJACS) > 0:
        last_ejac_date = datetime.strptime(EJACS[-1].date, "%d.%m.%Y").date()
        days_ago = (date.today() - last_ejac_date).days
        if days_ago == 0:
            print(f" {"current streak:":<42} {get_current_streak()} (last record: today, {EJACS[-1].time})")
        elif days_ago == 1:
            print(f" {"current streak:":<42} {get_current_streak()} (last record: yesterday, {EJACS[-1].time})")
        elif days_ago < 6:
            print(f" {"current streak:":<42} {get_current_streak()} (last record: {weekdays_names[last_ejac_date.weekday()]}, {EJACS[-1].time})")
        else:
            print(f" {"current streak:":<42} {get_current_streak()} (last record: {EJACS[-1].date}, {EJACS[-1].time})")
    else:
        print(f" {"current streak:":<42} 0 (last record: never)")

    max_streak = get_max_streak()
    if max_streak[0] > 0:
        print(f" {"the longest streak:":<42} {max_streak[0]} ({max_streak[1][0].strftime("%d.%m.%Y")} - {max_streak[1][1].strftime("%d.%m.%Y")}) ")
    else:
        print(f" {"the longest streak:":<42} 0")

    print()

    last_30_days = [(datetime.now() - timedelta(days = i + 1)).strftime("%d.%m.%Y") for i in range(30)]
    ejacs_per_30_days = len(list(filter(lambda ejac: ejac.date in last_30_days, EJACS)))
    if ejacs_per_30_days > 0:
        print(f" {"average frequency (in 30 days):":<42} once per {int(30 / ejacs_per_30_days * 24)}h ({ejacs_per_30_days / 30:.3}/day)")
    else:
        print(f" {"average frequency (in 30 days):":<42} 0")

    if len(EJACS) > 0:
        _, _, wa = get_ed_avr(365)
        print(f" {"favorite day of week (in 365 days):":<42} {weekdays_names[wa.index(max(wa))]:<12} ({wa[wa.index(max(wa))]:.3}/day)")
        print(f" {"the most hated day of week (in 365 days):":<42} {weekdays_names[wa.index(min(wa))]:<12} ({wa[wa.index(min(wa))]:.3}/day)")
    else:
        print(f" {"favorite day of week (in 365 days):":<42} {"N/A":<12} (0/day)")
        print(f" {"the most hated day of week (in 365 days):":<42} {"N/A":<12} (0/day)")

    print()

    cutoff = datetime.now() - timedelta(days=30)
    places = [e.place for e in EJACS if e.place and datetime.strptime(e.date, "%d.%m.%Y") >= cutoff]

    if places:
        counts = {}
        for p in places:
            counts[p] = counts.get(p, 0) + 1

        fav_place = max(counts, key=counts.get)
        fav_place_times = counts[fav_place]
        fav_place_pct = (fav_place_times / len(places)) * 100
    else:
        fav_place, fav_place_pct, fav_place_times = "N/A", 0.0, 0

    print(f" {'favorite location (in 30 days):'}\n {fav_place} ({fav_place_times} times | {fav_place_pct:.1f}%)")
    print()

    while True:
        command = input("\n" + " [n]ew ejac [r]ecords [w]rite to disk [s]tatistics [a]chievements [e]xit ".center(95, "=") + "\n"); print()
        if command == "n":
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

        elif command == "r":
            print("\n".join([ejac.st() for ejac in EJACS]))

        elif command == "w":
            payload = {
                "version": "2.3.1",
                "ejacs": [ejac.to_json() for ejac in EJACS]
            }
            with open(data_file_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
                print("saved")

        elif command == "a":
            print("oops.. achivments section is under development")

        elif command == "e":
            break
        elif command == "s":
            user_input = input("statistics for how many days (or DD.MM.YYYY date, Enter for all)? ").strip()
            if not user_input:
                first_cutted_day = first_ejac_date
            elif user_input.isdigit():
                cutoff = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=int(user_input))
                first_cutted_day = max(first_ejac_date, cutoff)
            else:
                parsed_date = datetime.strptime(user_input, "%d.%m.%Y")
                first_cutted_day = max(first_ejac_date, parsed_date)
            number_of_cutted_days = (datetime.now() - first_cutted_day).days + 1
            cutted_ejacs = [e for e in EJACS if datetime.strptime(e.date, "%d.%m.%Y") >= first_cutted_day]
            
            while True:
                stats_command = input("\n" + "[a]verage [c]alendar [w]eek days [m]onths [h]ours [t]imes per day [p]laces [b]ack".center(95, "=") + "\n"); print()
                if stats_command == "a":
                    delta = (datetime.now() - first_ejac_date).days
                    if delta != 0:
                        today = datetime.now()

                        all_before_today = len(list(filter(lambda ejac: ejac.date != today.strftime("%d.%m.%Y"), cutted_ejacs)))
                        final_all_without_today = round(all_before_today / delta, 3)
                        print(f"last midnight avrg per day (all time):      {final_all_without_today:<5} ({all_before_today}w/{delta}d){" "*(7-(len(str(all_before_today))+len(str(delta))))}{"■"*int(final_all_without_today*20)}")

                        final_all_with_today = round((len(cutted_ejacs) / (delta + 1)), 3)
                        print(f"next midnight avrg per day (all time):      {final_all_with_today:<5} ({len(cutted_ejacs)}w/{delta+1}d){" "*(7-(len(str(len(cutted_ejacs)))+len(str(delta+1))))}{"■"*int(final_all_with_today*20)}\n")

                        for term in [7, 14, 30, 90, 180, 360]:
                            last_x_days = [(today - timedelta(days = i + 1)).strftime("%d.%m.%Y") for i in range(term)]
                            ejacs_per_x_days = len(list(filter(lambda ejac: ejac.date in last_x_days, cutted_ejacs)))
                            final_number_x_days = round(ejacs_per_x_days / term, 3)
                            print(f"last midnight avrg per day (last {term} days):{" "*(4-len(str(term)))}{final_number_x_days:<5} ({ejacs_per_x_days}w/{term}d){" "*(7-(len(str(ejacs_per_x_days))+len(str(term))))}{"■"*int(final_number_x_days*20)}")
                    else:
                        final_all_with_today = round((len(cutted_ejacs) / (delta + 1)), 3)
                        print(f"""last midnight avrg per day (all time):      0.0   (0w/0d)
        next midnight avrg per day (all time):      {final_all_with_today:<5} ({len(cutted_ejacs)}w/{delta+1}d){" "*(7-(len(str(len(cutted_ejacs)))+len(str(delta+1))))}{"■"*int(final_all_with_today*20)}

        last midnight avrg per day (last 7 days):   0.0   (0w/7d)
        last midnight avrg per day (last 14 days):  0.0   (0w/14d)
        last midnight avrg per day (last 30 days):  0.0   (0w/30d)
        last midnight avrg per day (last 90 days):  0.0   (0w/90d)
        last midnight avrg per day (last 180 days): 0.0   (0w/180d)
        last midnight avrg per day (last 360 days): 0.0   (0w/360d)""")

                elif stats_command == "c":
                    print(f"\n\n{first_cutted_day.strftime('%d.%m.%Y')}: |" + " " * first_cutted_day.weekday(), end="")
                    ejacs_at_week = 0
                    total_days = (datetime.now() - first_cutted_day).days + 1

                    for day in range(total_days):
                        c_day = first_cutted_day + timedelta(days=day)
                        t_day = c_day.strftime("%d.%m.%Y")

                        if c_day.weekday() == 0 and day > 0:
                            print(f"|{'■' * ejacs_at_week} \n{t_day}: |", end="")
                            ejacs_at_week = 0

                        nw = len([w for w in cutted_ejacs if w.date == t_day])
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
                    print(f"{' ' * (6 - c_day.weekday())}|{'■' * ejacs_at_week}")

                elif stats_command == "m":
                    cmw = 0
                    cm = first_cutted_day.month
                    _, cml = calendar.monthrange(first_cutted_day.year, first_cutted_day.month)
                    print(first_cutted_day.strftime("%m.%Y") + ": ", end="")
                    for day in range((datetime.now() - first_cutted_day).days + 1):
                        c_day = first_cutted_day + timedelta(days = day)
                        if cm != c_day.month:
                            avr = round(cmw / cml, 3)
                            print(f"{cmw}w/{cml}d {avr:<5} {'■' * int(avr * 20)}")

                            cm = c_day.month
                            _, cml = calendar.monthrange(c_day.year, c_day.month)
                            cmw = 0
                            month = str(c_day.month)
                            if c_day.month < 10:
                                month = "0" + month
                            print(f"{month}.{c_day.year}: ", end="")

                        cmw += len(list(filter(lambda w: w.date == c_day.strftime("%d.%m.%Y"), cutted_ejacs)))
                    print("...")

                elif stats_command == "t":
                    if len(cutted_ejacs) > 0:
                        ejacs_per_day_distribution = {}
                        for day in range((datetime.now() - first_cutted_day).days + 1):
                            c_day = first_cutted_day + timedelta(days=day)
                            t_day = c_day.strftime("%d.%m.%Y")
                            nw = len(list(filter(lambda w: w.date == t_day, cutted_ejacs)))
                            ejacs_per_day_distribution[nw] = ejacs_per_day_distribution.get(nw, 0) + 1
                        
                        max_val = max(ejacs_per_day_distribution.values(), default=0)

                        for nw in sorted(ejacs_per_day_distribution):
                            count = ejacs_per_day_distribution[nw]
                            bar_len = int(100 * count / max_val) if max_val > 0 else 0
                            print(f"{nw}: {count:<4}{'■' * bar_len}")
                            if nw == 0:
                                print()
                    
                elif stats_command == "h":
                    hours = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    wihl = 0
                    for ejac in cutted_ejacs:
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

                elif stats_command =="w":
                    w, ws, wa = get_ed_avr(number_of_cutted_days)
                    for week_day in range(7):
                        ist = f"{w[week_day]}/{ws[week_day]}={wa[week_day]:.2f}"
                        print(f"{weekdays_names[week_day]:<10}: {ist:<10} | {'∎' * int(20 * wa[week_day])}")

                elif stats_command == "p":
                    counts = {}
                    for ejac in cutted_ejacs:
                        counts[ejac.place] = counts.get(ejac.place, 0) + 1
                    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
                    for place, count in sorted_counts:
                        print(f"{place}: {count}")
                elif stats_command == "b":
                    break

