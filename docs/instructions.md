# Instructions

todo

### Table of Contents
- [Setup](#setup)


## Setup

1. Clone the [repo](https://github.com/immone/ohtuprojekti-2022/tree/dev)
```bash
git clone git@github.com:immone/ohtuprojekti-2022.git
````
2. Install dependencies
```bash
poetry install
````
3. Build
```bash
poetry run invoke build
```

# Usage
- Interactive mode
    ´´´bash
    poetry run invoke start
    ````
- Run command once with optional flag
    ```bash
    poetry run invoke start -a[dd -d[elete] -e[dit] -l[ist] -s[earch] -b[ibtex] -h[elp]
    ```

## Testing

- Run tests
    ```bash
    poetry run invoke test
    ```
- Generate coverage report
    ```bash
    poetry run invoke coverage-report
    ```
- Perform pylint code quality inspection
    ```bash
    poetry run invoke lint
    ```
- Execute autopep8 format
    ```bash
    poetry run invoke format
    ```
