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

    #숫자를 입력받는 함수(최소~최대 숫자가 정해져있음).
    def get_number_input(self, message, minimum, maximum):
        while True:
            try:
                value = input(message).strip()

                if value == "":
                    print(
                        f"⚠️ 빈 입력은 사용할 수 없습니다. "
                        f"{minimum}-{maximum} 사이의 숫자를 입력하세요."
                    )
                    continue

                number = int(value)

                if number < minimum or number > maximum:
                    print(
                        f"⚠️ {minimum}-{maximum} 사이의 숫자를 입력하세요."
                    )
                    continue

                return number

            except ValueError:
                print(
                    f"⚠️ 숫자만 입력할 수 있습니다. "
                    f"{minimum}-{maximum} 사이의 숫자를 입력하세요."
                )

    #메시지를 입력받는 함수.(빈 내용X)
    def get_text_input(self, message):
        while True:
            text = input(message).strip()

            if text == "":
                print("⚠️ 빈 내용은 입력할 수 없습니다.")
                continue

            return text
    
    #퀴즈 메뉴를 출력하는 함수
    def display_menu(self):
        print()
        print("=" * 40)
        print("        🎮 게임 상식 퀴즈 🎮")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    #퀴즈를 실행하는 함수
    def play_quiz(self):
        if len(self.quizzes) == 0:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        quizzes = self.quizzes.copy()

        # 보너스 기능: 랜덤 출제
        random.shuffle(quizzes)

        print()
        print(f"📝 퀴즈를 시작합니다! (총 {len(quizzes)}문제)")

        correct_count = 0

        #문제 출력 및 정답 입력받기.
        for index, quiz in enumerate(quizzes, start=1):
            print(f"\n[문제 {index}/{len(quizzes)}]")

            quiz.display()

            answer = self.get_number_input(
                "\n정답 입력 (1-4): ",
                1,
                4
            )

            if quiz.check_answer(answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print("❌ 오답입니다!")
                print(
                    f"정답은 {quiz.answer}번 "
                    f"'{quiz.choices[quiz.answer - 1]}'입니다."
                )
	#점수 계산. 100점 만점
        total = len(quizzes)
        score = int(correct_count / total * 100)

        print()
        print("=" * 40)
        print(
            f"🏆 결과: {total}문제 중 "
            f"{correct_count}문제 정답! ({score}점)"
        )
	
	#기존의 최고점수가 없거나 더 높을 때 갱신.
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_correct = correct_count
            self.best_total = total

            print("🎉 새로운 최고 점수입니다!")

            self.save_state()

        print("=" * 40)
    
    #퀴즈 추가 함수
    def add_quiz(self):
        print()
        print("📌 새로운 퀴즈를 추가합니다.")

        question = self.get_text_input(
            "\n문제를 입력하세요: "
        )

        choices = []

	#선택지 입력받기.
        for i in range(1, 5):
            choice = self.get_text_input(
                f"선택지 {i}: "
            )
            choices.append(choice)

	#정답 입력받기.
        answer = self.get_number_input(
            "정답 번호 (1-4): ",
            1,
            4
        )

	#딕셔너리 형태로 퀴즈 데이터 초기화.
        new_quiz = Quiz(
            question,
            choices,
            answer
        )

	#퀴즈 추가
        self.quizzes.append(new_quiz)

	#저장함수 호출
        self.save_state()

        print("\n✅ 퀴즈가 추가되었습니다!")
