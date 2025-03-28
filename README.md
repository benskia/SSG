# Static Site Generator

This program parses markdown content and uses provided static files to build a
static site.

[TOC]

## Installation

1. [Download and install Python](https://www.python.org/downloads/)
2. Clone this repo

## Usage

The program expects markdown to follow [Google's Markdown Style Guide](https://google.github.io/styleguide/docguide/style.html)

It can accept a single arg to configure the server's base path. For Github
Pages, this is typically the name of the repo. If no path is given, the
default, "/", is used.

For example, this deployment uses `python3 main.py SSG`.

Currently, the static site files get built in `[project root]/docs/`. This is a
common path where Github Pages serves static sites - selected from a dropdown
in the repo's Settings -> Pages configuration.
