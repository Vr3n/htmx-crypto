from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Transaction
from .forms import TransactionForm


def home(request):
    form = TransactionForm()
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            transactions = Transaction.objects.filter(user=request.user)[:3]
            return render(request, "components/successful_transaction.html", {"form": TransactionForm(), 'transactions': transactions})
        else:
            return render(
                request,
                "components/transaction_form.html",
                {"form": form}
            )

    return render(request, "home.html", {"form": form})


def currencies(request, input_clicked):
    return render(request, "components/currencies.html", {"input_clicked": input_clicked})


def transactions(request):
    """
    Give paginator a list of objects, plus the number of items you'd like to
    have on each page, and it gives you methods for accessing the items for each
    page.
    """
    transactions_list = Transaction.objects.filter(user=request.user)
    paginator = Paginator(transactions_list, 3)
    page_number = request.GET.get("page")
    transactions = paginator.get_page(page_number)
    print("View Called!")
    print(transactions_list)
    print(transactions)
    return render(
        request,
        "components/transactions.html",
        {"transactions": transactions},
    )


def transaction_update(request, transaction_pk):
    transaction = get_object_or_404(Transaction, pk=transaction_pk)
    inline_form = TransactionForm(instance=transaction)
    # new
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save()
            return render(
                request,
                "components/transaction_detail.html",
                {"transaction": transaction},
            )
        else:
            return render(
                request,
                "components/transaction_update.html",
                {
                    "inline_form": inline_form,
                    "transaction": transaction,
                    "errors": form.errors,
                },
            )
    # end new
    return render(
        request,
        "components/transaction_update.html",
        {"inline_form": inline_form, "transaction": transaction},
    )

@require_http_methods(["DELETE"])
def delete(request, transaction_pk):
    transaction = get_object_or_404(Transaction, pk=transaction_pk)
    transaction.delete()
    return redirect("transactions")