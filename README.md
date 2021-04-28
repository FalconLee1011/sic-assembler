# SIC Assembler
![bugs](https://img.shields.io/badge/Bugs-A_lot-orange?&style=flat-square&logo=stackoverflow&logoColor=white) 

Overview
---
A bug-filled SIC Assembler by 草

Requirements
---
- [pyenv](https://github.com/pyenv/pyenv) (optional)
- [pipenv](https://github.com/pypa/pipenv) with python 3.9 or above

Usage
---
### Dive into the code
- Entry -> `main()` in `__main__.py`

### Setup
- Clone the repo.
- Install dependencies.
  ```sh
  pipenv install
  ```

### Usage
- To compile SIC assembly
  ```sh
  pipenv run assemble -s <source> -o <output>
  ```
  - Example
    ```sh
    pipenv run assemble -s ./examples/test.asm -o ./examples/test.obj
    ```
- To Get help
  ```sh
  pipenv run assemble -h
  ```
