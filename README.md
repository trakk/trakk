# trakk

Simple cli tasklist with recurrence, checklists, and stats.


# setup

Install dependencies `sudo apt-get install python-psycopg2 python-yaml`

Create database (`db-setup.sql` and tables `table-setup.sql`), then add
credentials to `config.yaml` (see `config.example.yaml` for reference).

`./run` or `python trakk.py`


# license

Copyright (C) 2014 - 2016  David Ulrich

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
