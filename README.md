# LinkedIn Bot

Automatically connect with people on LinkedIn, for your business, or for meeting new people.

## Features

- Provide a JSON file of people you want to connect with
- Scrape & Connect with people, all in one go
- Automatically send a message to the people you connect with

## Installation

Use `git` to clone the repository.

```bash
git clone https://github.com/FujiwaraChoki/linkedin-bot.git
```

Then, install the dependencies.

```bash
pip install -r requirements.txt
```

## Usage

> Before running the bot, make sure you have a Firefox profile with your LinkedIn account logged in.

> Also, tweak the parameters in the `src/main.py` file to your liking, for example due to your language.

To show the help message, run the following command.

```bash
python src/main.py --help
```

To run the bot, follow this template:

```bash
python src/main.py --profile {str} (Path to your Firefox profile) [OPTIONAL: --headless, --query {str} (Your search query (or your niche)), --people (Where your JSON file is located), --n {num} (Amount of people you want to connect with, if not supplied, default 30 is used)]
```

### Example JSON-File

```json
[
  {
    "pfp": "",
    "name": "",
    "profile_url": "",
    "subtitle": "",
    "secondary_subtitle": "",
    "summary": ""
  },
  ...
]
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

## Author

- [FujiwaraChoki](https://github.com/FujiwaraChoki)
