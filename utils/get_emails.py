import imaplib
import email
from email.header import decode_header
from email.message import Message
import os
from dotenv import load_dotenv
import random
import re

load_dotenv()


class Email:
    def __init__(self):
        self.email_id = os.getenv("EMAIL_ID")
        self.password = os.getenv("PASS")
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.mail.login(self.email_id, self.password)
        self.mail.select("inbox")
        self.sections = {
            "TLDR Design": [
                "News & Trends",
                "Opinions & Tutorials",
                "Launches & Tools",
                "Miscellaneous",
                "Quick Links",
            ],
            "TLDR Crypto": [
                "Markets & Business",
                "Innovation & Launches",
                "Guides & Tutorials",
                "Miscellaneous",
                "Quick Links",
            ],
            "TLDR AI": [
                "Headlines & Launches",
                "Research & Innovation",
                "Engineering & Resources",
                "Miscellaneous",
                "Quick Links",
            ],
            "TLDR Web Dev": [
                "Articles & Tutorials",
                "Opinions & Advice",
                "Launches & Tools",
                "Miscellaneous",
                "Quick Links",
            ],
            "TLDR Marketing": [
                "News & Trends",
                "Strategies & Tactics",
                "Resources & Tools",
                "Miscellaneous",
                "Quick Links",
            ],
            "TLDR Product": [
                "News & Trends",
                "Opinions & Tutorials",
                "Resources & Tools",
                "Miscellaneous",
                "Quick Links",
            ],
            "TLDR": [
                "Big Tech & Startups",
                "Science & Futuristic Technology",
                "Programming, Design & Data Science",
                "Miscellaneous",
                "Quick Links",
            ],
            "TLDR DevOps": [
                "News & Trends",
                "Opinions & Tutorials",
                "Resources & Tools",
                "Miscellaneous",
                "Quick Links",
            ],
            "TLDR InfoSec": [
                "Attacks & Vulnerabilities",
                "Strategies & Tactics",
                "Launches & Tools",
                "Miscellaneous",
                "Quick Links",
            ],
            "TLDR Founders": [
                "Headlines & Trends",
                "Strategies & Tactics",
                "Tools & Resources",
                "Miscellaneous",
                "Quick Links",
            ],
        }

    def check_topic(self, topic: str):
        for key in self.sections.keys():
            if topic.lower() == key.lower():
                return True
        return False

    def get_topics(self):
        topics = []
        for key in self.sections.keys():
            append_key = key.replace("TLDR ", "")
            if append_key != "":
                topics.append(append_key)

        return topics

    def extract_section_articles(self, email_body, topic: str):
        sections = self.sections[topic]

        # Initialize an empty list to store the articles for each section
        section_articles = {section: "" for section in sections}

        # Extract text between the 2 sections one by one, without taking "Quick Links" as the start
        for i in range(len(sections) - 1):
            index1 = email_body.lower().find(sections[i].lower())
            index2 = email_body.lower().find(sections[i + 1].lower())

            # If both sections are found
            if index1 != -1 and index2 != -1:
                # Slice the string to get the text between the sections
                text = email_body[index1 + len(sections[i]) : index2].strip()
            else:
                text = ""

            # Add the text to the list
            section_articles[sections[i]] = text

        return section_articles

    def extract_articles(self, body: str):
        if body == "":
            return []
        # replace 2 or more newlines with a single newline and single newline with a space
        body = body.replace("\r\n\r\n", "<DOUBLE_NEWLINE>")

        # Replace single newlines with a space
        body = body.replace("\r\n", " ")

        # Replace the placeholder with double newlines
        body = body.replace("<DOUBLE_NEWLINE>", "\r\n\r\n")

        body = re.sub(
            r"(\[\d{1,2}\])\s{0,2}\r\n\r\n",
            r"\1<WITHIN_ARTICLE>",
            body,
        )

        non_alnum_punct_pattern = re.compile(r"[^a-zA-Z0-9\s\.\,\;\:\-\_\!\?]+$")
        body = non_alnum_punct_pattern.sub(r"", body).strip()

        # Split the body into articles by "\r\n\r\n"
        articles = body.split("\r\n\r\n")

        # Initialize an empty list to store the articles
        article_list = []

        for article in articles:
            # Split the article into title and brief by "\r\n\r\n"
            try:
                title = article.split("<WITHIN_ARTICLE>")[0].strip()
                brief = article.split("<WITHIN_ARTICLE>")[1].strip()
            except:
                continue

            # Add the article to the list
            article_list.append({"title": title, "brief": brief})

        return article_list

    def extract_usable_content(self, body: str, topic: str):
        # Split the body into topics
        topics = self.extract_section_articles(body, topic)

        """Return format:
            {
                "section1": [
                    {"title": "title1", "brief": "brief1"},
                    {"title": "title2", "brief": "brief2"},
                    ...
                ],
                "section2": [
                    {"title": "title1", "brief": "brief1"},
                    {"title": "title2", "brief": "brief2"},
                    ...
                ],
                ...
            }
        """

        # Initialize an empty dict to store the articles
        articles = {}

        # Extract the articles for each section
        for section, section_text in topics.items():
            articles[section] = self.extract_articles(section_text)

        return articles

    def get_links(self, body: str):
        # replace 2 or more newlines with a single newline and single newline with a space
        body = body.replace("\r\n\r\n", "<DOUBLE_NEWLINE>")

        # Replace single newlines with a space
        body = body.replace("\r\n", " ")

        # Replace the placeholder with double newlines
        body = body.replace("<DOUBLE_NEWLINE>", "\r\n\r\n")

        links_text = body.split("Links: ------")[1].strip()

        matches = re.findall(r"\[(\d{1,2})\] (https?://[^\s]+)", links_text)

        # Create a dictionary from the matches
        links_dict = {int(key): url for key, url in matches}

        return links_dict

    def extract_mail_body(self, message: Message, topic: str, email_list: dict):
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            try:
                body = part.get_payload(decode=True).decode()
            except:
                pass

            if content_type == "text/plain" and "attachment" not in content_disposition:
                news = self.extract_usable_content(body, topic)
                links = self.get_links(body)
                email_list["topic"] = topic
                email_list["news"] = news
                email_list["links"] = links
                return email_list
        return email_list

    async def get_news(self, topic: str = ""):
        result, data = self.mail.search(None, "ALL")
        email_list = {
            "topic": "",
            "news": {},
        }
        counter = 0
        randint = random.randint(0, len(self.sections.keys()) - 1)
        for num in data[0].split()[::-1]:
            if email_list["news"] != {}:
                break

            if counter < randint and topic == "":
                counter += 1
                continue

            result, data = self.mail.fetch(num, "(RFC822)")
            raw_email = data[0][1]
            raw_email_string = raw_email.decode("utf-8")
            email_message = email.message_from_string(raw_email_string)
            subject = email_message["Subject"]
            From = email_message["From"]
            email_topic = From.split("<")[0].strip()
            if "tldr" in From.lower():
                if topic != "" and topic.lower() not in email_topic.lower():
                    continue
                if email_message.is_multipart():
                    email_list = self.extract_mail_body(
                        email_message, email_topic, email_list
                    )
        return email_list
