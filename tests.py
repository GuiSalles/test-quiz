import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_invalid_points_below_minimum():
    with pytest.raises(Exception):
        Question(title='q1', points=0)


def test_create_question_with_invalid_points_above_maximum():
    with pytest.raises(Exception):
        Question(title='q1', points=101)


def test_add_choice_returns_created_choice():
    question = Question(title='q1')

    choice = question.add_choice('Opção A', True)

    assert choice in question.choices
    assert choice.text == 'Opção A'
    assert choice.is_correct is True


def test_add_multiple_choices_generates_sequential_ids():
    question = Question(title='q1')

    choice1 = question.add_choice('A')
    choice2 = question.add_choice('B')
    choice3 = question.add_choice('C')

    assert choice1.id == 1
    assert choice2.id == 2
    assert choice3.id == 3


def test_add_choice_with_empty_text_raises_exception():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('')


def test_add_choice_with_text_longer_than_100_characters_raises_exception():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('a' * 101)


def test_remove_choice_by_id_removes_only_target_choice():
    question = Question(title='q1')
    choice1 = question.add_choice('A')
    choice2 = question.add_choice('B')

    question.remove_choice_by_id(choice1.id)

    assert len(question.choices) == 1
    assert question.choices[0].id == choice2.id
    assert question.choices[0].text == 'B'


def test_remove_choice_by_invalid_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('A')

    with pytest.raises(Exception):
        question.remove_choice_by_id(999)


def test_remove_all_choices_clears_question_choices():
    question = Question(title='q1')
    question.add_choice('A')
    question.add_choice('B')

    question.remove_all_choices()

    assert question.choices == []


def test_set_correct_choices_marks_only_selected_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('A')
    choice2 = question.add_choice('B')
    choice3 = question.add_choice('C')

    question.set_correct_choices([choice1.id, choice3.id])

    assert choice1.is_correct is True
    assert choice2.is_correct is False
    assert choice3.is_correct is True


def test_set_correct_choices_with_invalid_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('A')

    with pytest.raises(Exception):
        question.set_correct_choices([999])


def test_correct_selected_choices_returns_only_correct_selected_ids():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('A')
    choice2 = question.add_choice('B')
    choice3 = question.add_choice('C')

    question.set_correct_choices([choice1.id, choice3.id])

    corrected = question.correct_selected_choices([choice1.id, choice2.id])

    assert corrected == [choice1.id]


def test_correct_selected_choices_raises_exception_when_exceeding_max_selections():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('A')
    choice2 = question.add_choice('B')

    with pytest.raises(Exception):
        question.correct_selected_choices([choice1.id, choice2.id])

@pytest.fixture
def question_with_choices():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('A')
    c2 = question.add_choice('B')
    c3 = question.add_choice('C')
    question.set_correct_choices([c1.id, c3.id])
    return question


def test_correct_selected_choices_with_fixture(question_with_choices):
    question = question_with_choices

    selected = [1, 2]  
    result = question.correct_selected_choices(selected)

    assert result == [1]


def test_remove_choice_with_fixture(question_with_choices):
    question = question_with_choices

    initial_len = len(question.choices)
    choice_to_remove = question.choices[0]

    question.remove_choice_by_id(choice_to_remove.id)

    assert len(question.choices) == initial_len - 1
    assert choice_to_remove not in question.choices