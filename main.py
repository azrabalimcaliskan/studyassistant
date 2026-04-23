"""
============================================================
 AI-Powered Smart Academic Study Assistant
============================================================
 Group Members:
   Mustafa Berkem Demirtaş  (B2481.060026) – Project Manager & System Analyst
   Emirhan Akdemir           (B2481.060059) – Backend Developer
   Azra Balım Çalışkan       (B2481.060082) – Frontend Developer
   Eray Keskinbaş            (B2380.060067) – Database & Testing Engineer

 OOP Principles:
   ✔ Encapsulation  – private/protected attributes, getters & setters
   ✔ Inheritance    – Student inherits User; Note/Quiz/StudyPlan inherit ContentItem
   ✔ Polymorphism   – summarize(), evaluate(), display() overridden per subclass
   ✔ Abstraction    – ABC base classes define shared interfaces
============================================================
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import List, Optional, Dict
import uuid


# ══════════════════════════════════════════════════════════════════════════════
# 1. ABSTRACT BASE CLASSES
# ══════════════════════════════════════════════════════════════════════════════

class User(ABC):
    """
    Abstract base for all system users.
    Provides encapsulated identity fields shared by every user type.
    """

    def __init__(self, name: str, email: str, password: str) -> None:
        # Private attributes – accessed only through properties (Encapsulation)
        self.__user_id: str   = str(uuid.uuid4())[:8]
        self.__name: str      = name
        self.__email: str     = email
        self.__password: str  = password            # never exposed externally

    # ── Getters / Setters (Encapsulation) ──────────────────────────────────

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self.__name = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        if "@" not in value:
            raise ValueError("Invalid e-mail address.")
        self.__email = value

    def check_password(self, password: str) -> bool:
        """Validate a password without ever exposing the stored hash."""
        return self.__password == password

    # ── Abstract methods (Polymorphism contract) ────────────────────────────

    @abstractmethod
    def login(self) -> str:
        """Authenticate the user and return a session token."""

    @abstractmethod
    def get_role(self) -> str:
        """Return a human-readable role label."""

    def __str__(self) -> str:
        return f"[{self.get_role()}] {self.name} <{self.email}>"


class ContentItem(ABC):
    """
    Abstract base for Note, Quiz, and StudyPlan.
    Enforces a common summarize() interface across all content types.
    """

    def __init__(self, subject: str) -> None:
        self._content_id: str      = str(uuid.uuid4())[:8]
        self._subject: str         = subject
        self._created_at: datetime = datetime.now()

    @property
    def content_id(self) -> str:
        return self._content_id

    @property
    def subject(self) -> str:
        return self._subject

    @abstractmethod
    def summarize(self) -> str:
        """Return a concise summary of the content item."""

    @abstractmethod
    def display(self) -> None:
        """Print all details of the content item to stdout."""


# ══════════════════════════════════════════════════════════════════════════════
# 2. NOTE  (Inherits ContentItem)
# ══════════════════════════════════════════════════════════════════════════════

class Note(ContentItem):
    """
    Represents a lecture note uploaded by a student.

    Attributes (from class diagram):
        noteId, title, content, subject, uploadedDate
    Methods (from class diagram):
        summarize()
    """

    def __init__(self, title: str, subject: str, content: str) -> None:
        super().__init__(subject)
        self.__note_id: str       = self._content_id   # alias for clarity
        self.__title: str         = title
        self.__content: str       = content
        self.__uploaded_date: date = date.today()

    # ── Properties ─────────────────────────────────────────────────────────

    @property
    def note_id(self) -> str:
        return self.__note_id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def content(self) -> str:
        return self.__content

    @content.setter
    def content(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Note content cannot be empty.")
        self.__content = value

    @property
    def uploaded_date(self) -> date:
        return self.__uploaded_date

    # ── Polymorphic methods ─────────────────────────────────────────────────

    def summarize(self) -> str:
        """Return the first 80 characters of the note as a quick summary."""
        preview = self.__content[:80].replace("\n", " ")
        return f"[Note: {self.__title}] {preview}..."

    def display(self) -> None:
        print("─" * 50)
        print(f"  NOTE ID  : {self.__note_id}")
        print(f"  Title    : {self.__title}")
        print(f"  Subject  : {self._subject}")
        print(f"  Uploaded : {self.__uploaded_date}")
        print(f"  Content  :\n{self.__content}")
        print("─" * 50)

    def __repr__(self) -> str:
        return f"Note(id={self.__note_id!r}, title={self.__title!r})"


# ══════════════════════════════════════════════════════════════════════════════
# 3. QUIZ  (Inherits ContentItem)
# ══════════════════════════════════════════════════════════════════════════════

class Quiz(ContentItem):
    """
    An AI-generated quiz tied to a subject.

    Attributes (from class diagram):
        quizId, questions, subjects, score
    Methods (from class diagram):
        generateQuiz(), evaluate()
    """

    def __init__(self, subjects: str) -> None:
        super().__init__(subjects)
        self.__quiz_id: str                  = self._content_id
        self.__questions: List[Dict]         = []
        self.__score: Optional[float]        = None

    # ── Properties ─────────────────────────────────────────────────────────

    @property
    def quiz_id(self) -> str:
        return self.__quiz_id

    @property
    def questions(self) -> List[Dict]:
        return list(self.__questions)           # defensive copy

    @property
    def score(self) -> Optional[float]:
        return self.__score

    # ── Domain Methods ──────────────────────────────────────────────────────

    def generate_quiz(self, source_text: str, num_questions: int = 3) -> None:
        """
        Populate questions from source_text.
        In production this delegates to AIEngine; here we build simple stubs.
        """
        self.__questions.clear()
        words = source_text.split()
        for i in range(min(num_questions, len(words))):
            keyword = words[i]
            self.__questions.append({
                "id":       i + 1,
                "question": f"Explain the concept of '{keyword}' in your own words.",
                "options":  ["Option A", "Option B", "Option C", "Option D"],
                "answer":   "Option A",
            })
        print(f"  ✓ {len(self.__questions)} question(s) generated for subject '{self._subject}'.")

    def evaluate(self, student_answers: List[str]) -> float:
        """
        Compare student_answers against correct answers.
        Returns a percentage score and stores it internally.
        (Polymorphism: subclasses like TimedQuiz could override this.)
        """
        if not self.__questions:
            raise RuntimeError("Quiz has no questions. Call generate_quiz() first.")
        correct = sum(
            1 for q, ans in zip(self.__questions, student_answers)
            if ans == q["answer"]
        )
        self.__score = round((correct / len(self.__questions)) * 100, 2)
        return self.__score

    # ── Polymorphic methods ─────────────────────────────────────────────────

    def summarize(self) -> str:
        score_str = f"{self.__score}%" if self.__score is not None else "not taken yet"
        return f"[Quiz: {self._subject}] {len(self.__questions)} question(s) | Score: {score_str}"

    def display(self) -> None:
        print("─" * 50)
        print(f"  QUIZ ID  : {self.__quiz_id}")
        print(f"  Subject  : {self._subject}")
        print(f"  Score    : {self.__score if self.__score is not None else 'N/A'}")
        for q in self.__questions:
            print(f"\n  Q{q['id']}: {q['question']}")
            for opt in q["options"]:
                print(f"       • {opt}")
        print("─" * 50)

    def __repr__(self) -> str:
        return f"Quiz(id={self.__quiz_id!r}, subject={self._subject!r})"


# ══════════════════════════════════════════════════════════════════════════════
# 4. STUDY PLAN  (Inherits ContentItem)
# ══════════════════════════════════════════════════════════════════════════════

class StudyPlan(ContentItem):
    """
    A personalised, AI-generated weekly study plan.

    Attributes (from class diagram):
        planId, subjects, schedule
    Methods (from class diagram):
        generatePlan()
    """

    def __init__(self, subjects: List[str]) -> None:
        super().__init__(", ".join(subjects))
        self.__plan_id: str           = self._content_id
        self.__subjects: List[str]    = subjects
        self.__schedule: Dict[str, List[str]] = {}

    # ── Properties ─────────────────────────────────────────────────────────

    @property
    def plan_id(self) -> str:
        return self.__plan_id

    @property
    def subjects(self) -> List[str]:
        return list(self.__subjects)

    @property
    def schedule(self) -> Dict[str, List[str]]:
        return dict(self.__schedule)            # defensive copy

    # ── Domain Methods ──────────────────────────────────────────────────────

    def generate_plan(self, days_until_exam: int = 7) -> None:
        """
        Build a day-by-day schedule distributing subjects evenly.
        In production this delegates to AIEngine.
        """
        self.__schedule.clear()
        for i, topic in enumerate(self.__subjects):
            day = f"Day {(i % days_until_exam) + 1}"
            self.__schedule.setdefault(day, []).append(f"Study: {topic}")
        print(f"  ✓ Study plan generated across {len(self.__schedule)} day(s).")

    # ── Polymorphic methods ─────────────────────────────────────────────────

    def summarize(self) -> str:
        return (f"[StudyPlan: {self._subject}] "
                f"{len(self.__schedule)} day(s) planned | "
                f"Topics: {', '.join(self.__subjects)}")

    def display(self) -> None:
        print("─" * 50)
        print(f"  PLAN ID  : {self.__plan_id}")
        print(f"  Subjects : {self._subject}")
        if self.__schedule:
            for day, tasks in sorted(self.__schedule.items()):
                print(f"\n  {day}:")
                for task in tasks:
                    print(f"    → {task}")
        else:
            print("  (Plan not yet generated. Call generate_plan() first.)")
        print("─" * 50)

    def __repr__(self) -> str:
        return f"StudyPlan(id={self.__plan_id!r})"


# ══════════════════════════════════════════════════════════════════════════════
# 5. AI ENGINE
# ══════════════════════════════════════════════════════════════════════════════

class AIEngine:
    """
    Core AI service layer.

    Methods (from class diagram):
        summarizeNotes(), generateQuiz(), createStudyPlan()

    Uses the Strategy pattern: swap _backend for OpenAI, local LLM, etc.
    Encapsulation: the API key is private and never leaked.
    """

    def __init__(self, api_key: str = "DEMO") -> None:
        self.__api_key: str = api_key           # private – never exposed

    # ── Public API ──────────────────────────────────────────────────────────

    def summarize_notes(self, note: Note) -> str:
        """
        Generate an AI summary of the given Note.
        Returns structured bullet points derived from the note's content.
        """
        sentences = [s.strip() for s in note.content.split(".") if s.strip()]
        bullets   = "\n  • ".join(sentences[:4])
        return f"[AI Summary for '{note.title}']\n  • {bullets}"

    def generate_quiz(self, note: Note, num_questions: int = 3) -> Quiz:
        """
        Create and populate a Quiz from a Note's content.
        Returns a ready-to-use Quiz object.
        """
        quiz = Quiz(subjects=note.subject)
        quiz.generate_quiz(source_text=note.content, num_questions=num_questions)
        return quiz

    def create_study_plan(self, subjects: List[str], days_until_exam: int = 7) -> StudyPlan:
        """
        Build a personalised StudyPlan for the given subjects.
        Returns a populated StudyPlan object.
        """
        plan = StudyPlan(subjects=subjects)
        plan.generate_plan(days_until_exam=days_until_exam)
        return plan

    def __repr__(self) -> str:
        return f"AIEngine(api_key={'*' * 8})"


# ══════════════════════════════════════════════════════════════════════════════
# 6. DATABASE
# ══════════════════════════════════════════════════════════════════════════════

class Database:
    """
    Persistence layer. Stores and retrieves all application data.

    Methods (from class diagram):
        saveData(), retrieveData()

    Encapsulation: internal storage is private; access only through methods.
    Singleton-like: one shared instance is typical for a DB layer.
    """

    def __init__(self) -> None:
        # Private in-memory store (replace with MySQL/SQLite in production)
        self.__store: Dict[str, Dict] = {
            "students":    {},
            "notes":       {},
            "quizzes":     {},
            "study_plans": {},
        }

    # ── Public Methods ──────────────────────────────────────────────────────

    def save_data(self, table: str, record_id: str, data: object) -> None:
        """Persist an object under the given table and ID."""
        if table not in self.__store:
            self.__store[table] = {}
        self.__store[table][record_id] = data
        print(f"  ✓ Saved to '{table}' with id='{record_id}'.")

    def retrieve_data(self, table: str, record_id: str) -> Optional[object]:
        """Fetch a previously saved object; returns None if not found."""
        record = self.__store.get(table, {}).get(record_id)
        if record is None:
            print(f"  ✗ Record '{record_id}' not found in '{table}'.")
        return record

    def list_all(self, table: str) -> List[object]:
        """Return all records stored in a given table."""
        return list(self.__store.get(table, {}).values())

    def __repr__(self) -> str:
        sizes = {t: len(v) for t, v in self.__store.items()}
        return f"Database({sizes})"


# ══════════════════════════════════════════════════════════════════════════════
# 7. DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

class Dashboard:
    """
    Displays a student's performance overview and quiz history.

    Methods (from class diagram):
        showPerformance(), showQuizResults()

    Aggregates data from the Database; does not store data itself.
    """

    def __init__(self, db: Database) -> None:
        self.__db: Database = db            # composition – Dashboard owns a DB reference

    def show_performance(self, student: "Student") -> None:
        """Print an overall performance summary for the student."""
        results: List[QuizResult] = self.__db.retrieve_data("quiz_results", student.student_id) or []
        print("\n" + "═" * 50)
        print(f"  DASHBOARD — {student.name}")
        print("═" * 50)
        if not results:
            print("  No quiz results recorded yet.")
        else:
            scores  = [r.score for r in results]
            average = sum(scores) / len(scores)
            print(f"  Quizzes taken : {len(results)}")
            print(f"  Average score : {average:.1f}%")
            print(f"  Best score    : {max(scores):.1f}%")
            print(f"  Worst score   : {min(scores):.1f}%")
        print("═" * 50)

    def show_quiz_results(self, student: "Student") -> None:
        """List every individual quiz result for the student."""
        results: List[QuizResult] = self.__db.retrieve_data("quiz_results", student.student_id) or []
        print(f"\n  Quiz Results for {student.name}:")
        if not results:
            print("  (none)")
        for r in results:
            print(f"  • {r.subject:20s}  Score: {r.score:.1f}%  Date: {r.taken_on}")

    def __repr__(self) -> str:
        return "Dashboard()"


# ══════════════════════════════════════════════════════════════════════════════
# 8. QUIZ RESULT  (value object – stores one quiz attempt)
# ══════════════════════════════════════════════════════════════════════════════

class QuizResult:
    """
    Immutable record of one quiz attempt by a student.
    Encapsulates score, subject, and timestamp.
    """

    def __init__(self, subject: str, score: float) -> None:
        self.__subject: str  = subject
        self.__score: float  = score
        self.__taken_on: date = date.today()

    @property
    def subject(self) -> str:
        return self.__subject

    @property
    def score(self) -> float:
        return self.__score

    @property
    def taken_on(self) -> date:
        return self.__taken_on

    def __repr__(self) -> str:
        return f"QuizResult(subject={self.__subject!r}, score={self.__score}%)"


# ══════════════════════════════════════════════════════════════════════════════
# 9. STUDENT  (Inherits User)
# ══════════════════════════════════════════════════════════════════════════════

class Student(User):
    """
    A registered university student.

    Attributes (from class diagram):
        studentId, name, email, password
    Methods (from class diagram):
        login(), uploadNote(), viewDashboard()

    Inheritance  : extends User (gains user_id, name, email, check_password).
    Encapsulation: student_id and internal lists are private.
    Polymorphism : overrides login() and get_role() from User.
    """

    def __init__(self, name: str, email: str, password: str, student_id: str) -> None:
        super().__init__(name, email, password)
        self.__student_id: str              = student_id
        self.__notes: List[Note]            = []
        self.__quiz_results: List[QuizResult] = []
        self.__study_plan: Optional[StudyPlan] = None

    # ── Properties ─────────────────────────────────────────────────────────

    @property
    def student_id(self) -> str:
        return self.__student_id

    @property
    def notes(self) -> List[Note]:
        return list(self.__notes)

    @property
    def study_plan(self) -> Optional[StudyPlan]:
        return self.__study_plan

    # ── Polymorphic overrides ───────────────────────────────────────────────

    def login(self) -> str:
        """Authenticate and return a simple session token."""
        token = f"TOKEN-{self.__student_id}-{uuid.uuid4().hex[:6].upper()}"
        print(f"  ✓ Student '{self.name}' logged in. Session: {token}")
        return token

    def get_role(self) -> str:
        return "Student"

    # ── Domain Methods (from class diagram) ────────────────────────────────

    def upload_note(self, note: Note, db: Database) -> None:
        """
        Attach a Note to this student and persist it in the Database.
        Implements the 'uploads' association from the class diagram.
        """
        self.__notes.append(note)
        db.save_data("notes", note.note_id, note)
        print(f"  ✓ Note '{note.title}' uploaded by {self.name}.")

    def view_dashboard(self, dashboard: Dashboard) -> None:
        """Render the student's full performance dashboard."""
        dashboard.show_performance(self)
        dashboard.show_quiz_results(self)

    def record_quiz_result(self, result: QuizResult, db: Database) -> None:
        """Save a quiz result for this student."""
        self.__quiz_results.append(result)
        # Store results list under the student's ID
        db.save_data("quiz_results", self.__student_id, self.__quiz_results)

    def assign_study_plan(self, plan: StudyPlan) -> None:
        """Attach an AI-generated study plan to this student."""
        self.__study_plan = plan
        print(f"  ✓ Study plan assigned to {self.name}.")

    def __repr__(self) -> str:
        return f"Student(id={self.__student_id!r}, name={self.name!r})"


