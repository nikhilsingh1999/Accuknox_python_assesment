# Accuknox_python_assesment
Django Signals – Behavior Demonstration
🧩 Django Signals – Behavior Demonstration

This repository demonstrates how Django signals behave in terms of:

Execution timing (synchronous/asynchronous)

Thread context

Database transaction behavior

Each example is backed by working code and console output proof.

Question 1:
🧠 Are Django signals executed synchronously or asynchronously by default?
✅ Answer:

By default, Django signals are executed synchronously.
When a signal is triggered (e.g., post_save), Django waits for all connected receivers to finish executing before continuing with the caller’s code.

🧩 Code Example
# myapp/signals.py
@receiver(post_save, sender=MyModel)
def demo_all(sender, instance, **kwargs):
    print("Signal start time:", timezone.now())
    time.sleep(3)
    print("Signal end time (after 3s sleep):", timezone.now())

# myapp/views.py
def test_sync(request):
    print("Before save:", timezone.now())
    MyModel.objects.create(name="Sync Test")
    print("After save:", timezone.now())
    return HttpResponse("Synchronous test done!")

🧾 Observed Console Output
Before save: 12:00:00
Signal start time: 12:00:00
Signal end time (after 3s sleep): 12:00:03
After save: 12:00:03

💡 Explanation:

The view’s After save line executes after the signal completes, showing that the view waits for the signal to finish.
➡️ Signals are synchronous by default.

Question 2:
🧠 Do Django signals run in the same thread as the caller?
✅ Answer:

Yes — Django signals run in the same thread as the function or view that triggered them.

🧩 Code Example
# myapp/signals.py
@receiver(post_save, sender=MyModel)
def demo_all(sender, instance, **kwargs):
    print(f"Signal thread id: {threading.get_ident()}")

# myapp/views.py
def test_thread(request):
    print(f"View thread id: {threading.get_ident()}")
    MyModel.objects.create(name="Thread Test")
    return HttpResponse("Thread test done!")

🧾 Observed Console Output
View thread id: 139882704922432
Signal thread id: 139882704922432

💡 Explanation:

Both thread IDs are identical, meaning Django does not spawn a background thread for signals.
➡️ Signals execute in the same thread as the caller.

Question 3:
🧠 Do Django signals run in the same database transaction as the caller?
✅ Answer:

Yes — by default, Django signals run inside the same database transaction as the code that triggered them.
If the signal raises an exception, the entire transaction rolls back.

🧩 Code Example
# myapp/signals.py
@receiver(post_save, sender=MyModel)
def demo_all(sender, instance, **kwargs):
    print(f"Row count inside signal: {MyModel.objects.count()}")
    if instance.name == "Rollback Test":
        print("Raising exception to test transaction rollback...")
        raise Exception("Rollback triggered from signal!")

# myapp/views.py
def test_transaction(request):
    try:
        with transaction.atomic():
            MyModel.objects.create(name="Rollback Test")
    except Exception as e:
        print("Caught exception:", e)

    print("Row count after transaction:", MyModel.objects.count())
    return HttpResponse("Transaction test done!")

🧾 Observed Console Output
Row count inside signal: 1
Raising exception to test transaction rollback...
Caught exception: Rollback triggered from signal!
Row count after transaction: 0

💡 Explanation:

The record count rolls back to 0, proving that:

The signal runs inside the same transaction.

An exception inside the signal can rollback the caller’s database changes.

➡️ Signals share the same DB transaction context by default.

🧭 Summary Table
Behavior	Default Mode	Proof
Execution timing	Synchronous	View waits until signal completes
Thread context	Same thread	Same thread ID in logs
Database transaction	Same transaction	Rollback affects both caller and signal

⚡ How to Run the Demo

Start your Django project:

python manage.py runserver


Visit the following URLs:

http://127.0.0.1:8000/sync
 → Test synchronous behavior

http://127.0.0.1:8000/thread
 → Test thread behavior

http://127.0.0.1:8000/transaction
 → Test transaction behavior

Observe the Django console output for results.

🧠 Conclusion

Django’s signal mechanism is designed for in-process event handling —
executed synchronously, in the same thread, and within the same DB transaction by default.

To make signals asynchronous or transaction-independent, you can:

Use transaction.on_commit() to delay execution.

Use Celery, Django-Q, or threading to offload to background workers.
