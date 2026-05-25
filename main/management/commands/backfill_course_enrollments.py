from django.core.management.base import BaseCommand
from main.models import Course, LessonCompletion, CourseEnrollment

class Command(BaseCommand):
    help = 'Заполняет CourseEnrollment для существующих пользователей и их пройденных уроков'

    def handle(self, *args, **options):
        # Укажите slug вашего курса
        course = Course.objects.get(slug='tatarskii-yazyk-s-nulya')
        completions = LessonCompletion.objects.filter(lesson__course=course).select_related('user')
        user_dict = {}
        for comp in completions:
            if comp.user.id not in user_dict:
                user_dict[comp.user.id] = set()
            user_dict[comp.user.id].add(comp.lesson_id)

        for user_id, lesson_ids in user_dict.items():
            enrollment, created = CourseEnrollment.objects.get_or_create(
                user_id=user_id,
                course=course
            )
            enrollment.lessons_completed = len(lesson_ids)
            enrollment.course_xp = len(lesson_ids) * 150  # каждый урок даёт 150 XP
            enrollment.save()
            self.stdout.write(f"Обновлён {enrollment.user.username}: {enrollment.lessons_completed} уроков, {enrollment.course_xp} XP")

        self.stdout.write(self.style.SUCCESS('Готово!'))