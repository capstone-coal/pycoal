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

all : report.pdf problem-statement.pdf requirements.pdf techreview.pdf design.pdf \
presentation.pdf problem-statement-student.pdf fall-report.pdf

# execute pdflatex twice to update references

report.pdf :
	pdflatex report.ltx
	pdflatex report.ltx

problem-statement.pdf :
	pdflatex problem-statement.ltx
	pdflatex problem-statement.ltx

requirements.pdf :
	pdflatex requirements.ltx
	pdflatex requirements.ltx

techreview.pdf :
	pdflatex techreview.ltx
	pdflatex techreview.ltx

design.pdf :
	pdflatex design.ltx
	pdflatex design.ltx

presentation.pdf :
	pdflatex presentation.ltx
	pdflatex presentation.ltx

problem-statement-student.pdf :
	pdflatex problem-statement-student.ltx
	pdflatex problem-statement-student.ltx

fall-report.pdf :
	pdflatex fall-report.ltx
	pdflatex fall-report.ltx

clean :
	rm -f report.pdf
	rm -f problem-statement.pdf
	rm -f requirements.pdf
#	rm -f techreview.pdf
	rm -f design.pdf
	rm -f presentation.pdf
	rm -f problem-statement-student.pdf
	rm -f fall-report.pdf
