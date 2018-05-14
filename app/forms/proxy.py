from wtforms import Form, StringField
from wtforms.validators import DataRequired, Length, ValidationError


class ProxyCookieForm(Form):
    proxy_cookie = StringField('Cookie', validators=[
        DataRequired(), Length(100, -1, message='Cookie至少需要100个字符')])

    def validate_proxy_cookie(self, field):
        proxy_cookie = field.data
        if 'JSESSIONID' not in proxy_cookie:
            raise ValidationError('Cookie无效，请确认后再提交')
        if len(proxy_cookie.split(' ')) < 10:
            raise ValidationError('Cookie无效，请确认后再提交')
