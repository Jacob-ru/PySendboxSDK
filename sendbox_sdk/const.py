
SENDBOX_API_ENDPOINT = "https://mailer-api.i.bizml.ru"


class METHOD_PATHS:
    auth = "/oauth/access_token"

    email_send = "/smtp/emails"
    emails_total = "/smtp/emails/total"
    email_info = "/smtp/emails/%s"
    emails_info = "/smtp/emails/info"

    unsubscribe = "/smtp/unsubscribe"