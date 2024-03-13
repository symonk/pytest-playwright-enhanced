import functools
import pathlib
import tempfile


@functools.lru_cache(maxsize=1)
def cached_invocation_artifact_dir() -> pathlib.Path:
    """Generates a temporary directory for storing artifacts of this
    particular run.  These are unique per execution and any xdist
    workers will also share this same directory.

    artifacts that will reside in here are:
        * video artifacts
        * screenshot artifacts
        * trace artifacts
        * Any downloaded files throughout the run (Todo: Allow these to persist outside driver ctx).

    # Todo: Figure out persistence.
    """
    return tempfile.TemporaryDirectory(prefix="playwright-enhanced")
