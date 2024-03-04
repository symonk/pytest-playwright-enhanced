## Contribution

----

Currently `pytest-playwright-enhanced` supports ease of development on a `linux` based environment, however
pull requests to enable testing on `windows` and `mac OSX` would be greatly appreciated.


## Towncrier

All changes should have a corresponding github `issue`.  For each issue, use `towncrier create --content <message> <issue>.<type>.rst`.
This allows us to create an automatic `changelog` for each release.  Refer to:

https://towncrier.readthedocs.io/en/stable/tutorial.html

If `towncrier` is new to you.  The generated files reside in `changes/*`.

For building the change log, `tox -e changelog` is available.

----