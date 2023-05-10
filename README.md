# Ethupdate

`Ethupdate` is a Python command-line tool for updating multiple Ethereum client repositories with upstream changes.

Its essentially a fast way to fetch all the upstream changes and merge them with your forked client repos. For me this is a sanity check to make sure I always stay up to date.

## Requirements

Before using `Ethupdate`, currently you must have forked the following Ethereum client repositories on GitHub:

-   [erigon](https://github.com/ledgerwatch/erigon)
-   [ethereumjs](https://github.com/ethereumjs/ethereumjs-monorepo)
-   [evmone](https://github.com/ethereum/evmone)
-   [besu](https://github.com/hyperledger/besu)
-   [nethermind](https://github.com/NethermindEth/nethermind)
-   [go-ethereum](https://github.com/ethereum/go-ethereum)

To mitigate the requirement for all these repos you can remove them within the `FORKED_REPOS` list within `ethup/__init__.py`.

This package assumes you have all your ethereum client forked repos in one folder or directory, or intend to.

## Installation

First clone `Ethupdate`, you can follow these steps:

```bash
git clone https://github.com/spencer-tb/Ethupdate.git
cd ethupdate
```

Next you will need to first set the following lines within `ethup/__init__.py`.

```python
# This should be an absolute path, the location of all your clients.
REPO_PATH = '/path/to/your/local/repos'

# Generate on GitHub within Settings
#  -> Developer Settings
#  -> Personal Access Tokens
GITHUB_TOKEN = '<your_github_token>'

GITHUB_USER = '<your_user_name>'
```

Finally you can install `Ethupdate` using pip:

```bash
cd ethupdate
pip install .
```

## Usage

After installation the `ethup` package should be executable from your Path.

To update (fetch upstream and merge it with your forked master/main) for all the clients you can simply run:

```
ethup
```

If you want to do this for a specific clients you can run:

```
ethup --clients go-ethereum besu erigon
```

To specify a path manually you can use the `--path` flag.

Note that if you specify an empty directory, the tool with clone and update with upstream for every client specified in `FORKED_REPOS`.

If you want to add more clients to the list, you can modify the `FORKED_REPOS` variable in `ethup/__init__.py`.

## Contributing

If you would like to contribute, you can fork the repository and submit a pull request. You can also open an issue if you find a bug or have a suggestion for a new feature.
