# SNMPy

SNMPy is a Python-based email sending tool that allows you to send emails using various email providers such as Google, Yahoo, and Microsoft. It supports both CLI (Command Line Interface) and GUI (Graphical User Interface) modes.

## Features

* Send emails using various email providers
* Supports both CLI and GUI modes
* Option to save credentials for future use
* Option to load email list from a file
* Option to load email content from a file
* Customizable email server and port
* Customizable email sender name, subject, and body
* Supports HTML, Markdown, and plain text email content
* Customizable delay between emails

## Installation

To install the required dependencies, run the following command:

```
pip install -r requirements.txt
```

This will install the required packages such as `smtplib`, `tkinter`, `ttkthemes`, `markdown`, and `argparse`.

## Usage

### CLI Mode

To run the program in CLI mode, open a terminal and navigate to the directory where the `main.py` file is located. Then, run the following command:

```css
python main.py -cli
```

The program will prompt you to enter the email server, port, email address, password, sender name, recipient email addresses, subject, and email body.

### GUI Mode

To run the program in GUI mode, double-click on the `main.py` file or run the following command in a terminal:

```bash
python main.py
```

The program will open a window where you can enter the email server, port, email address, password, sender name, recipient email addresses, subject, and email body. You can also choose to save your credentials for future use, load an email list from a file, and load email content from a file.

### Installation

The minimal size of the project (two .py files) makes it easy to setup and run as anything you need. Dockerize it, make it a webapp on the cloud, run it on your own machine. As long as the two scripts are on the same folder, they can be installed as anything anywhere once Python and the requirements are installed.

## Email Server and Port

By default, the program supports the following email providers:

* Google (smtp.gmail.com, port 587)
* Yahoo (smtp.mail.yahoo.com, port 465)
* Microsoft (smtp.office365.com, port 587)

You can choose one of these providers from the dropdown menu or enter a custom server and port.

## Saving Credentials

If you choose to save your credentials, the program will create a `.env` file in the same directory as the `main.py` file. The `.env` file will contain your email server, port, email address, and password. The next time you run the program, it will automatically load your saved credentials.

## Loading Email List

You can load a list of recipient email addresses from a text or CSV file. To do this, click on the "Load Email List" button and select the file you want to use. The program will extract the email addresses from the file and add them to the "To Email(s)" field.

## Loading Email Content

You can load email content from an HTML, Markdown, or plain text file. To do this, click on the "Load File" button and select the file you want to use. The program will load the file content and add it to the "Body" field.

## Customizable Delay

You can customize the delay between sending emails by entering a value in the "Delay between emails (seconds)" field. This can be useful if you are sending a large number of emails and want to avoid being flagged as spam.

## Stored Data

The data stored by the e-mail generator is saved under the ``sent.json`` file. This file contains the usernames (beginning of e-mail address before the @) and the ID and timestamp of all e-mails sent to them through the program.

The server stores its data in the ``savedata.json`` file, which is used to pair users with the e-mail IDs they clicked on. Nothing else is saved.

## API

The API of the ``server.py`` script only has a single endpoint that is referenced in all sent mails that use official ReEnforced templates. The link in those e-mails contains a part of the target's e-mail address and the unique ID that was assigned to that mail. When called, the API checks that the user was sent e-mails by the client in the past, and that the ID is valid, at which point it is attached to the user.

This is essentially gaining one "point". The amount of successful phishing attacks egals the amount of IDs attached to a particular user.

The API and script both default to the ``127.0.0.1`` address and ``9900`` port. These can easily be changed within the scripts to whatever suits your needs.

## Formations

Formations are hand-crafted from either templates given by the client company or the findings of what worked on certain employees multiple times. We can check exactly which emails were responsible for an increase in score thanks to their attached timestamp, which lets us filter which e-mail is responsible for it.

## Conclusion

SNMPy is a powerful and easy-to-use email sending tool that supports various email providers, customizable email content, and a user-friendly interface. Whether you prefer using the CLI or GUI mode, SNMPy has got you covered.