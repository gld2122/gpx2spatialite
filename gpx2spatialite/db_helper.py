# Copyright (C) 2014  Peter Vasil <mail@petervasil.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].


from .spatialite_finder import get_connection
from .__init__ import get_data


def create_new_db(db_path):
    connection = get_connection(db_path)
    create_db_script = get_data("sql/create_db.sql")

    cursor = connection.cursor()

    init_spatial_metadata(connection)

    create_db_query = open(create_db_script, 'r').read()
    cursor.executescript(create_db_query)
    connection.commit()

    cursor.close()
    connection.close()


def init_spatial_metadata(connection):
    cursor = connection.cursor()
    result = cursor.execute('SELECT spatialite_version()')
    spatialite_version = result.fetchone()[0]

    from distutils.version import LooseVersion
    if cmp(LooseVersion(spatialite_version),
           LooseVersion('4.1')) == -1:
        cursor.execute('SELECT InitSpatialMetaData()')
    else:
        cursor.execute('SELECT InitSpatialMetaData(1)')

    connection.commit()
