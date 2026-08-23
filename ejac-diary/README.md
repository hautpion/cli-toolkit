ejac-diary is a CLI for tracking sexual activity.

# Usage
The script uses only basic dependancies so there is no need do install external dependencies - you only need python.

Run (in bush) ```python ejac-diary``` (or make it executable via ```chmod +x ejac-diary.py``` and then you can use ```ejac-diary.py```). The program is going to start with printing the help like that:

```
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
e - exit
```
you can always return to it by sending ```help```. We'll go through them all one by one.

## Add new ejac (```n```)
Now we're going to add new ejaculation record. After you send ```n``` the program will request date (of the ejaculation), you shall use the dd.mm.yyyy format. Than it will request time, you shall use the 24-hour format without seconds (although, if you don't quite remember the exact minute of the ejaculation you can type "hh:" or, if you forgot the hour too, left this field and just send ""). Then it will request the act type, you can group your acts as you wish, of course, but I would recomend you use "s" as for sexual intercourses, "m" as for masturbation acts, and "e" as for nocturnal emissions (sorry, those who don't have it). Then it will request place where the ejaculation occured, use any format you'd like. Then you will be asked for a note, you can type there whatever you want or just left it empty. That's all, the ejaculation is added.

## view history (```h```)
Spits out every recorded ejaculation (its date, time, act type, place, and note) from first to last.

## day time (```d```)
Calculates an hourly distribution histogram showing the percentage of total ejaculation records for each hour. Note that the scale runs from 06:00 to 05:00 (rather than 00:00 to 23:00) to align with a typical waking day cycle.

## week (```w```)
Similar to the hourly distribution, but aggregates activity by days of the week instead of hours (so from Monday to Sunday).

## avarage per different periods (```a```)
Calculates average daily frequency across multiple timeframes (last 7, 14, 30, 90, 180, and 360 days) alongside all-time averages (including and excluding today), rendered with a histograms.

## calendar (```c```)
Renders a calendar (starting from the day of the first record), so day is depicted as "°" when there is no record at that day and "░", "▒", and "▓" if there is 1, 2 and 3 or more accordingly. Also it renders a histogram on right side of the calendar of the weekly activity (only there "■" implies one ejaculation record in other places it's relative).

## month (```m```)
Renders a histogram of the monthly activity.

## times per day distribution (```t```)
Renders a histogram of the distribution of daily frequencies grouping number of daily frequencies by days when was that number of ejaculation records per day (0, 1, 2, etc.)

## places distribution (```p```)
Prints list of all places which are in the ejaculation records, sorted by the number of ejaculation records in which they are presented

## exit (```e```)
Closes the tool (WITHOUT SAVING! run ```s``` if you want to save the data)

## P.S.
The term ejaculation is presented as a way more less elastic concept than orgasm, but if you don't ejaculate during sexual activity you can use your understanding of how to determine if the sexual act should be recorded (but better you have Semёn)
