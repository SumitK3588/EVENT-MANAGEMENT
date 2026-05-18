from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .forms import EventForm, TicketPurchaseForm
from django.utils import timezone
from django.http import JsonResponse
from django.utils.text import slugify
import qrcode
import io
import base64


def home(request):
    current_time = timezone.now()
    events = Event.objects.filter(end_time__gt=current_time).order_by("start_time")

    return render(request, "app/home.html", {"events": events})


def create_e(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = EventForm()

    return render(request, "app/create_e.html", {"form": form})


def delete_event(request, event_id):
    # Retrieve the event or return a 404 error if it doesn't exist
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        event.delete()  # Removes the record from the database
        return redirect("home")

    # If a user accidentally navigates here via GET, show a confirmation page
    return render(request, "app/confirm_delete.html", {"event": event})


# def create_e(request):
#     context = {}
#     return render(request, "app/create_e.html", context)


def event_list(request):
    # Analytics: Getting count of events
    events = Event.objects.all()
    context = {"events": events, "total_count": events.count()}
    return render(request, "app/events.html", context)


def buy_ticket(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == "POST":
        form = TicketPurchaseForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data["ticket_quantity"]
            customer_name = form.cleaned_data["full_name"]
            customer_email = form.cleaned_data["email"]

            # 1. Update the database counter
            event.tickets_sold += quantity
            event.save()

            # 2. Compile ticket metadata payload for the QR code scanning layout
            qr_payload = (
                f"--- OFFICIAL TICKET PASS ---\n"
                f"Event: {event.title}\n"
                f"Attendee: {customer_name}\n"
                f"Email: {customer_email}\n"
                f"Quantity: {quantity} Ticket(s)\n"
                f"Location: {event.location}"
            )

            # 3. Generate the QR code image object
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(qr_payload)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # 4. Save the QR image into an in-memory byte buffer (avoiding hard-disk bloat)
            buffer = io.BytesIO()
            qr_img.save(buffer, format="PNG")
            buffer.seek(0)

            # 5. Encode the bytes string to base64 so HTML can read it directly
            qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            qr_data_url = f"data:image/png;base64,{qr_base64}"
            safe_filename = f"Ticket_{slugify(event.title)}"
            # 6. Ship context values to the success download screen
            context = {
                "event": event,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "quantity_bought": quantity,
                "qr_data_url": qr_data_url,
                "safe_filename": safe_filename,
            }
            return render(request, "app/ticket_success.html", context)
    else:
        form = TicketPurchaseForm()

    return render(request, "app/buy_ticket.html", {"form": form, "event": event})


# Keep your existing home, create_event, delete_event, and buy_ticket views here...


# --- ADD THIS NEW VIEW FOR THE CALENDAR DATA ---
def event_calendar_json(request):
    current_time = timezone.now()

    # FILTER: Only pull events whose end_time is GREATER THAN the current time
    active_events = Event.objects.filter(end_time__gt=current_time)

    events_list = []
    for event in active_events:
        events_list.append(
            {
                "title": event.title,
                "start": event.start_time.isoformat(),
                "end": event.end_time.isoformat(),
                "description": event.location,
            }
        )

    return JsonResponse(events_list, safe=False)
