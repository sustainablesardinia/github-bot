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
import abc


class LanguageFormatter:
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, '_get_month_name') and callable(subclass._get_month_name) and
                hasattr(subclass, 'print_post_title') and callable(subclass.print_post_title) and
                hasattr(subclass, 'print_post_description') and callable(subclass.print_post_description) and
                hasattr(subclass, 'print_post_beginning') and callable(subclass.print_post_beginning) and
                hasattr(subclass, 'print_repo_header') and callable(subclass.print_repo_header) and
                hasattr(subclass, 'print_commit_header') and callable(subclass.print_commit_header) and
                hasattr(subclass, 'print_commit_committer') and callable(subclass.print_commit_committer) and
                hasattr(subclass, 'print_commit_author') and callable(subclass.print_commit_author) and
                hasattr(subclass, 'print_automatic_commit') and callable(subclass.print_automatic_commit) and
                hasattr(subclass, 'print_commit_stats') and callable(subclass.print_commit_stats) and
                hasattr(subclass, 'get_file_name') and callable(subclass.get_file_name) or
                NotImplemented)

    def __init__(self, language):
        self.language = language

    @abc.abstractmethod
    def _get_month_name(self, month_number):
        raise NotImplementedError

    def _date_string(self, today):
        date_format = today.date()
        day = today.day
        month = self._get_month_name(date_format)
        year = today.year
        return f"{day} {month} {year}"

    @abc.abstractmethod
    def print_post_title(self):
        raise NotImplementedError

    @abc.abstractmethod
    def print_post_description(self):
        raise NotImplementedError

    @abc.abstractmethod
    def print_post_beginning(self):
        raise NotImplementedError

    @abc.abstractmethod
    def print_repo_header(self, full_name, url):
        raise NotImplementedError

    @abc.abstractmethod
    def print_commit_header(self, sha, url, date):
        raise NotImplementedError

    @abc.abstractmethod
    def print_commit_committer(self, name):
        raise NotImplementedError

    @abc.abstractmethod
    def print_commit_author(self, login, url, name):
        raise NotImplementedError

    @abc.abstractmethod
    def print_automatic_commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def print_commit_stats(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_file_name(self):
        raise NotImplementedError


class EnglishFormatter(LanguageFormatter):
    def __init__(self):
        super().__init__("en")

    def _get_month_name(self, today):
        return today.strftime("%B")

    def print_post_title(self, today):
        return f"What's happening within Sustainable Sardinia? Update as of {super()._date_string(today)}"

    def print_post_description(self):
        return "An overview of what was done in the projects within Sustainable Sardinia in the past month."

    def print_post_beginning(self):
        return "Another month has passed, and more work was done on the projects within Sustainable Sardinia. Let's have a look at the activity of the past 30 days."

    def print_repo_header(self, full_name, url):
        return f"## Work in [{full_name}]({url})"

    def print_commit_header(self, sha, url, date):
        return f"[{sha}]({url}) on {date}"

    def print_commit_committer(self, name):
        return f"by **{name}**"

    def print_commit_author(self, login, url, name):
        return f"by **[{login}]({url})** ({name})"

    def print_automatic_commit(self):
        return "was generated automatically"

    def print_commit_stats(self, additions, deletions):
        return f"_Stats: {additions} lines added, {deletions} lines removed_."

    def get_file_name(self):
        return "what-happening"


class SardinianFormatter(LanguageFormatter):
    def __init__(self):
        super().__init__("srd")

    def _get_month_name(self, today):
        month_number = today.month
        month_names = ["Gennàrgiu", "Friàrgiu", "Martzu", "Abrili", "Maju", "Làmpadas",
                       "Argiolas", "Austu", "Cabudanni", "Ladàmini", "Donniasantu", "Idas"]
        return f"de {month_names[month_number-1]}"

    def print_post_title(self, today):
        return f"Ita ant fatu in Sustainable Sardinia? Sceda finsas a su {super()._date_string(today)}"

    def print_post_description(self):
        return "Un' arresumu de su chi ant fatu in is fainas de Sustainable Sardinia in su mesi passau."

    def print_post_beginning(self):
        return "Un' àteru mesi est passau, e prus traballu puru dd' ant portau innantis in Sustainable Sardinia. Andaus a biri su chi ant fatu de 30 diis a oi."

    def print_repo_header(self, full_name, url):
        return f"## Traballu in [{full_name}]({url})"

    def print_commit_header(self, sha, url, date):
        return f"[{sha}]({url}) su {date}"

    def print_commit_committer(self, name):
        return f"fatu de **{name}**"

    def print_commit_author(self, login, url, name):
        return f"fatu de **[{login}]({url})** ({name})"

    def print_automatic_commit(self):
        return "dd' ant ingenerau de manera automàtica"

    def print_commit_stats(self, additions, deletions):
        return f"_Statìsticas: {additions} lìnias de còdixi aciuntas, {deletions} lìnias de còdixi bogadas_."

    def get_file_name(self):
        return "ita-fatu"


class ItalianFormatter(LanguageFormatter):
    def __init__(self):
        super().__init__("it")

    def _get_month_name(self, today):
        month_number = today.month
        month_names = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
                       "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
        return f"{month_names[month_number-1]}"

    def print_post_title(self, today):
        return f"Cosa è stato fatto in Sustainable Sardinia? Aggiornamento fino all {super()._date_string(today)}"

    def print_post_description(self):
        return "Un riassunto di ciò che è stato fatto nei progetti di Sustainable Sardinia nello scorso mese."

    def print_post_beginning(self):
        return "Un altro mese è passato, e altro lavoro è stato portato avanti nei progetti di Sustainable Sardinia. Andiamo a vedere ciò che è stato fatto negli ultimi 30 giorni:"

    def print_repo_header(self, full_name, url):
        return f"## Lavoro su [{full_name}]({url})"

    def print_commit_header(self, sha, url, date):
        return f"[{sha}]({url}) il {date}"

    def print_commit_committer(self, name):
        return f"di **{name}**"

    def print_commit_author(self, login, url, name):
        return f"di **[{login}]({url})** ({name})"

    def print_automatic_commit(self):
        return "è stato generato automaticamente"

    def print_commit_stats(self, additions, deletions):
        return f"_Statistiche: {additions} linee di codice aggiunte, {deletions} linee di codice rimosse_."

    def get_file_name(self):
        return "cosa-fatto"


class FileWriter():
    def __init__(self, formatter: LanguageFormatter, repo, today: datetime.datetime):
        self.formatter = formatter
        self.commit_count = 0
        self.repo = repo
        self.file_content = ""
        self.today = today.date()

    def _add_line(self, line):
        self.file_content += line + "\n"

    def _add_newline(self):
        self.file_content += "\n"

    def print_header(self, today):
        self._add_line("---")
        self._add_line(f"title: {self.formatter.print_post_title(today)}")
        self._add_line(f"image: /assets/images/workers.webp")
        self._add_line(
            f"description: {self.formatter.print_post_description()}")
        date_string = str(today.date())
        self._add_line(f"reference: activity_{date_string.replace('-', '_')}")
        self._add_line("---")
        self._add_newline()
        self._add_line(self.formatter.print_post_beginning())
        self._add_newline()

    def print_repo(self, repo):
        print(f"Reading repo {repo.full_name}")
        self._add_line(self.formatter.print_repo_header(
            repo.full_name, repo.html_url))
        self._add_newline()

    def print_commit(self, commit):
        self.commit_count += 1

        commit_sha = str(commit.sha)[0:6]
        print(f"Reading commit {commit_sha}")
        log_string = [self.formatter.print_commit_header(
            commit_sha, commit.html_url, commit.commit.committer.date)]

        if commit.author:
            log_string += [self.formatter.print_commit_author(
                commit.author.login, commit.author.html_url, commit.author.name)]
        elif commit.committer:
            log_string += [self.formatter.print_commit_committer(
                commit.committer.name)]
        else:
            log_string += [self.formatter.print_automatic_commit()]
        log_string[-1] += ":"

        log_string += [f"{commit.commit.message}"]
        self._add_line(" ".join(log_string))

        self._add_newline()
        self._add_line(self.formatter.print_commit_stats(
            commit.stats.additions, commit.stats.deletions))
        self._add_newline()

    def commit_new_post(self, is_debug_mode=False):
        file_name = str(self.today) + "-" + \
            self.formatter.get_file_name() + "-" + str(self.today) + ".md"
        post_path = "/".join([self.formatter.language, "_posts", file_name])
        post_message = f"Adding update post for {self.today} (Language: {self.formatter.language})"
        print(f"Committing {post_path} with message: {post_message}")
        if is_debug_mode:
            print(self.file_content)
        else:
            self.repo.create_file(post_path, post_message, self.file_content)


def _print_post(today, writer, organization):
    writer.print_header(today)

    for repo in organization.get_repos():
        commits = repo.get_commits()

        if commits:
            writer.print_repo(repo)

        for commit in commits:
            commit_date = commit.commit.committer.date
            if (today-commit_date).days > 30:
                continue
            writer.print_commit(commit)


if __name__ == "__main__":
    github = Github(sys.argv[1])
    organization = github.get_organization("sustainablesardinia")
    if len(sys.argv) > 2:
        today = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d")
    else:
        today = datetime.datetime.today()
    print(f"Date is: {today}")
    is_debug_mode = False
    if len(sys.argv) > 3 and "debug" in sys.argv[3]:
        is_debug_mode = True
        print("Running in debug mode")

    write_repo = github.get_repo(
        "sustainablesardinia/sustainablesardinia.github.io")

    writers = [FileWriter(EnglishFormatter(), write_repo, today),
               FileWriter(SardinianFormatter(), write_repo, today),
               FileWriter(ItalianFormatter(), write_repo, today)]

    commit_count = 0
    for writer in writers:
        _print_post(today, writer, organization)
        commit_count += writer.commit_count

    if commit_count > 0:
        for writer in writers:
            writer.commit_new_post(is_debug_mode)
