# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
