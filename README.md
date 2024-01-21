# LinkedIn Bot

Automatically connect with people on LinkedIn, for your business, or for meeting new people.

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

```bash
python src/main.py --profile (Path to your Firefox profile) [OPTIONAL: --headless, --people (Where your JSON file is located)]
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

[MIT](https://choosealicense.com/licenses/mit/)

## Author

- [FujiwaraChoki](https://github.com/FujiwaraChoki)

```

```
