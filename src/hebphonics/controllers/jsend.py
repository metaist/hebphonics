#!/usr/bin/env python
# coding: utf-8
"""Standard JSON responses."""

# <dict> shorthand
# pylint: disable=invalid-name
_del = dict.__delitem__
_get = dict.__getitem__
_in = dict.__contains__
_set = dict.__setitem__
_getattr = object.__getattribute__
_setattr = object.__setattr__

# Response status
STATUS_SUCCESS = "success"
STATUS_FAIL = "fail"
STATUS_ERROR = "error"


class JSend(dict):
    """Service response object.

    This object loosly conforms to the JSend specification:
    <https://labs.omniti.com/labs/jsend>
    """

    def __init__(self, *args, **kwargs):
        """Construct a response.

        Examples:
            >>> result = JSend()
            >>> result.ok
            True
            >>> result.status == 'success'
            True
            >>> result.data is None
            True
            >>> result == {'ok': True, 'status': 'success', 'data': None}
            True
        """
        self.update(ok=True, status=STATUS_SUCCESS, data=None)
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """Set the value of an attribute.

        Args:
            name (str): name of the attribute
            value (any): value to set

        Examples:
            >>> item = JSend()
            >>> item.a = 1
            >>> item['a'] == 1
            True
            >>> object.__setattr__(item, 'b', 2)
            >>> item.b = 3
            >>> item.b == 3
            True
        """
        try:
            _getattr(self, name)
            _setattr(self, name, value)
        except AttributeError:
            self[name] = value

    def __getattr__(self, name):
        """Return the value of the attribute.

        Args:
            name (str): name of the attribute

        Returns:
            (any): value of the attribute, or None if it is missing

        Examples:
            >>> item = JSend(a=1)
            >>> item.a == 1
            True
        """
        return self[name]

    def __delattr__(self, name):
        """Delete the attribute.

        Args:
            name (str): name of the attribute

        Examples:
            >>> item = JSend(a=1, b=2)
            >>> del item.a
            >>> item.a is None
            True
        """
        del self[name]

    def __setitem__(self, name, value):
        """Set the value of a key.

        Args:
            name (str): name of the key
            value (any): value to set

        Examples:
            >>> item = JSend()
            >>> item['a'] = 1
            >>> item.a == 1
            True
        """
        _set(self, name, value)

    def __getitem__(self, name):
        """Return the value of the key.

        Args:
            name (str): name of the key

        Returns:
            (any): value of the key, or None if it is missing

        Examples:
            >>> item = JSend(a=1)
            >>> item['a'] == 1
            True
        """
        result = None
        if _in(self, name):
            result = _get(self, name)
        return result

    def __delitem__(self, name):
        """Delete a key.

        Args:
            name (str): name of the key

        Examples:
            >>> item = JSend(a=1, b=2)
            >>> del item['a']
            >>> item['a'] is None
            True
        """
        _del(self, name)

    def fail(self, message=None):
        """Indicate a controlled failure.

        Args:
            message (str): human-readable explanation of the failure

        Returns:
            (JSend): self for chaining

        Examples:
            >>> result = JSend()
            >>> msg = 'Missing a phone number.'
            >>> result.fail(msg) is result
            True
            >>> result.ok is False
            True
            >>> result.status == 'fail'
            True
            >>> result.message == msg
            True
        """
        self.update(ok=False, status=STATUS_FAIL, message=message)
        return self

    def error(self, message=None, code=None):
        """Indicate an uncontrolled error.

        Args:
            message (str): human-readable explanation of the error
            code (any): technical indication of the error

        Returns:
            (JSend): self for chaining

        Examples:
            >>> result = JSend()
            >>> msg = 'No such file [file.text].'
            >>> code = 13
            >>> result.error(msg, code) is result
            True
            >>> result.ok is False
            True
            >>> result.status == 'error'
            True
            >>> result.message == msg
            True
            >>> result.code == code
            True
        """
        self.update(ok=False, status=STATUS_ERROR, message=message, code=code)
        return self

    def success(self, data=None):
        """Indicate a successful response.

        Args:
            data (any): response payload

        Returns:
            (JSend): self for chaining

        Examples:
            >>> result = JSend()
            >>> result.success("Works") is result
            True
        """
        self.update(ok=True, status=STATUS_SUCCESS, data=data)
        return self
