from rest_framework import serializers


class UserLoginSuccessResponse(serializers.Serializer):
    token = serializers.CharField(
        label='토큰'
    )


class UserLoginFailResponse(serializers.Serializer):
    message = serializers.CharField(
        label='메세지',
        default='아이디와 비밀번호를 다시 한번 확인해주세요.'
    )
    code = serializers.CharField(
        label='에러 코드',
        default='WRONG CREDENTIALS'
    )

    @classmethod
    def json(cls):
        return {
            'message': '아이디와 비밀번호를 다시 한번 확인해주세요.',
            'code': 'WRONG CREDENTIALS'
        }


class UserDuplicateResponse(serializers.Serializer):
    is_duplicate = serializers.BooleanField(
        label='아이디 중복 여부'
    )