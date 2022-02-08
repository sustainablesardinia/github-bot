# get_repo_data_past_month.py
#
# Beti is informus de su chi ant fatu in Sustainable Sardinia su mesi passau.
#
# Copyright 2022 Sustainable Sardinia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from github import Github
import datetime
import sys
import tempfile


class LanguageWriter:
    def __init__(self, language):
        self.file = tempfile.NamedTemporaryFile(
            mode='xw', prefix=language, delete=False)
        self.language = language

    def _add_line(self, line):
        self.file.write(line)

    def _add_newline(self):
        self.file.write("\n")


class SardinianWriter(LanguageWriter):
    def __init__(self):
        super().__init__("srd")

    def print_post_header(self):
        return

    def print_repo_header(self, full_name, url):
        self._add_line(f"## Traballu in sa faina [{full_name}]({url})")
        return

    def print_commit_header(self, sha, url, date):
        self._add_line(f"[{sha}]({url}) fatu su {date}")
        return

    def print_commit_committer(self, name):
        self._add_line(f"de **{committer_name}**")
        return

    def print_commit_author(self, login, url, name):
        self._add_line(f"de **{committer_name}**")
        return

    def print_commit_stats(self):
        return


if __name__ == "__main__":
    github = Github(sys.argv[1])
    organization = github.get_organization("sustainablesardinia")
    today = datetime.datetime.today()

    for repo in organization.get_repos():
        commits = repo.get_commits()

        if not commits:
            continue

        print(f"## Work in [{repo.full_name}]({repo.url})")

        for commit in commits:

            commit_sha = str(commit.sha)[0:6]
            commit_url = commit.url
            log_string = [f"[{commit_sha}]({commit_url}) on"]
            commit_date = commit.commit.committer.date
            if (today-commit_date).days > 30:
                continue

            log_string += [f"{commit_date}"]
            if commit.author:
                log_string += [
                    f"by **[{commit.author.login}]({commit.author.url})** ({commit.author.name}):"]
            elif commit.committer:
                log_string += [f"by **{commit.committer.name}**:"]
            else:
                log_string += ["was generated automatically:"]
            log_string += [f"{commit.commit.message}."]
            log_string = " ".join(log_string)

            stats_string = f"_Stats: {commit.stats.additions} lines added, {commit.stats.deletions} lines removed_."
            print("\n".join([log_string, stats_string, ""]))
