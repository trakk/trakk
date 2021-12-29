-- trakk: simple cli tasklist with recurrence, checklists, and stats
-- Copyright (C) 2015 - 2016, 2021  David Ulrich
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


CREATE TABLE IF NOT EXISTS categories (
	category_id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v1(),
	category_slug TEXT NOT NULL DEFAULT '',
	category_title TEXT NOT NULL DEFAULT ''
);


CREATE TYPE TrakkStatus AS ENUM ('open','closed','archived');

-- run as user `trakk`
-- individual todo tasks
DROP TABLE IF EXISTS tasks;
CREATE TABLE IF NOT EXISTS tasks (
	task_id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v1(),
	task_title TEXT NOT NULL DEFAULT '',
	task_description TEXT NOT NULL DEFAULT '',
	task_status TrakkStatus NOT NULL DEFAULT 'open',
	category_id UUID
);

-- checklist items within a task
DROP TABLE IF EXISTS subtasks;
CREATE TABLE IF NOT EXISTS subtasks (
	subtask_id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v1(),
	task_id UUID,
	subtask_description TEXT NOT NULL DEFAULT '',
	subtask_status TrakkStatus NOT NULL DEFAULT 'open'
);
