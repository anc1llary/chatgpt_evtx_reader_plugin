# chatgpt_evtx_reader_plugin
 This plugin parses and reads EVTX files providing enrichment for digital forensics and incident response.

## Disclaimer

Data you put into ChatGPT **is not private**.  The nature of logs like this will almost always cause concern for privacy.  Consider this plugin a proof-of-concept of what is possible and where we're headed with AI.  Only use this plugin in circumstances where you do not care if someone else could potentially have access to the data you are sending.

## Installation

- Install poetry by running the command: ```pip3 install poetry```
- Install the project by running: ```poetry install``` inside the main directory of the project.
- Start the project by running: ```poetry run start```
- Access chat.openai.com and select 'alpha', click either 'no plugins enabled' or if you have them enabled, click the icon to present the plugins installed.
- Access the plugin store, on the bottom right, click 'Develop your own plugin'.
- Point ChatGPT to http://localhost:9001 (default settings) or where you are hosting the application.

## Usage

- Add the evtx files you want to work with into the evtx folder included in the project.
- Use the following prompt or variations of it to allow ChatGPT to trigger the parsing function:

```
I have the file [evtx file name here] in the evtx folder ready to be parsed by evtx reader plugin please initiate it.

start date
2022-01-01 00:00:00.000
end date
2022-01-01 00:00:00.000
```

The start and end date is not necessary but is recommended explained in limitations.

## Prompts

- Give me events that are commonly associated with [insert MITRE technique here].
- List process execution events.
- Display events through [start time] and [end time] (note: these must be timestamps with millisecond precision as shown above).

## Limitations

- The EVTX parsing library does not always parse the date properly, causing date boundaries to not properly work.
- The token limitation with ChatGPT will limit the scope of how you can search a large EVTX file.
- GPT4 has a limitation of requests every 3 hours which substantially limits the usage of plugins in general.

## Changelog

- Create a check for errors with date-time and default to the nearest date that is in proper format.
- Implement Local LLM  and create functionality to parse larger event logs into blocks.
