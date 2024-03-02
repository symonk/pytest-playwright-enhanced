<img src="https://github.com/symonk/pytest-playwright-enhanced/blob/main/.github/images/logo.png" border="1" width="275" height="275">

![version](https://img.shields.io/pypi/v/pytest-playwright-enhanced?color=%2342f54b&label=&style=flat-square)
[![codecov](https://codecov.io/gh/symonk/pytest-playwright-enhanced/branch/main/graph/badge.svg)](https://codecov.io/gh/symonk/pytest-playwright-enhanced)
[![docs](https://img.shields.io/badge/documentation-online-brightgreen.svg)](https://symonk.github.io/pytest-playwright-enhanced/)


### pytest-playwright-enhanced


> [!CAUTION]
> `pytest-playwright-enhanced` is in the alpha stage.


`pytest-playwright-enhanced` is a batteries included `pytest` plugin for the `playwright` python bindings that 
offers extended functionality with a focus on removing boilerplate code for projects that wish to test modern 
web applications and APIs. `pytest-playwright-enhanced` plans to offer the following:

 * Automatic, browser management and installation if required.
 * Improved, human readable APIs that build on top of playwrights API.
 * Improved artifacting and debugability.
 * `Asynchronous` support.
 * Custom `hooks` to allow you to plugin and modify behaviour at runtime.
 * Much More...

 `pytest-playwright-enhanced` is currently implementing core plugin functionality, the main enhancements
 will follow shortly.

-----

## Quick Start

Quickly get running by doing the following:

* `pip install pytest-playwright-enhanced`
* `pytest <posargs> --acquire-binaries=with-deps`

-----


## Fixtures

-----

`playwright` - At present this returns the sync `Playwright` instance.
`pw_multi_browser` - Automatically run a test on `chromium`, `firefox` and `webkit`.


-----


## Hooks

`pytest_playwright_acquire_binaries` - Hook in and customise binary acquisition at runtime.


-----

## Markers

`pytest.mark.only_on_browsers` - Only run on a subset of browsers when using the `pw_multi_browser` fixture.

----- 
