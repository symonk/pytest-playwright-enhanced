<img src="https://github.com/symonk/pytest-playwright-enhanced/blob/main/.github/images/logo.png" border="1" width="275" height="275">

![version](https://img.shields.io/pypi/v/pytest-playwright-enhanced?color=%2342f54b&label=&style=flat-square)
[![codecov](https://codecov.io/gh/symonk/pytest-playwright-enhanced/branch/main/graph/badge.svg)](https://codecov.io/gh/symonk/pytest-playwright-enhanced)
[![docs](https://img.shields.io/badge/documentation-online-brightgreen.svg)](https://symonk.github.io/pytest-playwright-enhanced/)


### pytest-playwright-enhanced

`pytest-playwright-enhanced` is a batteries included `pytest` plugin for the `playwright` python bindings that 
offers extended functionality with a focus on removing boilerplate code for projects that wish to test modern 
web applications and APIs. `pytest-playwright-enhanced` plans to offer the following:

 * Automatic, browser management and installation if required.
 * Improved, human readable APIs that built on top of playwrights API.
 * Improved artifacting and debuggability.
 * `Asynchronous` support.
 * Custom `hooks` to allow you to plugin and modify behaviour at runtime.
 * Much More


> [!CAUTION]
> `pytest-playwright-enhanced` is in the alpha stage.


-----

## Quick Start

Quickly get running by doing the following:

* `pip install pytest-playwright-enhanced`
* `playwright install`

-----


## Fixtures

-----

`playwright` - At present this returns the sync `Playwright` instance.


-----


## Hooks

`pytest_playwright_acquire_binaries` - Hook in and customise binary acquisition at runtime.
