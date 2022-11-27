# akamai-monitor
Receive Telegram message when the Akamai script changed.

## Settings

An example of settings is available in [settings.example.json](settings.example.json)

```json
{
	"delay": 3600,
	"target": "https://zalando.fr/login",

	"telegram": {
		"bot-token": "Your telegram bot token here.",
		"chat-id": "Your telegram chat id here."
	}
}
```

* `delay` : The delay between checks, in seconds.
* `target` : The full url of your target. It will follow redirects.
* `telegram.bot-token` : The bot token of your bot provided by BotFather.
* `telegram.chat-id` : The chat id of your telegram group/channel to receive updates.
