import base64

from typing import List

from .base import ApiBase
from .const import METHOD_PATHS


def get_base_params(subject, from_name, from_email, to_name, to_email,
                    template_id=None, context=None, html=None, text=None):
    """Creates base params for email"""
    params = {
        "email": {
            "subject": subject,
            "from": {
                "name": from_name,
                "email": from_email,
            },
            "to": [
                {
                    "email": to_email,
                    "name": to_name
                }
            ]
        }
    }
    if template_id and context is not None:
        params['email']["template"] = {
            "id": template_id,
            "variables": context
        }
    elif html is not None and text is not None:
        params['email']['html'] = base64.b64encode(html.encode()).decode()
        params['email']['text'] = text
    return params


class SendBoxApi(ApiBase):

    def emails_total(self):
        return self._get_request(METHOD_PATHS.emails_total)

    def emails_id(self, id):
        return self._get_request(METHOD_PATHS.email_info % id)

    def emails_info(self):
        return self._get_request(METHOD_PATHS.emails_info)

    def unsubscribed_users_list(self):
        return self._get_request(METHOD_PATHS.unsubscribe)

    def unsubscribe_user(self, email: str, comment: str = ""):
        return self.unsubscribe_users([email], comment)

    def unsubscribe_users(self, emails: List[str], comment: str = ""):
        request_params = [
            {'email': email, 'comment': comment} for email in emails
        ]
        res = self._post_request(METHOD_PATHS.unsubscribe, request_params)
        return res

    def send_templated_email(self, subject: str,
                             from_email: str, from_name: str,
                             to_email: str, to_name: str,
                             template_id: str, context: dict, ):
        """
        Send email base on template
        :param subject: Email Title
        :param from_email:
        :param from_name:
        :param to_email:
        :param to_name:
        :param template_id:
        :param context: dict of template context variables
        :return:
        """
        params = get_base_params(
            subject=subject,
            template_id=template_id,
            context=context,
            from_name=from_name,
            from_email=from_email,
            to_email=to_email,
            to_name=to_name,
        )
        res = self._post_request(METHOD_PATHS.email_send, params)
        assert res['result']
        return res

    def send_html_email(self, subject: str,
                        from_email: str, from_name: str,
                        to_email: str, to_name: str,
                        html: str, text: str, ):
        """
        Send email base on template
        :param subject: Email Title
        :param from_email:
        :param from_name:
        :param to_email:
        :param to_name:
        :param template_id:
        :param context: dict of template context variables
        :return:
        """
        params = get_base_params(
            subject=subject,
            html=html,
            text=text,
            from_name=from_name,
            from_email=from_email,
            to_email=to_email,
            to_name=to_name,
        )
        res = self._post_request(METHOD_PATHS.email_send, params)
        assert res['result']
        return res