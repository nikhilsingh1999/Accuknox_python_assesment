from django.http import HttpResponse
from django.utils import timezone
from django.db import transaction
import threading
from .models import MyModel


def test_sync(request):
    print("\n--- [SYNC TEST] ---")
    print("Before save:", timezone.now())
    MyModel.objects.create(name="Sync Test")
    print("After save:", timezone.now())
    print("--- END [SYNC TEST] ---\n")
    return HttpResponse("Synchronous test done!")


def test_thread(request):
    print("\n--- [THREAD TEST] ---")
    print("View thread id:", threading.get_ident())
    MyModel.objects.create(name="Thread Test")
    print("--- END [THREAD TEST] ---\n")
    return HttpResponse("Thread test done!")


def test_transaction(request):
    print("\n--- [TRANSACTION TEST] ---")
    try:
        with transaction.atomic():
            MyModel.objects.create(name="Rollback Test")
    except Exception as e:
        print("Caught exception:", e)

    print("Row count after transaction:", MyModel.objects.count())
    print("--- END [TRANSACTION TEST] ---\n")
    return HttpResponse("Transaction test done!")
