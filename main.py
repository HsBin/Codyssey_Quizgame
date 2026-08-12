import json
import os
import random

STATE_FILE = "state.json"

#Quiz 클래스, 퀴즈 1개의 역할
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print("\n" + "-" * 40)
        print(self.question)

        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

#QuizGame을 진행하는 class
class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.best_correct = 0
        self.best_total = 0

        self.load_state()
	
#기본 퀴즈 반환(주제: 게임)
    def get_default_quizzes(self):
        return [
            Quiz(
                "마인크래프트를 개발한 인물은 누구일까요?",
                ["게이브 뉴웰", "마르쿠스 페르손", "토비 폭스", "시드 마이어"],
                2
            ),
            Quiz(
                "리그 오브 레전드를 개발한 회사는?",
                ["Valve", "Blizzard", "Riot Games", "Nintendo"],
                3
            ),
            Quiz(
                "언리얼 엔진을 개발한 회사는?",
                ["Epic Games", "Unity Technologies", "Valve", "Ubisoft"],
                1
            ),
            Quiz(
                "스타듀 밸리의 개발자는?",
                ["Eric Barone", "Markus Persson", "Hideo Kojima", "Shigeru Miyamoto"],
                1
            ),
            Quiz(
                "젤다의 전설 시리즈를 제작한 게임 회사는?",
                ["Sony", "Nintendo", "Microsoft", "Capcom"],
                2
            )
        ]
