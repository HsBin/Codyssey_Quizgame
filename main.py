import json
import os
import random
from datetime import datetime #표준라이브러리라서 외부라이브러리 금지조건에도 문제없음.

STATE_FILE = "state.json"

#Quiz 클래스, 퀴즈 1개의 역할
class Quiz:
    #보너스 기능3 위한 hint 매개변수 추가.
    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint



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
            "answer": self.answer,
            "hint": self.hint           #보너스 기능3 위한 "hint" 데이터 추가.
        }

#QuizGame을 진행하는 class
class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.best_correct = 0
        self.best_total = 0
        self.score_history = [] #보너스기능5 점수기록 히스토리

        self.load_state()
    
    #기본 퀴즈 반환 함수(주제: 게임)
    def get_default_quizzes(self):
        return [
            Quiz(
                "마인크래프트를 개발한 인물은 누구일까요?",
                ["게이브 뉴웰", "마르쿠스 페르손", "토비 폭스", "시드 마이어"],
                2,
                "Notch라는 닉네임으로 알려진 개발자입니다."
            ),
            Quiz(
                "리그 오브 레전드를 개발한 회사는?",
                ["Valve", "Blizzard", "Riot Games", "Nintendo"],
                3,
                "발로란트를 개발한 회사이기도 합니다."
            ),
            Quiz(
                "언리얼 엔진을 개발한 회사는?",
                ["Epic Games", "Unity Technologies", "Valve", "Ubisoft"],
                1,
                "포트나이트를 개발한 회사입니다."
            ),
            Quiz(
                "스타듀 밸리의 개발자는?",
                ["Eric Barone", "Markus Persson", "Hideo Kojima", "Shigeru Miyamoto"],
                1,
                "ConcernedApe라는 이름으로도 활동합니다."
            ),
            Quiz(
                "젤다의 전설 시리즈를 제작한 게임 회사는?",
                ["Sony", "Nintendo", "Microsoft", "Capcom"],
                2,
                "마리오 시리즈를 제작한 회사이기도 합니다."
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
        print("5. 퀴즈 삭제")
        print("6. 종료")
        print("=" * 40)

    #퀴즈를 실행하는 함수
    def play_quiz(self):
        if len(self.quizzes) == 0:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        quizzes = self.quizzes.copy()

        # 풀 문제 수 선택(보너스 기능2 관련)
        quiz_count = self.get_number_input(
            f"\n몇 문제를 풀겠습니까? (1-{len(quizzes)}): ",
            1,
            len(quizzes)
        )

        # 보너스 기능1: 랜덤 출제
        random.shuffle(quizzes)

        # 선택한 문제 수만 사용
        quizzes = quizzes[:quiz_count]

        print()
        print(f"📝 퀴즈를 시작합니다! (총 {len(quizzes)}문제)")

        #정답 개수, 힌트 사용 개수
        correct_count = 0
        hint_count = 0

        #문제 출력 및 정답 입력받기.
        for index, quiz in enumerate(quizzes, start=1):
            print(f"\n[문제 {index}/{len(quizzes)}]")

            quiz.display()

            use_hint = self.get_number_input(
                "\n힌트를 보시겠습니까? (1. 예 / 2. 아니오): ",
                1,
                2
            )

            if use_hint == 1:
                if quiz.hint:
                    print(f"💡 힌트: {quiz.hint}")
                    hint_count += 1
                else:
                    print("⚠️ 등록된 힌트가 없습니다.")

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

        #hint 사용개수 * 5 만큼 패널티 점수 부여
        hint_penalty = hint_count * 5
        score -= hint_penalty

        #최종점수가 음수라면, 0으로 초기화.
        if score < 0:
            score = 0

        # 보너스기능5 - 현재 게임 결과를 기록(딕셔너리 형태로)
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "score": score,
            "correct": correct_count,
            "total": total
        }

        #보너스기능5 - 리스트로 추가.
        self.score_history.append(record)

        print()
        print("=" * 40)
        print(
            f"🏆 결과: {total}문제 중 "
            f"{correct_count}문제 정답! ({score}점)"
        )

        #힌트 사용한 적 있으면, 추가로 힌트 사용횟수와 차감점수 출력
        if hint_count > 0:
            print(
                f"💡 힌트 {hint_count}회 사용 "
                f"(-{hint_penalty}점)"
            )
    
        #기존의 최고점수가 없거나 더 높을 때 갱신.
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_correct = correct_count
            self.best_total = total

            print("🎉 새로운 최고 점수입니다!")

        #보너스 기능5 - 최고기록에 상관없이 게임 기록 저장하도록 변경 (원래는 최고기록갱신때만 저장했음.)
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

        #힌트 입력받기
        hint = self.get_text_input(
            "힌트를 입력하세요: "
        )

        #딕셔너리 형태로 퀴즈 데이터 초기화.
        new_quiz = Quiz(
            question,
            choices,
            answer,
            hint
        )

        #퀴즈 추가
        self.quizzes.append(new_quiz)

        #저장함수 호출
        self.save_state()

        print("\n✅ 퀴즈가 추가되었습니다!")


    #퀴즈 목록 출력 함수
    def show_quiz_list(self):
        print()

        #등록된 퀴즈 없을 때
        if len(self.quizzes) == 0:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        #퀴즈 총 개수 출력
        print(
            f"📋 등록된 퀴즈 목록 "
            f"(총 {len(self.quizzes)}개)"
        )

        print("-" * 40)
    
        #퀴즈 1번부터 문제 출력
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")

        print("-" * 40)

    # 등록된 퀴즈를 삭제하는 함수
    def delete_quiz(self):
        # 퀴즈가 없는 경우
        if len(self.quizzes) == 0:
            print("\n⚠️ 삭제할 퀴즈가 없습니다.")
            return

        # 현재 퀴즈 목록 출력
        self.show_quiz_list()

        # 삭제할 퀴즈 번호 입력
        quiz_number = self.get_number_input(
            f"삭제할 퀴즈 번호 (1-{len(self.quizzes)}): ",
            1,
            len(self.quizzes)
        )

        # 리스트의 인덱스는 0부터 시작하므로 -1, 해당 위치 데이터 제거하면서, 제거한 데이터 반환
        deleted_quiz = self.quizzes.pop(quiz_number - 1)

        # 삭제된 상태를 파일에 저장
        self.save_state()

        print(
            f"\n🗑️ '{deleted_quiz.question}' "
            f"퀴즈가 삭제되었습니다."
        )

    #현재 최고점수 출력 함수
    def show_best_score(self):
        print()

        #최고점수가 존재하지 않을 때
        if self.best_score is None:
            print("🏆 아직 퀴즈를 풀지 않았습니다.")
            return
    
        #최고점수와 문제 개수, 정답 문제 개수 출력
        print(
            f"🏆 최고 점수: {self.best_score}점 "
            f"({self.best_total}문제 중 "
            f"{self.best_correct}문제 정답)"
        )

        #점수 기록 출력
        print("\n📊 게임 기록")
        print("-" * 40)

        for index, record in enumerate(self.score_history, start=1):
            print(
                f"[{index}] {record['date']} | "
                f"{record['score']}점 | "
                f"{record['total']}문제 중 "
                f"{record['correct']}문제 정답"
            )

        print("-" * 40)



    #state에 저장 하는 함수
    def save_state(self):
        #데이터 딕셔너리 형태로 변환해서 초기화
        data = {
            "quizzes": [
                quiz.to_dict()
                for quiz in self.quizzes
            ],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
            "score_history": self.score_history # 보너스기능5 - 점수 역사 기록위한 데이터
        }
        #오류발생 대비 try구문
        try:
            with open(
                STATE_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )
        #오류 발생 함수 사용. OS,Type
        except (OSError, TypeError) as error:
            print(
                f"⚠️ 데이터를 저장하는 중 "
                f"오류가 발생했습니다: {error}"
            )


    #state 데이터 가져오는 함수
    def load_state(self):
        #state저장하는 파일이 없을 때
        if not os.path.exists(STATE_FILE):
            print("📂 저장 파일이 없어 기본 퀴즈를 생성합니다.")

            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            self.best_correct = 0
            self.best_total = 0
            self.score_history = []

            self.save_state()
            return

        try:
            with open(
                STATE_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            quizzes_data = data.get("quizzes", [])

            self.quizzes = []

            #파일은 있지만, 저장된 퀴즈 데이터가 없을때
            if len(quizzes_data) == 0:
                print("⚠️ 저장된 퀴즈가 없어 기본 퀴즈를 불러옵니다.")
                self.quizzes = self.get_default_quizzes()
                self.save_state()
                return
            
            for quiz_data in quizzes_data:
                quiz = Quiz(
                    quiz_data["question"],
                    quiz_data["choices"],
                    quiz_data["answer"],
                    quiz_data.get("hint", "") #hint가 있으면 가져오고 hint가 없으면 "" 사용.
                )

                self.quizzes.append(quiz)
        
            #가져온 데이터로 최고 점수 관련 데이터 초기화.
            self.best_score = data.get("best_score")
            self.best_correct = data.get("best_correct", 0)
            self.best_total = data.get("best_total", 0)
            self.score_history = data.get("score_history", [])

            #저장된 퀴즈 개수와 최고점수(없을 시 없다고 출력) 함께 출력
            print(
                "📂 저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(self.quizzes)}개"
                f", 최고점수 "
                f"{self.best_score if self.best_score is not None else '없음'})"
            )
        #예외처리
        except (
            json.JSONDecodeError,
            OSError,
            KeyError,
            TypeError
        ) as error:

            print(
                "⚠️ 저장 파일이 손상되었거나 "
                "읽을 수 없습니다."
            )
            print(
                "기본 퀴즈 데이터로 복구합니다."
            )

            #저장 파일에 문제 있을 시 기본 퀴즈 데이터로 복구.
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            self.best_correct = 0
            self.best_total = 0
            self.score_history = []

            self.save_state()


    #퀴즈 게임 스타트 하는 함수.
    def run(self):
        while True:
            self.display_menu()

            choice = self.get_number_input(
                "선택: ",
                1,
                6
            )

            if choice == 1:
                self.play_quiz()

            elif choice == 2:
                self.add_quiz()

            elif choice == 3:
                self.show_quiz_list()

            elif choice == 4:
                self.show_best_score()

            elif choice == 5:
                self.delete_quiz()

            elif choice == 6:
                self.save_state()
                print("\n💾 데이터를 저장했습니다.")
                print("👋 퀴즈 게임을 종료합니다.")
                break

#main함수(객체생성하고 실행하는 곳)
def main():
    game = QuizGame()

    try:
        game.run()

    except KeyboardInterrupt:
        print("\n\n⚠️ Ctrl+C가 입력되었습니다.")
        print("💾 데이터를 저장하고 안전하게 종료합니다.")

        game.save_state()

    except EOFError:
        print("\n\n⚠️ 입력 스트림이 종료되었습니다.")
        print("💾 데이터를 저장하고 안전하게 종료합니다.")

        game.save_state()


if __name__ == "__main__":
    main()
