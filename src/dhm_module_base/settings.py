import configparser
import os


class Configuration(object):
    """Instantiate a Configuration object."""

    ENVS = ["local", "dev", "prod"]
    cwd = os.path.dirname(__file__)
    # If the configuration is local to the module, put it here.
    default_config = os.path.join(cwd, "configs", "config.ini")
    if not os.path.exists(default_config):
        default_config = os.path.join(cwd, "configs", "dummy.ini")

    def __init__(self, env="dev", path=default_config):
        """__init__.

        Args:
            env (str): env to use for connections etc
            path (str): Path to configuration file, allows to overwrite the default configuration
        """
        self.config = configparser.ConfigParser()
        self.env = env
        self.path = path

    @property
    def env(self):
        """Env section to use for connections."""
        return self.env

    @env.setter
    def env(self, env):
        """Validator for env.

        Args:
            env (str): Environment to use, accepted values are local | dev | prod

        Raises:
            ValueError: Raised if env is not in list
        """
        if env in self.ENVS:
            # pylint: disable=attribute-defined-outside-init
            self._env = env
        else:
            raise ValueError(
                "%s not in accepted values %s" % (str(env), str(self.ENVS))
            )

    @property
    def path(self):
        """Configuration file path."""
        return self._path

    @path.setter
    def path(self, path):
        """Validator for path.

        Args:
            path (str): Path to configuration file

        Raises:
            FileNotFoundError: If configuration file is not found
        """
        if os.path.exists(path):
            # pylint: disable=attribute-defined-outside-init
            self._path = path
            self.config.read(path)
        else:
            raise FileNotFoundError("File %s not found" % path)
