#
# SchoolTool - common information systems platform for school administration
# Copyright (c) 2005 Shuttleworth Foundation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
Functional tests for schooltool.timetable.

$Id$
"""

import unittest

from schooltool.testing.functional import collect_ftests
from schooltool.timetable.ftesting import timetable_functional_layer

def test_suite():
    return collect_ftests(layer=timetable_functional_layer)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')