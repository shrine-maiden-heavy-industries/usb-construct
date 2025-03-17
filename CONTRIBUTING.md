# Contribution Guidelines

## Contributing

Contributions to usb-construct are released under the [BSD-3-Clause] license.

Please note that usb-construct is released with a [Contributor Code of Conduct]. By participating in this project you agree to abide by its terms.

## Development and Testing

Ensure to install [nox], like so:

```
$ pip install nox
```

General testing and linting of usb-construct is done with nox, as such there are some session names to know about:

* `test` - Run the test suite
* `lint` - Run the linter
* `typecheck` - Run the type-checker

Bye default these are configured to run one right after another when invoking `nox` with no arguments, to run a single check, you can run it with passing `-s <session>` to nox, like so:

```
$ nox -s lint
```

## Use of Generative AI

This project explicitly does not allow any contributions that were generated in whole or in-part by large language models (LLMs), chatbots, or image generation systems. This ban includes tools, including but not limited to Copilot, ChatGPT, Claude, DeepSeek, Stable Diffusion, DALL-E, Midjourney, or Devin AI.

This policy covers all parts of the project, including, but not limited to code, documentation, issues, artworks, comments, discussions, pull requests, and any other contributions to usb-construct, without exception.

> [!NOTE]
> It is also recommended to avoid any and all AI tools when asking questions about usb-construct,
> prefer the documentation when available, as well as things such as the discussion forum, or IRC channel.
> These tools often fabricate plausible sounding information that is entirely incorrect, or often subtly
> incorrect and pass it off with confidence, thus misleading.

[BSD-3-Clause]: ./LICENSE
[Contributor Code of Conduct]: ./CODE_OF_CONDUCT.md
[nox]: https://nox.thea.codes/
