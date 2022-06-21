import base64


with open('frontend/src/images/hamburger-menu.png', 'rb') as file:
    data = file.read()
    print(
        base64.b64encode(data),
        base64.standard_b64encode(data),
        base64.urlsafe_b64encode(data),
        sep=3 * '\n'
    )
