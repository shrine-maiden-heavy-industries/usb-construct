# Contribution Guidelines

> **Note** Contributions that were generated in whole or in-part from any
> language model or AI, such as GitHub Copilot, ChatGPT, BARD, or any other such tool
> are explicitly forbidden and will result in your permanent ban from contributing
> to this project.

## Contributing

Contributions to usb-construct are released under the [BSD-3-Clause](./LICENSE) license.

Please note that usb-construct is released with a [Contributor Code of Conduct](./CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Development and Testing

Ensure to install [nox](https://nox.thea.codes/), like so:

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
