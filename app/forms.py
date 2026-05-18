from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "location", "start_time", "end_time"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Event Title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe your event...",
                }
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Venue or Virtual URL"}
            ),
            "start_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "end_time": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
        }


class TicketPurchaseForm(forms.Form):
    # Personal Details
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "John Doe"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "john@example.com"}
        )
    )

    QUANTITY_CHOICES = [(i, f"{i} Ticket{'s' if i > 1 else ''}") for i in range(1, 6)]
    ticket_quantity = forms.IntegerField(
        widget=forms.Select(choices=QUANTITY_CHOICES, attrs={"class": "form-select"})
    )

    # Simulated Bank/Card Details
    card_number = forms.CharField(
        max_length=16,
        min_length=16,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "1234567812345678",
                "pattern": "[0-7-9]*",
            }
        ),
    )
    expiry_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "MM/YY"}),
    )
    cvv = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "123"}
        ),
    )