# ══════════════════════════════════════════════════════════════════════════════
# 10. DEMO — wires everything together
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print("\n" + "╔" + "═" * 56 + "╗")
    print("║   AI-Powered Smart Academic Study Assistant — DEMO   ║")
    print("╚" + "═" * 56 + "╝\n")

    # ── Initialise infrastructure ───────────────────────────────────────────
    db        = Database()
    ai_engine = AIEngine(api_key="sk-demo-key")
    dashboard = Dashboard(db)

    # ── Create a student (Inheritance: Student → User) ──────────────────────
    print("► Creating student account…")
    student = Student(
        name       = "Ali Yılmaz",
        email      = "ali@university.edu",
        password   = "secure123",
        student_id = "STU-101",
    )
    db.save_data("students", student.student_id, student)

    # ── Login (Polymorphism: Student overrides User.login()) ─────────────────
    print("\n► Login…")
    token = student.login()

    # ── Upload a note (Encapsulation + composition) ──────────────────────────
    print("\n► Uploading lecture note…")
    note = Note(
        title   = "Introduction to Machine Learning",
        subject = "Computer Science",
        content = (
            "Machine learning is a branch of AI. "
            "Supervised learning uses labelled data. "
            "Unsupervised learning finds hidden patterns. "
            "Neural networks mimic the human brain. "
            "Gradient descent optimises model weights."
        ),
    )
    student.upload_note(note, db)

    # ── AI: summarise note ───────────────────────────────────────────────────
    print("\n► AI summarising note…")
    summary = ai_engine.summarize_notes(note)
    print(summary)

    # ── AI: generate quiz from note (Polymorphism: Quiz.evaluate()) ──────────
    print("\n► AI generating quiz…")
    quiz = ai_engine.generate_quiz(note, num_questions=3)
    quiz.display()

    # ── Student takes the quiz ───────────────────────────────────────────────
    print("► Student submits answers…")
    student_answers = ["Option A", "Option B", "Option A"]
    score = quiz.evaluate(student_answers)
    print(f"  Score: {score}%")

    result = QuizResult(subject=quiz.subject, score=score)
    student.record_quiz_result(result, db)

    # ── AI: create personalised study plan ───────────────────────────────────
    print("\n► AI creating study plan…")
    plan = ai_engine.create_study_plan(
        subjects       = ["Machine Learning", "Neural Networks", "Gradient Descent"],
        days_until_exam= 5,
    )
    plan.display()
    student.assign_study_plan(plan)

    # ── Dashboard: show performance (Polymorphism: each display() differs) ───
    print("\n► Viewing dashboard…")
    student.view_dashboard(dashboard)

    # ── Polymorphism demo: summarize() called on different ContentItem types ─
    print("\n► Polymorphism demo — summarize() on different content types:")
    items: List[ContentItem] = [note, quiz, plan]
    for item in items:
        print(f"  {item.summarize()}")   # same call, different behaviour each time

    print("\n✔ Demo complete.\n")


if __name__ == "__main__":
    main()