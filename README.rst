sendbox_sdk
===========

.. image:: https://img.shields.io/pypi/v/sendbox_sdk.svg
    :target: https://pypi.python.org/pypi/sendbox_sdk
    :alt: Latest PyPI version


SDK for Mail.ru Sendbox rest api

Usage
-----

.. code-block:: python

    from sendbox_sdk.api import SendBoxApi

    sendbox_api = SendBoxApi("sendbox_account_id", "sendbox_account_secret")
    sendbox_api.send_templated_email(
        context={
            'template_parameter1': 'test',
            'template_parameter2': 'test',
        },
        from_email='test@example.come',
        from_name="Example",
        to_email='user@example.com',
        to_name="Username",
        subject="Subject"
    )


Installation
------------

Requirements
^^^^^^^^^^^^
requests

Compatibility
-------------

Licence
-------
MIT

Authors
-------

`sendbox_sdk` was written by `Yasha Mikhoparkin <ja.mix@mail.ru>`_.
