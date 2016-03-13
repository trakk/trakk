-- trakk: simple cli tasklist with recurrence, checklists, and stats
-- Copyright (C) 2015 - 2016  David Ulrich
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU Affero General Public License as published
-- by the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU Affero General Public License for more details.
--
-- You should have received a copy of the GNU Affero General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.


CREATE TYPE TrakkStatus AS ENUM ('Open','Closed','Archived');

-- run as user `trakk`
-- individual todo tasks
CREATE TABLE IF NOT EXISTS tasks (
	TaskID SERIAL PRIMARY KEY,
	TaskTitle VARCHAR NOT NULL DEFAULT '',
	TaskDescription VARCHAR NOT NULL DEFAULT '',
	TaskStatus TrakkStatus NOT NULL DEFAULT 'Open'
);

-- checklist items within a task
CREATE TABLE IF NOT EXISTS subtasks (
	SubtaskID SERIAL PRIMARY KEY,
	TaskID INT,
	SubtaskDescription VARCHAR NOT NULL DEFAULT '',
	SubtaskStatus TrakkStatus NOT NULL DEFAULT 'Open'
);
