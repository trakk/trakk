# trakk

(originally) Simple cli tasklist with recurrence, checklists, and stats.

The ultimate concept is an integrated solution for time management, task management,
calorie consumption/meal planning, exercise regimen, multi timezome time settings


# setup

Create database (`sql/001-db-setup.sql` and tables `sql/002-table-setup.sql`), then add
credentials to `.env` (see `env.example` for reference).

virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
sudo ln -s ~/trakk/src/run /usr/bin/trakk

`trakk`


# features

- maintain a schedule
- audible & notification alarms at boundaries
- "snooze" to auto-extend the current task
  - snooze tasks to push them out of the active tasks for n s/x/h/d/w/m/y
- quick reconfiguration of the current day's schedule
  - "pomodoro" time periods
  - smart swap different blocks
  - movable and immovable time blocks

- date reminders:
  - birthdays, anniversaries, reach-out recommendations

- tasklist with categories
  - when in categorized time, tasks are automatically shown of that type
- 

- how to get an ubiquitous experience across devices?
  - desktop
  - laptop
  - mobile
  - api: cli/web/app clients?


# references
- https://open.lib.umn.edu/collegesuccess/part/chapter-2-staying-motivated-organized-and-on-track/


# license

Copyright (C) 2014 - 2016, 2021  David Ulrich

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

