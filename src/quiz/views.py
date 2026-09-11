from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Exam, Question, Choice
from .forms import QuestionForm, ChoiceFormSet


def exam_list(request):
    exams = Exam.objects.all()
    return render(request, "quiz/exam_list.html", {"exams": exams})


def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    return render(request, "quiz/exam_detail.html", {"exam": exam})


def question_create(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()

            formset.instance = question
            formset.save()

            correctas = question.choices.filter(is_correct=True).count()
            if correctas != 1:
                question.delete()
                messages.error(
                    request,
                    "Debe marcar exactamente una opción como correcta."
                )
            else:
                messages.success(request, "Pregunta creada correctamente.")
                return redirect("quiz:exam_detail", pk=exam.pk)
    else:
        form = QuestionForm()
        formset = ChoiceFormSet()

    return render(
        request,
        "quiz/question_form.html",
        {"form": form, "formset": formset, "exam": exam},
    )