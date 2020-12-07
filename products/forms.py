from django import forms


class OrderForm(forms.Form):
    STATUS = (
        ('Новый', 'Новый заказ'),
        ('В ожидании', 'Заказ в ожидании'),
        ('Выполнен', 'Выполненный заказ')
    )
    name = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=255, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 8
    }), required=True)

    # def is_valid(values):
    #     valid = True
    #     for field in values:
    #         if field == '':
    #             valid = False
    #     return valid
