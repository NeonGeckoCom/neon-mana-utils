# Neon Mana
Neon Mana (Messagebus Application for Neon AI) provides tools for interacting with 
the [MessageBus](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/message-bus).

Install the Mana utilities Python package with: `pip install neon-mana-utils`
The `mana` entrypoint is available to interact with a bus via CLI. Help is available via `mana --help`.

## Configuration
The default behavior of Mana is to connect to the default core bus (`ws://0.0.0.0:8181/core`). The connection can be 
configured for all `mana` commands via:

```shell
mana configure-messagebus --host "192.168.1.100" --port 18181
```
* `--host` specifies the host URL or IP address
* `--port` specifies the port the `MessageBus` is running on

Any unspecified arguments will use default values.

All configurations can be printed to the terminal with:

```shell
mana print-config
```

## Monitoring
Mana can connect to a messagebus and log all `Message` objects sent on that bus.

```shell
mana tail-messagebus --format
```
* `--format` flag formats serialized messages printed to the shell

### Filtering Messages by type
`--include` and `--exclude` arguments may be passed to include or exclude messages 
with `msg_type` matching specified prefixes. Global filters may be specified in: 
`${XDG_CONFIG_HOME}/mana/filters.yml`. An example filter file is included here:

```yaml
include:
  - recognizer_loop
exclude:
  - "recognizer_loop:utterance"
```

The spec above would log any `Message`s that start with `recognizer_loop`, except
messages with type `recognizer_loop:utterance`.

### Monitoring other MessageBusses
`--host`, `--port`, `--route`, and `--ssl` may be specified to monitor a different 
messagebus without changing the configured bus that is used for other commands. A 
common use case would be to monitor the GUI bus while interacting with the core bus.

## Sending Messages
There are several commands available to interact with a connected Core.

### `send-message`
Send an arbitrary `Message` over the `MessageBus`. The specified file should be a json or yaml
serialized message. `--response` may optionally define a response message type to wait for and print to the terminal.

### Basic Commands
These are commands supported by Mycroft and all derivative cores; they replicate some of
the commands originally found in [mycroft-core/bin](https://github.com/MycroftAI/mycroft-core/tree/e6fe1bbc8affd2f7b22455dc21539ee6725fb45b/bin).

#### `listen`
Send a `mycroft.mic.listen` Message.

#### `stop`
Send a `mycroft.stop` Message.

#### `say-to`
Send a `recognizer_loop:utterance` Message to skills for processing. This sends a minimal message that is
not sufficient for testing user profiles or multi-user cores.

#### `speak`
Send a `speak` Message to TTS for generation and playback

### Messagebus API
These commands are currently specified for `neon-core` only and are not supported 
by other cores. Work is ongoing to standardize these entrypoints across projects.

#### `get-stt`
Send a `neon.get_stt` Message and print the returned Message with transcriptions.
This will only work under NeonCore.

#### `get-tts`
Send a `neon.get_tts` Message and print the returned Message with a path to generated TTS.
This will only work under NeonCore.

#### `get-response`
Send a `recognizer_loop:utterance` Message with the appropriate context to return a `klat.shout` response.
This will only work under NeonCore and will likely be refactored to reflect NeonCore changes.
