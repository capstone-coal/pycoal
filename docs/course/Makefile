# Copyright (C) 2017 COAL Developers
#
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation; version 2.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty 
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with this program; if not, write to the Free 
# Software Foundation, Inc., 51 Franklin Street, Fifth 
# Floor, Boston, MA 02110-1301, USA.

# makefile to build course documents

all : report.pdf problem-statement.pdf requirements.pdf techreview.pdf design.pdf \
presentation.pdf problem-statement-student.pdf fall-report.pdf

report.pdf :
	./build.sh report/report.ltx report

problem-statement.pdf :
	./build.sh problem-statement/problem-statement.ltx problem-statement

requirements.pdf :
	./build.sh requirements/requirements.ltx requirements

techreview.pdf :
	./build.sh technology-review/techreview.ltx technology-review

design.pdf :
	./build.sh design/design.ltx design

presentation.pdf :
	./build.sh presentation/presentation.ltx presentation

presentation-winter.pdf :
	./build.sh presentation-winter/presentation-winter.ltx presentation-winter

presentation-winter-final.pdf :
	./build.sh presentation-winter-final/presentation-winter-final.ltx presentation-winter-final

problem-statement-student.pdf :
	./build.sh problem-statement-student/problem-statement-student.ltx problem-statement-student

fall-report.pdf :
	./build.sh fall-report/fall-report.ltx fall-report

winter-progress.pdf :
	./build.sh winter-progress/winter-progress.ltx winter-progress

spring-midterm.pdf :
	./build.sh spring-midterm/spring-midterm.ltx spring-midterm
